# MiniMax 海外版 HTTP 500 错误诊断

## 📊 错误信息

```json
{
  "type": "error",
  "error": {
    "type": "api_error",
    "message": "Internal server error"
  },
  "request_id": "05dc90a2730ea35969d3adad208b70fc"
}
```

## 🔍 问题分析

### HTTP 500 错误含义
- **状态码**: 500 Internal Server Error
- **类型**: 服务器端错误（非客户端问题）
- **严重性**: ⚠️ 中等（服务器问题，但请求已到达）

### 可能原因

#### 1. 🎯 **海外版 vs 国内版 API 差异**
| 版本 | 端点 | 状态 |
|------|------|------|
| 国内版 | `api.minimax.chat` | ✅ 正常 |
| 海外版 | `openplatform-api-chat.xaminim.com` 或其他 | ❌ 500 错误 |

#### 2. 🔑 **密钥权限问题**
- API 密钥可能没有海外版访问权限
- 账户可能只授权了特定区域
- 密钥可能过期或被限制

#### 3. 📝 **请求格式/参数问题**
- 模型名称不兼容海外版
- 请求体格式差异
- 缺少必需参数

#### 4. 🌐 **网络/路由问题**
- 海外节点不稳定
- 请求被中间节点篡改
- CDN 节点故障

#### 5. 🔧 **服务器端问题**
- 海外服务临时维护
- 负载过高
- 服务异常

## 🛠️ 解决方案

### 方案1：使用正确的海外版 API 端点

```powershell
# 海外版可能的端点
$overseasEndpoints = @(
    "https://api.minimax.chat/v1/text/chatcompletion_pro"  # 国内版
    "https://api.minimax.com/v1/text/chatcompletion_pro"    # 海外版A
    "https://api.xaminim.com/v1/text/chatcompletion_pro"   # 海外版B
    "https://openplatform-api-chat.xaminim.com/v1/text/chatcompletion_pro"  # 海外版C
)

# 测试不同端点
foreach ($endpoint in $overseasEndpoints) {
    Write-Host "测试: $endpoint" -ForegroundColor Yellow
    try {
        $response = Invoke-WebRequest -Uri $endpoint -Method POST -Headers $headers -Body $body -TimeoutSec 10 -UseBasicParsing
        Write-Host "  状态: $($response.StatusCode)" -ForegroundColor $(if($response.StatusCode -eq 200){'Green'}else{'Red'})
    } catch {
        Write-Host "  错误: $($_.Exception.Message)" -ForegroundColor Gray
    }
}
```

### 方案2：检查密钥权限

```powershell
# 获取密钥信息
$apiKey = "sk-api-xxx"

# 测试密钥基本有效性
$testBody = @{
    model = "abab6.5"
    messages = @(@{role="user";content="test"})
    max_tokens = 10
} | ConvertTo-Json

$headers = @{
    "Content-Type" = "application/json"
    "Authorization" = "Bearer $apiKey"
}

# 测试多个端点
$endpoints = @(
    "https://api.minimax.chat/v1/text/chatcompletion_pro"
    "https://api.minimax.com/v1/text/chatcompletion_pro"
)

foreach ($endpoint in $endpoints) {
    Write-Host "`n测试端点: $endpoint" -ForegroundColor Cyan
    try {
        $response = Invoke-WebRequest -Uri $endpoint -Method POST -Headers $headers -Body $testBody -TimeoutSec 15 -UseBasicParsing
        $result = $response.Content | ConvertFrom-Json
        
        if ($result.base_resp.status_code -eq 0) {
            Write-Host "  ✅ 成功！密钥有效" -ForegroundColor Green
            Write-Host "  回复: $($result.reply)" -ForegroundColor White
        } else {
            Write-Host "  ⚠️ 错误$($result.base_resp.status_code): $($result.base_resp.status_msg)" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "  ❌ 网络错误: $($_.Exception.Message)" -ForegroundColor Red
    }
}
```

### 方案3：使用标准化的请求格式

```powershell
# 确保使用标准化的请求格式
$requestBody = @{
    model = "abab6.5-chat"  # 尝试不同的模型名称
    messages = @(
        @{
            role = "user"
            content = "Hello, please respond in English"
        }
    )
    temperature = 0.7
    max_tokens = 100
    stream = $false
} | ConvertTo-Json -Depth 10

$headers = @{
    "Content-Type" = "application/json; charset=utf-8"
    "Accept" = "application/json"
    "Authorization" = "Bearer $env:MINIMAX_API_KEY"
}

