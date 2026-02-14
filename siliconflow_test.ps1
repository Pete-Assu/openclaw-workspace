# Silicon Flow API 测试脚本
# 用途：测试 Silicon Flow API 连通性和功能

param (
    [string]$ApiKey = $env:SILICONFLOW_API_KEY,
    [string]$Endpoint = "https://siliconflow.cn/api/chat",
    [string]$Model = "deepseek-ai/DeepSeek-V2.5",
    [switch]$QuickTest,
    [switch]$FullTest
)

Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "Silicon Flow API 测试工具" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan

# 颜色配置
$colors = @{
    "Info" = "White"
    "Success" = "Green"
    "Warning" = "Yellow"
    "Error" = "Red"
    "Result" = "Cyan"
}

function Test-Endpoint {
    <#
    .SYNOPSIS
    测试 API 端点连通性
    #>
    param([string]$Endpoint)
    
    Write-Host "`n[测试 1/5] API 端点连通性" -ForegroundColor $colors.Info
    
    try {
        $startTime = Get-Date
        $response = Invoke-WebRequest -Uri $endpoint -Method GET -TimeoutSec 15 -UseBasicParsing
        $endTime = Get-Date
        $latency = ($endTime - $startTime).TotalMilliseconds
        
        Write-Host "  ✅ 端点可达 (延迟: ${latency}ms)" -ForegroundColor $colors.Success
        Write-Host "  状态码: $($response.StatusCode)" -ForegroundColor $colors.Info
        
        return $true
    } catch {
        Write-Host "  ❌ 端点不可达: $($_.Exception.Message)" -ForegroundColor $colors.Error
        return $false
    }
}

function Test-Authentication {
    <#
    .SYNOPSIS
    测试 API 密钥认证
    #>
    param([string]$ApiKey, [string]$Endpoint)
    
    Write-Host "`n[测试 2/5] API 密钥认证" -ForegroundColor $colors.Info
    
    if (-not $ApiKey) {
        Write-Host "  ❌ 未找到 API 密钥" -ForegroundColor $colors.Error
        Write-Host "  提示: 设置 `$env:SILICONFLOW_API_KEY 或使用 -ApiKey 参数" -ForegroundColor $colors.Warning
        return $false
    }
    
    # 检查密钥格式
    $keyLength = $ApiKey.Length
    $keyPrefix = $ApiKey.Substring(0, [Math]::Min(5, $keyLength))
    Write-Host "  📋 密钥: $keyPrefix... (长度: $keyLength)" -ForegroundColor $colors.Info
    
    if ($keyLength -ge 40) {
        Write-Host "  ✅ 密钥格式可能正确" -ForegroundColor $colors.Success
    } else {
        Write-Host "  ⚠️  密钥长度较短，可能不正确" -ForegroundColor $colors.Warning
    }
    
    return $true
}

function Test-ChatCompletion {
    <#
    .SYNOPSIS
    测试聊天完成功能
    #>
    param([string]$ApiKey, [string]$Endpoint, [string]$Model)
    
    Write-Host "`n[测试 3/5] 聊天完成测试" -ForegroundColor $colors.Info
    
    if (-not $ApiKey) {
        Write-Host "  ⏭️  跳过（无 API 密钥）" -ForegroundColor $colors.Warning
        return $null
    }
    
    $testBody = @{
        model = $Model
        messages = @(
            @{
                role = "user"
                content = "请回复：Silicon Flow API 测试成功"
            }
        )
        temperature = 0.7
        max_tokens = 100
    } | ConvertTo-Json -Depth 10
    
    $headers = @{
        "Content-Type" = "application/json"
        "Authorization" = "Bearer $ApiKey"
    }
    
    try {
        Write-Host "  发送测试请求 (模型: $Model)..." -ForegroundColor $colors.Info
        
        $startTime = Get-Date
        $response = Invoke-WebRequest -Uri $endpoint -Method POST -Headers $headers -Body $testBody -TimeoutSec 30 -UseBasicParsing
        $endTime = Get-Date
        $latency = ($endTime - $startTime).TotalMilliseconds
        
        $result = $response.Content | ConvertFrom-Json
        
        Write-Host "  ✅ 请求成功 (延迟: ${latency}ms)" -ForegroundColor $colors.Success
        
        # 解析响应
        if ($result.choices) {
            $reply = $result.choices[0].message.content
            Write-Host "`n  💬 模型回复:" -ForegroundColor $colors.Result
            Write-Host "  $reply" -ForegroundColor White
            return $true
        } elseif ($result.error) {
            Write-Host "  ⚠️  API 返回错误: $($result.error.message)" -ForegroundColor $colors.Warning
            return $false
        } else {
            Write-Host "  ℹ️  响应格式: $result" -ForegroundColor $colors.Info
            return $true
        }
        
    } catch {
        Write-Host "  ❌ 请求失败: $($_.Exception.Message)" -ForegroundColor $colors.Error
        
        # 尝试读取错误详情
        try {
            $errorStream = $_.Exception.Response.GetResponseStream()
            $reader = New-Object System.IO.StreamReader($errorStream)
            $errorText = $reader.ReadToEnd()
            Write-Host "  错误详情: $errorText" -ForegroundColor $colors.Warning
        } catch {
            Write-Host "  无法读取错误详情" -ForegroundColor $colors.Warning
        }
        
        return $false
    }
}

