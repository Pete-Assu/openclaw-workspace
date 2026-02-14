# Silicon Flow API 快速使用
$env:SILICONFLOW_API_KEY = "sk-asvjcddwvpqdacgvfsxkoyeucbegqlmidnpqpthvrzmmdiqw"

# 对话示例
\ = @{
    model = "deepseek-ai/DeepSeek-V2.5"
    messages = @(@{role="user";content="你好"})
    temperature = 0.7
    max_tokens = 500
} | ConvertTo-Json

\ = @{
    "Content-Type" = "application/json"
    "Authorization" = "Bearer $env:SILICONFLOW_API_KEY"
}

Invoke-WebRequest -Uri "https://api.siliconflow.cn/v1/chat/completions" -Method POST -Headers \ -Body \ -UseBasicParsing
