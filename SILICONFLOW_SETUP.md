# Silicon Flow API 配置指南

## 📊 API 状态

### ✅ 可用端点
- **基础端点**: `https://siliconflow.cn/api/chat`
- **状态**: 返回 200 (需要认证)

### 🔍 测试命令
```powershell
# 测试基础连通性
Invoke-WebRequest -Uri "https://siliconflow.cn/api/chat" -Method GET -TimeoutSec 10

# 应该返回：需要认证或错误（说明端点存在）
```

## 🚀 快速配置

### 1. 设置 API 密钥
```powershell
# 方法1：临时设置（当前会话有效）
$env:SILICONFLOW_API_KEY = "your-api-key-here"

# 方法2：永久设置（系统环境变量）
[Environment]::SetEnvironmentVariable(
    "SILICONFLOW_API_KEY", 
    "your-api-key-here", 
    "User"
)

# 方法3：保存到配置文件
$config = @{
    api_key = "your-api-key-here"
    endpoint = "https://siliconflow.cn/api/chat"
    model = "deepseek-ai/DeepSeek-V2.5"
} | ConvertTo-Json

$config | Out-File "siliconflow_config.json" -Encoding UTF8
```

### 2. 测试 API 调用
```powershell
# 完整的 API 测试脚本
$apiKey = $env:SILICONFLOW_API_KEY
$endpoint = "https://siliconflow.cn/api/chat"

$body = @{
    model = "deepseek-ai/DeepSeek-V2.5"
    messages = @(
        @{
            role = "user"
            content = "你好，请介绍一下 Silicon Flow"
        }
    )
    temperature = 0.7
    max_tokens = 500
} | ConvertTo-Json -Depth 10

$headers = @{
    "Content-Type" = "application/json"
    "Authorization" = "Bearer $apiKey"
}

Write-Host "发送请求到 Silicon Flow..." -ForegroundColor Cyan
$response = Invoke-WebRequest -Uri $endpoint -Method POST -Headers $headers -Body $body -TimeoutSec 30 -UseBasicParsing
Write-Host "响应状态: $($response.StatusCode)" -ForegroundColor White
$response.Content
```

## 📋 可用模型

### 对话模型
- `deepseek-ai/DeepSeek-V2.5`
- `deepseek-ai/DeepSeek-V2`
- `Qwen/Qwen2.5-72B-Instruct`
- `01-ai/Yi-1.5-34B-Chat`
- `mistralai/Mistral-7B-Instruct-v0.2`

###  embedding 模型
- `BAAI/bge-large-zh-v1.5`
- `BAAI/bge-m3`

### 代码模型
- `bigcode/starcoder2-15b`

## 🎯 OpenClaw 集成

### 1. 配置 OpenClaw 使用 Silicon Flow
```powershell
# 在 OpenClaw 配置中添加 Silicon Flow 提供商
# 文件位置: ~/.openclaw/config.json

{
  "providers": {
    "siliconflow": {
      "api_key": "$env:SILICONFLOW_API_KEY",
      "endpoint": "https://siliconflow.cn/api/chat",
      "models": {
        "default": "deepseek-ai/DeepSeek-V2.5",
        "chat": "deepseek-ai/DeepSeek-V2.5",
        "coding": "bigcode/starcoder2-15b"
      }
    }
  }
}
```

### 2. 设置默认模型
```powershell
# 将 Silicon Flow 设置为默认提供商
openclaw config set provider default siliconflow
```

## 💻 完整使用示例

### PowerShell 函数
```powershell
function Invoke-SiliconFlowChat {
    <#
    .SYNOPSIS
    调用 Silicon Flow API 进行对话
    #>
    param(
        [Parameter(Mandatory=$true)]
        [string]$Message,
        
        [Parameter(Mandatory=$false)]
        [string]$Model = "deepseek-ai/DeepSeek-V2.5",
        
        [Parameter(Mandatory=$false)]
        [double]$Temperature = 0.7,
        
        [Parameter(Mandatory=$false)]
        [int]$MaxTokens = 1000
    )
    
    # 获取 API 密钥
    $apiKey = $env:SILICONFLOW_API_KEY
    if (-not $apiKey) {
        Write-Error "请设置 `$env:SILICONFLOW_API_KEY"
        return
    }
    
    # 构建请求
    $endpoint = "https://siliconflow.cn/api/chat"
    $body = @{
        model = $Model
        messages = @(@{role="user";content=$Message})
        temperature = $Temperature
        max_tokens = $MaxTokens
    } | ConvertTo-Json -Depth 10
    
    $headers = @{
        "Content-Type" = "application/json"
        "Authorization" = "Bearer $apiKey"
    }
    
    # 发送请求
    $response = Invoke-WebRequest -Uri $endpoint -Method POST -Headers $headers -Body $body -TimeoutSec 30 -UseBasicParsing
    
    # 解析响应
    $result = $response.Content | ConvertFrom-Json
    
    if ($result.choices) {
        return $result.choices[0].message.content
    } else {
        return $response.Content
    }
}

# 使用示例
$reply = Invoke-SiliconFlowChat -Message "你好，请介绍一下 Silicon Flow" -Model "deepseek-ai/DeepSeek-V2.5"
Write-Host $reply
```

## 🔧 故障排除

### 问题1：无法连接
```powershell
# 检查网络
Test-NetConnection siliconflow.cn -Port 443

# 检查 DNS
nslookup siliconflow.cn

# 尝试 IP 访问（如果 DNS 有问题）
ping siliconflow.cn
```

### 问题2：认证失败
```powershell
# 检查 API 密钥
Write-Host "API 密钥: $($env:SILICONFLOW_API_KEY.Substring(0, 10))..." -ForegroundColor Yellow

# 确认密钥格式（通常以 sk- 开头）
if ($env:SILICONFLOW_API_KEY -match '^sk-') {
    Write-Host "✅ 密钥格式正确" -ForegroundColor Green
} else {
    Write-Host "⚠️ 密钥格式可能不正确" -ForegroundColor Yellow
}
```

### 问题3：模型不存在
```powershell
# 获取可用模型列表
$models = Invoke-WebRequest -Uri "https://siliconflow.cn/api/models" -Headers $headers -UseBasicParsing
Write-Host "可用模型: $models" -ForegroundColor White
```

## 📊 性能测试

### 延迟测试
```powershell
Measure-Command {
    Invoke-SiliconFlowChat -Message "测试" -MaxTokens 10
}
```

### 并发测试
```powershell
# 测试并发请求
1..5 | ForEach-Object {
    $job = Start-Job -ScriptBlock {
        Invoke-SiliconFlowChat -Message "测试 $_" -MaxTokens 50
    }
}

Get-Job | Wait-Job | Receive-Job
```

## 💰 定价信息

（请访问 https://siliconflow.cn 官网获取最新定价）

## 📞 官方资源

- **官网**: https://siliconflow.cn
- **API 文档**: https://siliconflow.cn/docs
- **状态页**: https://siliconflow.cn/status
- **支持**: https://siliconflow.cn/support

## 🎯 后续步骤

1. **获取 API 密钥**
   - 访问 https://siliconflow.cn
   - 注册账户
   - 创建 API 密钥

2. **配置环境变量**
   ```powershell
   $env:SILICONFLOW_API_KEY = "sk-xxx"
   ```

3. **运行测试**
   ```powershell
   .\siliconflow_test.ps1
   ```

4. **集成到 OpenClaw**
   ```powershell
   # 在配置中添加 Silicon Flow 提供商
   ```

---
*创建时间: 2026-02-12*
*版本: 1.0*
