# MiniMax API 密钥诊断报告

## 🔍 问题分析

### ❌ 密钥格式问题
**当前密钥格式：** `sk-api-SJgJvFASCso7PmfGV0yf5_0WimhWLvE2_JO7ZBQcYnAeSzdlPfmq73bE-NlQJjoIIbjPcue6YYf-ZVb5upQpteLCWNYVs89HG1ORT1V_y8oOT5LQL0PSOko`
**长度：** 126 字符
**问题：** 包含 `sk-api-` 前缀，这不是标准 MiniMax API 密钥格式

### 📊 测试结果
- ✅ 网络连接正常
- ✅ API服务器可达
- ✅ 请求到达服务器
- ❌ **密钥格式错误 (2049: invalid api key)**

## 🎯 标准格式对比

| 当前密钥 | 标准格式 |
|---------|---------|
| `sk-api-xxxxxxxxxxxxxxxxxxxxxx` | `sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |

## 🚨 诊断结论

**你的密钥前缀有问题！**

1. **错误来源：** 密钥可能来自非官方渠道或复制时包含了额外信息
2. **正确获取：** 
   - 访问 https://api.minimax.chat 登录后台
   - 在"API密钥"页面创建新密钥
   - 格式应该是：`sk-` + 48位随机字符

## 📋 正确密钥示例
```
sk-AbCdEfGhIjKlMnOpQrStUvWxYz1234567890
```
- 开头：`sk-`
- 长度：通常50-60字符
- 字符：字母+数字
- 无其他前缀或后缀

## 🔄 解决方案

### 方案1：重新获取密钥
1. 登录 MiniMax 官方控制台
2. 生成新的API密钥
3. 确保格式为 `sk-xxxxxxxx`

### 方案2：尝试去除前缀
```powershell
$cleanKey = "sk-api-SJgJvFASCso7PmfGV0yf5_0WimhWLvE2_JO7ZBQcYnAeSzdlPfmq73bE-NlQJjoIIbjPcue6YYf-ZVb5upQpteLCWNYVs89HG1ORT1V_y8oOT5LQL0PSOko"
$correctedKey = $cleanKey -replace "^sk-api-", "sk-"
# 然后使用 $correctedKey 重新测试
```

---
*诊断时间：2026-02-12 12:17*
*问题状态：密钥格式错误，需要重新获取*
*网络状态：完全正常*