Write-Host "📤 发送请求..." -ForegroundColor Cyan
Write-Host "端点: https://api.minimax.chat/v1/text/chatcompletion_pro" -ForegroundColor Gray
Write-Host "密钥: $($env:MINIMAX_API_KEY.Substring(0, 10))..." -ForegroundColor Gray

$response = Invoke-WebRequest -Uri "https://api.minimax.chat/v1/text/chatcompletion_pro" -Method POST -Headers $headers -Body $requestBody -TimeoutSec 30 -UseBasicParsing
Write-Host "📥 响应: $($response.StatusCode)" -ForegroundColor White
$response.Content
```

### 方案4：备用方案 - 使用国内版

```powershell
# 如果海外版持续 500 错误，优先使用国内版
$preferredEndpoint = "https://api.minimax.chat/v1/text/chatcompletion_pro"

Write-Host "🌐 使用首选端点: $preferredEndpoint" -ForegroundColor Cyan

# 测试国内版
$testResult = Invoke-WebRequest -Uri $preferredEndpoint -Method POST -Headers $headers -Body $requestBody -TimeoutSec 20 -UseBasicParsing
$result = $testResult.Content | ConvertFrom-Json

if ($result.base_resp.status_code -eq 0) {
    Write-Host "✅ 国内版正常工作" -ForegroundColor Green
    Write-Host "回复: $($result.reply)" -ForegroundColor White
} else {
    Write-Host "⚠️ 国内版也异常: $($result.base_resp.status_msg)" -ForegroundColor Yellow
    Write-Host "建议: 联系 MiniMax 官方支持" -ForegroundColor Cyan
}
```

## 🎯 诊断步骤

### Step 1: 确认错误复现
```powershell
# 记录完整的错误信息
$error = @{
    time = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    request_id = "05dc90a2730ea35969d3adad208b70fc"
    status = 500
    message = "Internal server error"
}
$error | ConvertTo-Json | Out-File "minimax_500_error.log" -Append
```

### Step 2: 测试多个端点
```powershell
# 测试 3-5 个不同的 API 端点
$testEndpoints = @(
    "https://api.minimax.chat/v1/text/chatcompletion_pro"
    "https://api.minimax.chat/v1/text/chatcompletion_v1"
    "https://api.minimax.com/v1/text/chatcompletion_pro"
)

# 记录每个端点的响应
```

### Step 3: 检查密钥状态
```powershell
# 确认密钥是否有效
$keyStatus = Invoke-WebRequest -Uri "https://api.minimax.chat/v1/user/info" -Headers $headers -TimeoutSec 10 -UseBasicParsing
$keyStatus.Content
```

### Step 4: 联系官方支持
- 提供 `request_id`: `05dc90a2730ea35969d3adad208b70fc`
- 提供完整的请求/响应日志
- 说明使用的 API 端点

## 📋 错误对比

| 错误码 | 含义 | 解决 |
|--------|------|------|
| 401 | 未授权 | 检查 API 密钥 |
| 403 | 禁止访问 | 检查账户权限 |
| 404 | 未找到 | 检查端点 URL |
| 429 | 请求过多 | 降低请求频率 |
| 500 | 服务器错误 | 联系官方支持 |
| 502/503/504 | 服务不可用 | 等待恢复 |

## 💡 临时解决方案

### 1. **重试请求**
```powershell
for ($i = 1; $i -le 3; $i++) {
    Write-Host "尝试 $i/3..." -ForegroundColor Yellow
    try {
        $response = Invoke-WebRequest -Uri $endpoint -Method POST -Headers $headers -Body $body -TimeoutSec 30
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ 重试成功！" -ForegroundColor Green
            break
        }
    } catch {
        Start-Sleep -Seconds 5
    }
}
```

### 2. **切换端点**
```powershell
# 如果海外版失败，尝试国内版
$fallbackEndpoint = "https://api.minimax.chat/v1/text/chatcompletion_pro"
```

### 3. **等待恢复**
如果是服务器端问题，通常会在 10-30 分钟内恢复。

## 🔧 预防措施

1. **实现重试机制**
2. **配置多个备用端点**
3. **监控 API 健康状态**
4. **保留错误日志**

## 📞 联系官方

如果问题持续：
1. 访问: https://api.minimax.chat
2. 提交工单
3. 提供 `request_id`: `05dc90a2730ea35969d3adad208b70fc`
4. 说明环境和复现步骤

---
*诊断时间: 2026-02-12*
*错误类型: 服务器端错误 (500)*
*状态: 等待官方修复或切换端点*
