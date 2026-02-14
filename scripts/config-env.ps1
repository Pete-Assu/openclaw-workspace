# Self-Orchestrator 环境变量配置
# 运行此脚本配置 API Keys

# Moltbook (已配置)
$MOLTBOOK_KEY = "moltbook_sk_oyiwn5NTjQVqrdoThu4XTGutzwpeyfEU"
[Environment]::SetEnvironmentVariable("MOLTBOOK_API_KEY", $MOLTBOOK_KEY, "User")

# ClawHub (需要用户获取)
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🦞 ClawHub API 配置" -ForegroundColor Yellow
Write-Host "========================================"
Write-Host ""
Write-Host "ClawHub 可能需要 API Key 才能访问。"
Write-Host "请访问 https://clawhub.com/settings/api 获取 API Key。"
Write-Host ""
Read-Host "输入 ClawHub API Key (直接回车跳过)" | ForEach-Object {
    if ($_) {
        [Environment]::SetEnvironmentVariable("CLAWHUB_API_KEY", $_, "User")
        Write-Host "✅ ClawHub API Key 已设置" -ForegroundColor Green
    } else {
        Write-Host "⏭️ 跳过 ClawHub 配置" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "📊 当前配置状态" -ForegroundColor Yellow
Write-Host "========================================"

$MOLT = [Environment]::GetEnvironmentVariable("MOLTBOOK_API_KEY", "User")
if ($MOLT) {
    Write-Host "✅ Moltbook: 已配置 (${MOLT.Substring(0, 10)}...)" -ForegroundColor Green
} else {
    Write-Host "❌ Moltbook: 未配置" -ForegroundColor Red
}

$CLAW = [Environment]::GetEnvironmentVariable("CLAWHUB_API_KEY", "User")
if ($CLAW) {
    Write-Host "✅ ClawHub: 已配置" -ForegroundColor Green
} else {
    Write-Host "⏭️ ClawHub: 未配置 (可选)" -ForegroundColor Gray
}

Write-Host ""
Write-Host "配置完成！重启终端后生效。" -ForegroundColor Cyan
