# OpenClaw 自动更新配置

## 📋 概述

本配置实现 OpenClaw 启动时自动检查版本并更新。

## 🚀 功能特性

### 1. 版本检查
- 自动获取当前版本
- 自动检查 npm 最新版本
- 版本比较和更新判断

### 2. 自动更新
- 智能更新（仅新版本时更新）
- 强制更新（`-ForceUpdate`）
- npm 缓存清理

### 3. 重启机制
- 手动确认重启
- 服务状态检查
- 平滑重启

## 📁 文件说明

### auto_update.ps1
主自动更新脚本，支持以下参数：

| 参数 | 说明 | 示例 |
|------|------|------|
| 无参数 | 完整更新流程 | `.\auto_update.ps1` |
| `-CheckOnly` | 仅检查版本 | `.\auto_update.ps1 -CheckOnly` |
| `-ForceUpdate` | 强制更新 | `.\auto_update.ps1 -ForceUpdate` |
| `-NoRestart` | 不重启 | `.\auto_update.ps1 -NoRestart` |

### startup_config.json
启动配置，定义更新策略：

```json
{
  "versionCheck": true,
  "autoUpdate": true,
  "forceUpdate": false,
  "cacheCleanup": true,
  "restartOnUpdate": true,
  "notification": true
}
```

## 🎯 使用方法

### 方式1：手动运行
```powershell
# 仅检查版本
.\auto_update.ps1 -CheckOnly

# 完整更新
.\auto_update.ps1

# 强制更新
.\auto_update.ps1 -ForceUpdate
```

### 方式2：集成到启动
更新 `auto_start.py` 添加自动更新调用：

```python
# 在 auto_start.py 中添加
import subprocess
import sys

def auto_update():
    """自动更新检查"""
    try:
        result = subprocess.run(
            ['powershell', '-File', 'auto_update.ps1', '-CheckOnly'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✅ 版本检查完成")
            return True
        else:
            print("⚠️ 版本检查需要更新")
            return False
    except Exception as e:
        print(f"❌ 更新检查失败: {e}")
        return False

# 在主流程中调用
if __name__ == "__main__":
    print("🚀 OpenClaw 启动中...")
    auto_update()
    # 继续其他启动流程...
```

### 方式3：计划任务
创建 Windows 计划任务，开机自动运行：

```powershell
# 创建计划任务
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-File 'C:\Users\殇\.openclaw\workspace\auto_update.ps1'"
$trigger = New-ScheduledTaskTrigger -AtStartup
Register-ScheduledTask -TaskName "OpenClaw Auto Update" -Action $action -Trigger $trigger -RunLevel Highest
```

## 📊 执行流程

```
1. 检查当前 OpenClaw 版本
      ↓
2. 连接 NPM 注册表
      ↓
3. 获取最新版本信息
      ↓
4. 版本比较
      ↓
    ┌───────────────┐
    │ 最新版本?     │
    └───────────────┘
      是    │   否
        ↓       ↓
    ✅ 完成   ⬇️
               执行 npm update
               ⬇️
            清理缓存
               ⬇️
            提示重启
```

## 🎨 通知示例

### 终端输出
```
🚀 OpenClaw 自动更新检查...
时间: 2026-02-12 13:10

📦 当前版本检查...
  当前版本: 2026.2.9

🌐 检查网络...
  NPM Registry: https://registry.npmjs.org/
  ✅ NPM 注册表可达

📥 检查最新版本...
  最新版本: 2026.2.10

  ⚠️  发现新版本可用

⬇️  开始更新...
  运行: npm update -g openclaw
  ✅ 更新完成

🧹 清理 npm 缓存...
  ✅ 缓存已清理

🔄 检查是否需要重启...
  状态: 等待用户确认重启

提示: 运行 'openclaw gateway restart' 重启服务

✅ OpenClaw 自动更新检查完成！
```

## 🔧 高级配置

### 静默模式
```powershell
.\auto_update.ps1 -CheckOnly -NoRestart
```

### 仅更新 OpenClaw
```powershell
npm update -g openclaw
```

### 自定义 NPM 源
```powershell
npm config set registry https://registry.npmmirror.com
```

## 📝 日志记录

### 日志位置
- PowerShell: 控制台输出
- 计划任务: Windows 事件查看器
- 服务: openclaw logs

### 日志格式
```
[时间] [级别] [模块] 消息
[2026-02-12 13:10:00] [INFO] [Updater] 开始版本检查
[2026-02-12 13:10:01] [INFO] [NPM] 最新版本: 2026.2.10
[2026-02-12 13:10:02] [ACTION] [Updater] 执行更新
```

## ⚠️ 注意事项

1. **权限要求**
   - 更新需要管理员权限
   - 使用 `-RunLevel Highest` (计划任务)

2. **网络要求**
   - 需要访问 npm 注册表
   - 建议配置备用源

3. **重启要求**
   - 更新后需要重启 Gateway
   - 确认无活跃任务后重启

4. **错误处理**
   - 网络失败: 跳过更新，记录日志
   - 更新失败: 回滚，通知用户
   - 版本错误: 跳过，保持当前版本

## 🔄 与 SSS 集成

结合 SSS 三层技能架构：

```python
# 在 auto_start.py 中
def startup_sequence():
    """启动序列：SSS + 更新"""
    print("🚀 启动 OpenClaw...")
    
    # Layer 1: 系统检查
    system_check()
    
    # Layer 2: 自动更新
    auto_update()
    
    # Layer 3: 服务启动
    start_services()
    
    # 生成简报
    generate_briefing()
```

## 📈 监控指标

| 指标 | 说明 | 阈值 |
|------|------|------|
| 版本一致性 | 当前 vs 最新 | < 1 版本差 |
| 更新成功率 | 更新成功次数 | > 95% |
| 更新耗时 | 完整更新时间 | < 60s |
| 故障恢复 | 自动恢复能力 | 100% |

## 🐛 故障排除

### 问题1：NPM 无法连接
```powershell
# 检查网络
ping registry.npmjs.org

# 切换国内源
npm config set registry https://registry.npmmirror.com
```

### 问题2：权限不足
```powershell
# 以管理员身份运行
Start-Process powershell -Verb RunAs -ArgumentList "-File auto_update.ps1"
```

### 问题3：版本检测失败
```powershell
# 手动检查版本
npm list -g openclaw

# 强制重新安装
npm uninstall -g openclaw
npm install -g openclaw
```

## 📚 相关文件

- `auto_update.ps1` - 自动更新脚本
- `auto_start.py` - 启动序列
- `startup_config.json` - 启动配置
- `SSS_ARCHITECTURE.md` - SSS 架构文档

---
*文档创建时间: 2026-02-12*
*版本: 1.0*