# Feishu 配置修复指南

## 问题
App Secret 被安全机制清空，需要重新获取。

## 解决方案

### 步骤 1: 获取新的 App Secret
1. 访问飞书开放平台: https://open.feishu.cn/
2. 登录开发者账号
3. 进入"应用管理"找到应用: **OpenClaw**
4. 在"凭证与权限"页面获取新的 **App Secret**
5. 点击"重新获取"（如果需要确认身份）

### 步骤 2: 更新配置文件
运行以下命令更新配置：

```bash
npx openclaw config set channels.feishu.appSecret "你的新AppSecret"
```

### 步骤 3: 测试连接
```bash
npx openclaw channels test feishu
```

## 或者：完全重新配置飞书应用

如果应用已过期，需要：
1. 创建新应用: https://open.feishu.cn/admin/apps
2. 配置权限:
   - im:message
   - im:message:send_as_bot
   - contact:user.base:readonly
   - wiki:space
   - drive:file
3. 发布应用
4. 更新 App ID 和 Secret

## 当前配置状态
- App ID: cli_a908b9cf35f8dbc9
- App Secret: ❌ 需要重新获取
- Domain: feishu

---
生成时间: 2026-02-13 23:02
