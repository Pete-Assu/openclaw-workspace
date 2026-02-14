# OpenClaw 自动备份计划任务

## 手动运行
```bash
python "C:/Users/殇/.openclaw/workspace/auto_backup.py"
```

## Windows 计划任务设置

以管理员身份运行 PowerShell：

```powershell
# 创建每日凌晨 3 点执行的任务
$action = New-ScheduledTaskAction -Execute "python.exe" -Argument '"C:/Users/殇/.openclaw/workspace/auto_backup.py"' -WorkingDirectory "C:/Users/殇/.openclaw/workspace"
$trigger = New-ScheduledTaskTrigger -Daily -At 3am
$settings = New-ScheduledTaskSettingsSet -RunOnlyIfNetworkAvailable -WakeToRun
Register-ScheduledTask -TaskName "OpenClaw-Auto-Backup" -Action $action -Trigger $trigger -Settings $settings -RunLevel Highest
```

## 查看任务状态
```powershell
Get-ScheduledTask -TaskName "OpenClaw-Auto-Backup"
```

## 删除任务
```powershell
Unregister-ScheduledTask -TaskName "OpenClaw-Auto-Backup" -Confirm
```

## 备份日志
- 位置: `C:/Users/殇/.openclaw/workspace/auto_backup.log`