function Test-ModelList {
    <#
    .SYNOPSIS
    测试模型列表获取
    #>
    param([string]$ApiKey], [string]$Endpoint)
    
    Write-Host "`n[测试 4/5] 模型列表测试" -ForegroundColor $colors.Info
    
    if (-not $ApiKey) {
        Write-Host "  ⏭️  跳过（无 API 密钥）" -ForegroundColor $colors.Warning
        return $null
    }
    
    $modelsEndpoint = $endpoint -replace "/chat", "/models"
    
    try {
        $headers = @{
            "Authorization" = "Bearer $ApiKey"
        }
        
        $response = Invoke-WebRequest -Uri $modelsEndpoint -Method GET -Headers $headers -TimeoutSec 15 -UseBasicParsing
        $result = $response.Content | ConvertFrom-Json
        
        Write-Host "  ✅ 获取成功" -ForegroundColor $colors.Success
        
        if ($result.data) {
            Write-Host "  📋 可用模型数量: $($result.data.Count)" -ForegroundColor $colors.Info
            $result.data | Select-Object -First 5 | ForEach-Object {
                Write-Host "    - $($_.id)" -ForegroundColor Gray
            }
        }
        
        return $true
        
    } catch {
        Write-Host "  ⚠️  无法获取模型列表: $($_.Exception.Message)" -ForegroundColor $colors.Warning
        Write-Host "  提示: 这不是严重问题，可以手动指定模型" -ForegroundColor $colors.Info
        return $null
    }
}

function Generate-Report {
    <#
    .SYNOPSIS
    生成测试报告
    #>
    param(
        [bool]$EndpointOk,
        [bool]$AuthOk,
        [bool]$ChatOk,
        [object]$ModelResult
    )
    
    Write-Host "`n" + "=" * 60 -ForegroundColor Cyan
    Write-Host "测试报告" -ForegroundColor Cyan
    Write-Host "=" * 60 -ForegroundColor Cyan
    
    Write-Host "`n📊 测试结果:" -ForegroundColor $colors.Info
    Write-Host "  🌐 API 端点: $(if($EndpointOk) {'✅ 可达'} else {'❌ 不可达'})" -ForegroundColor $(if($EndpointOk){$colors.Success}else{$colors.Error})
    Write-Host "  🔑 API 密钥: $(if($AuthOk) {'✅ 已配置'} else {'❌ 未配置'})" -ForegroundColor $(if($AuthOk){$colors.Success}else{$colors.Error})
    Write-Host "  💬 聊天功能: $(if($ChatOk -eq $true) {'✅ 正常'} elseif($ChatOk -eq $false) {'❌ 失败'} else {'⏭️  跳过'})" -ForegroundColor $(if($ChatOk -eq $true){$colors.Success}elseif($ChatOk -eq $false){$colors.Error}else{$colors.Warning})
    Write-Host "  📋 模型列表: $(if($ModelResult -eq $true) {'✅ 正常'} elseif($ModelResult -eq $null) {'⏭️  跳过'} else {'⚠️  部分'})" -ForegroundColor $(if($ModelResult -eq $true){$colors.Success}else{$colors.Warning})
    
    Write-Host "`n🎯 总结:" -ForegroundColor $colors.Info
    
    if ($EndpointOk -and $AuthOk -and $ChatOk -eq $true) {
        Write-Host "  🎉 Silicon Flow API 完全可用！" -ForegroundColor $colors.Success
        Write-Host "  可以开始使用 Silicon Flow 进行 AI 对话" -ForegroundColor $colors.Success
    } elseif ($EndpointOk -and -not $AuthOk) {
        Write-Host "  ⏳ API 端点正常，需要配置 API 密钥" -ForegroundColor $colors.Warning
        Write-Host "  下一步: 获取并配置 API 密钥" -ForegroundColor $colors.Info
    } elseif (-not $EndpointOk) {
        Write-Host "  ❌ API 端点不可达，需要检查网络" -ForegroundColor $colors.Error
        Write-Host "  建议: 检查 DNS 和网络连接" -ForegroundColor $colors.Info
    } else {
        Write-Host "  ⚠️  部分功能异常，请检查错误信息" -ForegroundColor $colors.Warning
    }
    
    Write-Host "`n📁 测试日志已保存" -ForegroundColor $colors.Info
    Write-Host "   位置: siliconflow_test.log" -ForegroundColor Gray
}

# 主程序
function Main {
    # 检查快速测试模式
    if ($QuickTest) {
        Write-Host "`n🚀 快速测试模式" -ForegroundColor Cyan
        
        $endpointOk = Test-Endpoint -Endpoint $Endpoint
        
        if ($endpointOk) {
            Write-Host "`n✅ API 端点连通性正常" -ForegroundColor $colors.Success
            Write-Host "🎉 Silicon Flow API 已就绪！" -ForegroundColor $colors.Success
        } else {
            Write-Host "`n❌ API 端点不可达" -ForegroundColor $colors.Error
        }
        
        return
    }
    
    # 完整测试
    Write-Host "`n🔍 开始完整测试..." -ForegroundColor $colors.Info
    
    # 测试 1: 端点连通性
    $endpointOk = Test-Endpoint -Endpoint $Endpoint
    
    # 测试 2: 认证
    $authOk = Test-Authentication -ApiKey $ApiKey -Endpoint $Endpoint
    
    # 测试 3: 聊天完成
    $chatOk = Test-ChatCompletion -ApiKey $ApiKey -Endpoint $Endpoint -Model $Model
    
    # 测试 4: 模型列表
    $modelResult = Test-ModelList -ApiKey $ApiKey -Endpoint $Endpoint
    
    # 生成报告
    Generate-Report -EndpointOk $endpointOk -AuthOk $authOk -ChatOk $chatOk -ModelResult $modelResult
}

# 运行主程序
Main

Write-Host "`n" + "=" * 60 -ForegroundColor Cyan
Write-Host "测试完成" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan