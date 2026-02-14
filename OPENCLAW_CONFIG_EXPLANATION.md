# OpenClaw 配置文件详解 - openclaw.json

## 📋 概述

**文件名**: `openclaw.json`
**位置**: `C:\Users\殇\.openclaw\openclaw.json`
**作用**: OpenClaw 的主配置文件，控制所有功能和行为

## 🏗️ 配置结构

```
openclaw.json
├── meta                    # 元数据
├── wizard                  # 向导配置
├── update                  # 更新设置
├── auth                    # 认证配置
├── models                  # 模型配置 ⭐ 重要
├── agents                  # 代理配置
├── tools                   # 工具配置
├── messages                # 消息配置
├── commands                # 命令配置
├── hooks                   # 钩子配置
├── web                     # Web 配置
├── channels               # 频道配置
├── gateway                 # 网关配置
├── skills                  # 技能配置
└── plugins                 # 插件配置
```

## 📖 详细说明

### 1. Meta（元数据）
```json
"meta": {
  "lastTouchedVersion": "2026.2.9",      // 最后修改版本
  "lastTouchedAt": "2026-02-12T04:59:00.145Z"  // 最后修改时间
}
```
**作用**: 跟踪配置的修改历史

### 2. Wizard（向导配置）
```json
"wizard": {
  "lastRunAt": "2026-02-11T14:11:00.015Z",    // 上次运行时间
  "lastRunVersion": "2026.2.9",              // 上次版本
  "lastRunCommand": "configure",              // 上次命令
  "lastRunMode": "local"                       // 运行模式
}
```
**作用**: 记录配置向导的运行状态

### 3. Update（更新配置）
```json
"update": {
  "channel": "stable",      // 更新通道: stable/beta/alpha
  "checkOnStart": true      // 启动时检查更新
}
```
**作用**: 控制 OpenClaw 的自动更新

### 4. Auth（认证配置）⭐
```json
"auth": {
  "profiles": {
    "qwen-portal:default": {
      "provider": "qwen-portal",
      "mode": "oauth"
    },
    "minimax-portal:default": {
      "provider": "minimax-portal",
      "mode": "oauth"
    },
    "minimax:default": {
      "provider": "minimax",
      "mode": "api_key"
    }
  }
}
```
**作用**: 管理各提供商的身份认证

### 5. Models（模型配置）⭐⭐⭐
```json
"models": {
  "mode": "merge",  // 合并模式
  "providers": {
    "minimax": {
      "baseUrl": "https://api.minimax.io/anthropic",
      "apiKey": "minimax-oauth",
      "api": "anthropic-messages",
      "models": [
        {
          "id": "MiniMax-M2.1",
          "name": "MiniMax M2.1",
          "reasoning": false,
          "input": ["text"],
          "cost": {
            "input": 15,
            "output": 60,
            "cacheRead": 2,
            "cacheWrite": 10
          },
          "contextWindow": 200000,
          "maxTokens": 8192
        }
      ]
    },
    "ollama": { ... },
    "qwen-portal": { ... },
    "minimax-portal": { ... }
  }
}
```
**作用**: 配置所有可用的 AI 模型提供商

### 6. Agents（代理配置）
```json
"agents": {
  "defaults": {
    "model": {
      "fallbacks": [
        "minimax-portal/MiniMax-M2.1",
        "minimax-portal/MiniMax-M2.1-lightning",
        "qwen-portal/coder-model",
        "qwen-portal/vision-model"
      ],
      "primary": "minimax-portal/MiniMax-M2.1"
    },
    "models": {
      "minimax/MiniMax-M2.1": { "alias": "Minimax" },
      "qwen-portal/coder-model": { "alias": "qwen" },
      "minimax-portal/MiniMax-M2.1": { "alias": "minimax-m2.1" },
      "minimax-portal/MiniMax-M2.1-lightning": { "alias": "minimax-m2.1-lightning" }
    },
    "workspace": "C:\\Users\\殇\\.openclaw\\workspace",
    "compaction": { "mode": "safeguard" },
    "maxConcurrent": 4,
    "subagents": { "maxConcurrent": 8 }
  }
}
```
**作用**: 设置默认代理行为

### 7. Tools（工具配置）
```json
"tools": {
  "web": {
    "search": {
      "enabled": true,
      "provider": "brave",
      "apiKey": "",
      "maxResults": 5,
      "timeoutSeconds": 30
    }
  },
  "agentToAgent": { "enabled": false },
  "elevated": { "enabled": true }
}
```
**作用**: 配置各种工具的行为

### 8. Gateway（网关配置）
```json
"gateway": {
  "port": 18789,
  "mode": "local",
  "bind": "loopback",
  "auth": {
    "mode": "token",
    "token": "88505db640a41bcf8916ae8fc5c80ba4b4077454bd7a7cd7"
  },
  "tailscale": {
    "mode": "off",
    "resetOnExit": false
  }
}
```
**作用**: 配置本地网关服务

## 🔧 添加新模型提供商的步骤

### Silicon Flow 集成示例

需要在以下位置添加：

1. **`models.providers`**
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
         "cost": { "input": 0.5, "output": 1.0 },
         "contextWindow": 128000,
         "maxTokens": 8192
       }
     ]
   }
   ```

2. **`auth.profiles`**
   ```json
   "siliconflow:default": {
     "provider": "siliconflow",
     "mode": "api_key"
   }
   ```

3. **`agents.defaults.model.fallbacks`**
   ```json
   "siliconflow/deepseek-ai/DeepSeek-V2.5"
   ```

4. **`agents.defaults.models`**
   ```json
   "siliconflow/deepseek-ai/DeepSeek-V2.5": {
     "alias": "deepseek"
   }
   ```

## 📊 常用配置操作

### 查看当前模型
```powershell
Get-Content openclaw.json | ConvertFrom-Json | Select-Object -Expand models -Expand providers | Select-Object -ExpandProperty Keys
```

### 检查特定配置
```powershell
(Get-Content openclaw.json | ConvertFrom-Json).agents.defaults.model.fallbacks
```

### 重置为默认值
```powershell
# 删除配置文件，OpenClaw 会自动重新生成
Remove-Item openclaw.json
```

## ⚠️ 注意事项

1. **备份**: 修改前先备份
2. **JSON 格式**: 必须严格遵守 JSON 语法
3. **编码**: 使用 UTF-8 编码
4. **重启**: 修改后需要重启 OpenClaw

## 🎯 下一步

修改 `openclaw.json` 后：
1. 保存文件
2. 重启 OpenClaw Gateway
3. 测试新配置

---
*文档创建时间: 2026-02-12*
*版本: 1.0*
