# OpenClaw 自动更新脚本
# 功能：检查版本、更新、清理、重启

param (
    [switch]$CheckOnly,
    [switch]$ForceUpdate,
    [switch]$NoRestart
)

$ErrorActionPreference = "Continue"

Write-Host "🚀 OpenClaw 自动更新检查..." -ForegroundColor Cyan -BackgroundColor Black
Write-Host "时间: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray

# 获取当前版本
Write-Host "
📦 当前版本检查..." -ForegroundColor White
try {
    $currentVersion = npm list openclaw --depth=0 2>&1 | Select-String "\d+\.\d+\.\d+"
    if ($currentVersion) {
        Write-Host "  当前版本: $currentVersion" -ForegroundColor Green
    } else {
        Write-Host "  无法获取当前版本" -ForegroundColor Yellow
        $currentVersion = "未知"
    }
} catch {
    Write-Host "  版本检查失败: $_" -ForegroundColor Red
    $currentVersion = "错误"
}

if ($CheckOnly) {
    Write-Host "
✅ 版本检查完成 (仅检查模式)" -ForegroundColor Green
    exit 0
}

# 检查 npm 注册表
Write-Host "
🌐 检查网络..." -ForegroundColor White
try {
    $registry = npm config get registry
    Write-Host "  NPM Registry: $registry" -ForegroundColor Gray
    
    $testResponse = Invoke-WebRequest -Uri "https://registry.npmjs.org/openclaw" -TimeoutSec 10 -UseBasicParsing -ErrorAction SilentlyContinue
    if ($testResponse.StatusCode -eq 200) {
        Write-Host "  ✅ NPM 注册表可达" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  NPM 注册表响应异常" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  ⚠️  无法连接 NPM 注册表" -ForegroundColor Yellow
}

# 获取最新版本
Write-Host "
📥 检查最新版本..." -ForegroundColor White
try {
    $latestInfo = Invoke-WebRequest -Uri "https://registry.npmjs.org/openclaw/latest" -TimeoutSec 15 -UseBasicParsing -ErrorAction SilentlyContinue | ConvertFrom-Json
    $latestVersion = $latestInfo.version
    Write-Host "  最新版本: $latestVersion" -ForegroundColor Cyan
    
    # 版本比较
    $current = $currentVersion.ToString().Trim()
    if ($current -match '(\d+\.\d+\.\d+)') {
        $current = $Matches[1]
    }
    
    $versionCompare = [System.Version]::Parse($current) -ge [System.Version]::Parse($latestVersion)
    
    if ($versionCompare) {
        Write-Host "  ✅ 已是最新版本" -ForegroundColor Green
        if (-not $ForceUpdate) {
            Write-Host "
🎉 无需更新，OpenClaw 完全正常！" -ForegroundColor Green
            exit 0
        }
    } else {
        Write-Host "  ⚠️  发现新版本可用" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  ❌ 无法获取最新版本信息" -ForegroundColor Red
    Write-Host "  错误: $_" -ForegroundColor Gray
}

# 执行更新
Write-Host "
⬇️  开始更新..." -ForegroundColor White
try {
    Write-Host "  运行: npm update -g openclaw" -ForegroundColor Gray
    $updateResult = npm update -g openclaw 2>&1 | Out-String
    Write-Host "  更新输出: $updateResult" -ForegroundColor Gray
    
    # 清理缓存
    Write-Host "
🧹 清理 npm 缓存..." -ForegroundColor White
    npm cache verify 2>&1 | Out-Null
    
    Write-Host "  ✅ 更新完成" -ForegroundColor Green
} catch {
    Write-Host "  ❌ 更新失败: $_" -ForegroundColor Red
}

# 重启 OpenClaw (如果需要且允许)
if (-not $NoRestart) {
    Write-Host "
🔄 检查是否需要重启..." -ForegroundColor White
    
    $needsRestart = $false
    if ($ForceUpdate) { $needsRestart = $true }
    if ($latestVersion -and $current -ne $latestVersion) { $needsRestart = $true }
    
    if ($needsRestart) {
        Write-Host "  需要重启以应用更新..." -ForegroundColor Yellow
        
        # 检查 Gateway 状态
        Write-Host "  状态: 等待用户确认重启" -ForegroundColor Cyan
        
        Write-Host "
✅ 自动更新检查完成" -ForegroundColor Green
        Write-Host "提示: 运行 'openclaw gateway restart' 重启服务" -ForegroundColor White
    } else {
        Write-Host "  无需重启" -ForegroundColor Green
    }
}

Write-Host "
🎉 OpenClaw 自动更新检查完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Gray
