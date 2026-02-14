# MiniMax API 测试脚本
# 使用说明：请在 PowerShell 中设置环境变量 $env:MINIMAX_API_KEY = "你的API密钥"，然后运行此脚本

param (
    [string]$ApiKey = $env:MINIMAX_API_KEY
)

if (-not $ApiKey) {
    Write-Host "❌ 错误：未找到 MiniMax API 密钥" -ForegroundColor Red
    Write-Host "请设置环境变量：`$env:MINIMAX_API_KEY = '你的API密钥'" -ForegroundColor Yellow
    Write-Host "或直接运行：.`TEST_MINIMAX.ps1 -ApiKey '你的API密钥'" -ForegroundColor Yellow
    exit 1
}

Write-Host "🚀 开始测试 MiniMax API..." -ForegroundColor Green

# 测试数据
$testBody = @{
    model = "abab6.5"
    messages = @(
        @{
            role = "user"
            content = "测试消息，请回复：API连接成功"
        }
    )
    temperature = 0.7
    max_tokens = 100
} | ConvertTo-Json -Depth 10

# 请求头
$headers = @{
    "Content-Type" = "application/json"
    "Authorization" = "Bearer $ApiKey"
}

try {
    Write-Host "📡 发送测试请求到 MiniMax 服务器..." -ForegroundColor Cyan
    $response = Invoke-WebRequest -Uri "https://api.minimax.chat/v1/text/chatcompletion_pro" -Method POST -Headers $headers -Body $testBody -TimeoutSec 30 -UseBasicParsing
    
    Write-Host "✅ 请求成功！" -ForegroundColor Green
    Write-Host "📥 响应内容：" -ForegroundColor White
    $response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
    
    # 解析响应
    $result = $response.Content | ConvertFrom-Json
    if ($result.base_resp.status_code -eq 0) {
        Write-Host "🎉 API 调用成功！" -ForegroundColor Green
        Write-Host "💬 模型回复：" -ForegroundColor Cyan
        Write-Host $result.reply -ForegroundColor White
    } else {
        Write-Host "⚠️  API 返回错误：" -ForegroundColor Yellow
        Write-Host ("状态码：{0}" -f $result.base_resp.status_code) -ForegroundColor Red
        Write-Host ("错误信息：{0}" -f $result.base_resp.status_msg) -ForegroundColor Red
    }
    
} catch [System.Net.WebException] {
    Write-Host "🌐 网络错误：" -ForegroundColor Red
    Write-Host ("状态码：{0}" -f $_.Exception.Response.StatusCode.value__) -ForegroundColor Red
    Write-Host ("状态描述：{0}" -f $_.Exception.Response.StatusDescription) -ForegroundColor Red
    
    # 尝试读取错误响应
    try {
        $errorStream = $_.Exception.Response.GetResponseStream()
        $reader = New-Object System.IO.StreamReader($errorStream)
        $errorText = $reader.ReadToEnd()
        Write-Host "错误详情：$errorText" -ForegroundColor Yellow
    } catch {
        Write-Host "无法读取错误详情" -ForegroundColor Red
    }
    
} catch {
    Write-Host "❌ 未知错误：" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
}

Write-Host "`n🔍 网络连接状态检查..." -ForegroundColor Cyan
try {
    $pingResult = Test-NetConnection -ComputerName "api.minimax.chat" -Port 443
    if ($pingResult.TcpTestSucceeded) {
        Write-Host "✅ 网络连接正常 (延迟: {0}ms)" -f $pingResult.RoundTripTime??0 -ForegroundColor Green
    } else {
        Write-Host "❌ 网络连接失败" -ForegroundColor Red
    }
} catch {
    Write-Host "⚠️  无法检测网络状态" -ForegroundColor Yellow
}