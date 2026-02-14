# OpenClaw 自动更新配置指南

## 快速开始

### 1. 运行自动更新
`powershell
# 检查版本
.\auto_update.ps1 -CheckOnly

# 完整更新
.\auto_update.ps1

# Python 启动序列
python auto_start_sequence.py
`

### 2. 配置启动时自动更新
编辑 uto_start.py，添加：
`python
import subprocess
import os

def auto_update_on_startup():
    script_path = os.path.join(os.path.dirname(__file__), "auto_update.ps1")
    subprocess.run(["powershell", "-File", script_path, "-CheckOnly"])

# 在启动函数中调用
auto_update_on_startup()
`

### 3. 创建系统启动任务 (Windows)
`powershell
# 创建计划任务
schtasks /create /tn "OpenClaw Auto Update" /tr "powershell -File C:\Users\殇\.openclaw\workspace\auto_update.ps1" /sc onstart /ru SYSTEM
`

## 文件清单

| 文件 | 说明 | 重要性 |
|------|------|--------|
| auto_update.ps1 | 自动更新脚本 | ⭐⭐⭐ 核心 |
| auto_start_sequence.py | Python 启动序列 | ⭐⭐⭐ 集成 |
| startup_config.json | 启动配置 | ⭐⭐ 可选 |
| OPENCLAW_AUTO_UPDATE.md | 完整文档 | ⭐⭐ 参考 |
| startup_brief.log | 启动日志 | ⭐ 记录 |

## 使用统计

- 启动检查: 默认启用
- 自动更新: 发现新版本时触发
- 缓存清理: 每次更新后执行
- 重启提示: 可选

## 监控

- 检查时间: 每次启动时
- 日志位置: startup_brief.log
- 状态报告: 控制台输出
