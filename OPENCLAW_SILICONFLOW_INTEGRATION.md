# Silicon Flow OpenClaw 配置片段

## 需要添加到 openclaw.json 的内容

### 1. 在 `models.providers` 下添加：
```json
"siliconflow": {
  "baseUrl": "https://api.siliconflow.cn/v1",
  "apiKey": "siliconflow-api-key",
  "api": "openai-completions",
  "models": [
    {
      "id": "deepseek-ai/DeepSeek-V2.5",
      "name": "DeepSeek V2.5",
      "reasoning": false,
      "input": ["text"],
      "cost": {
        "input": 0.5,
        "output": 1.0,
        "cacheRead": 0.1,
        "cacheWrite": 0.2
      },
      "contextWindow": 128000,
      "maxTokens": 8192
    }
  ]
}
```

### 2. 在 `auth.profiles` 下添加：
```json
"siliconflow:default": {
  "provider": "siliconflow",
  "mode": "api_key"
}
```

### 3. 在 `agents.defaults.model.fallbacks` 数组中添加：
```json
"siliconflow/deepseek-ai/DeepSeek-V2.5"
```

### 4. 在 `agents.defaults.models` 下添加：
```json
"siliconflow/deepseek-ai/DeepSeek-V2.5": {
  "alias": "deepseek"
}
```

## 使用方法

### 方法1：手动编辑
1. 打开 `C:\Users\殇\.openclaw\openclaw.json`
2. 按上述位置添加配置
3. 保存文件
4. 重启 OpenClaw

### 方法2：使用配置合并工具
```powershell
# 运行配置合并脚本
python merge_config.py
```

## 集成后的功能

- **可用模型**: `deepseek-ai/DeepSeek-V2.5`
- **使用命令**: `model:siliconflow/deepseek-ai/DeepSeek-V2.5`
- **别名**: `deepseek`
- **认证方式**: API Key
- **API 端点**: `https://api.siliconflow.cn/v1`

## 下一步

配置完成后，需要：
1. 设置环境变量：`$env:SILICONFLOW_API_KEY = "你的密钥"`
2. 重启 OpenClaw Gateway
3. 测试模型调用

---
*创建时间: 2026-02-12*
*版本: 1.0*
