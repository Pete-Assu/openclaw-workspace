# SkillMint 简化设置指南

## 你需要准备的东西

### 1. Circle API Key（必需）
```
访问: https://developers.circle.com/
注册账号
创建 API Key (testnet 模式)
```

### 2. GitHub 账号（必需）
```
确保 GitHub 账号已登录
需要上传技能到 GitHub
```

---

## 步骤 1：安装 SkillMint

```bash
# 在 PowerShell 中执行
clawhub install skillmint
cd skillmint
npm install
```

## 步骤 2：设置 Circle 钱包

```bash
# 设置 API Key（用你的 Circle API Key）
circle-wallet setup --api-key YOUR_CIRCLE_API_KEY
```

## 步骤 3：注册你的技能

```bash
# 注册 system-monitor（$0.01/调用）
node skillmint.js register system-monitor 0.01

# 注册 quick-commands（$0.005/调用）
node skillmint.js register quick-commands 0.005

# 查看已注册的技能
node skillmint.js skills

# 查看收入
node skillmint.js earnings
```

---

## 你需要做的

| 步骤 | 操作 | 预计时间 |
|------|------|---------|
| 1 | 获取 Circle API Key | 2分钟 |
| 2 | 安装 SkillMint | 1分钟 |
| 3 | 设置钱包 | 1分钟 |
| 4 | 注册技能 | 1分钟 |

**总计：约 5 分钟**

---

## 下一步

1. **先获取 Circle API Key**
   - 打开：https://developers.circle.com/
   - 注册账号
   - 创建 API Key（选 testnet 模式）

2. **告诉我 API Key**
   - 我帮你执行命令
   - 你只需要复制粘贴

---

**先去获取 Circle API Key？** 完成后告诉我！🎯
