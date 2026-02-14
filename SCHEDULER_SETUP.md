# OpenClaw 开机自动运行配置
# 功能：开机自动启动 OpenClaw 并执行更新检查

## 方案1：使用 schtasks 创建计划任务

```powershell
# 以管理员身份运行 PowerShell，然后执行：

# 1. 创建开机启动任务
schtasks /create `
    /tn "OpenClaw Auto Start" `
    /tr "powershell -ExecutionPolicy Bypass -File 'C:\Users\殇\.openclaw\workspace\auto_start.ps1'" `
    /sc onstart `
    /ru SYSTEM `
    /rl HIGHEST `
    /f

# 2. 创建每次登录时的任务
schtasks /create `
    /tn "OpenClaw On Login" `
    /tr "python C:\Users\殇\.openclaw\workspace\auto_start.py" `
    /sc onlogon `
    /ru %USERNAME% `
    /rl HIGHEST `
    /f

# 3. 查看任务列表
schtasks /query | Select-String "OpenClaw"

# 4. 手动启动任务
schtasks /run /tn "OpenClaw Auto Start"

# 5. 删除任务
schtasks /delete /tn "OpenClaw Auto Start" /f
```

## 方案2：使用 New-ScheduledTaskcmdlet（推荐）

```powershell
# 以管理员身份运行

# 1. 创建开机任务
$action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-ExecutionPolicy Bypass -File 'C:\Users\殇\.openclaw\workspace\auto_start.ps1'"

$trigger = New-ScheduledTaskTrigger `
    -AtStartup `
    -RandomDelay (New-TimeSpan -Minutes 2)

$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RunElevated $true

Register-ScheduledTask `
    -TaskName "OpenClaw Auto Start" `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Description "OpenClaw 启动时自动检查更新并抓取 RSS" `
    -RunLevel Highest

# 2. 创建登录任务
$loginAction = New-ScheduledTaskAction `
    -Execute "python.exe" `
    -Argument "C:\Users\殇\.openclaw\workspace\auto_start.py" `
    -WorkingDirectory "C:\Users\殇\.openclaw\workspace"

$loginTrigger = New-ScheduledTaskTrigger `
    -AtLogOn

Register-ScheduledTask `
    -TaskName "OpenClaw On Login" `
    -Action $loginAction `
    -Trigger $loginTrigger `
    -Description "OpenClaw 登录时自动运行" `
    -RunLevel Highest

# 3. 查看任务
Get-ScheduledTask | Where-Object {$_.TaskName -like "*OpenClaw*"} | Format-Table

# 4. 手动测试
Start-ScheduledTask -TaskName "OpenClaw Auto Start"

# 5. 查看任务状态
Get-ScheduledTaskInfo -TaskName "OpenClaw Auto Start"
```

## 方案3：添加到启动文件夹（简单方式）

```powershell
# 创建快捷方式
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\OpenClaw.lnk")
$Shortcut.TargetPath = "python.exe"
$Shortcut.Arguments = "C:\Users\殇\.openclaw\workspace\auto_start.py"
$Shortcut.WorkingDirectory = "C:\Users\殇\.openclaw\workspace"
$Shortcut.Save()
```

## 任务配置详情

### 任务1：开机自动更新检查
- **名称**: OpenClaw Auto Start
- **触发器**: 系统启动后 2 分钟
- **运行**: PowerShell 脚本
- **权限**: 最高（管理员）
- **功能**: 
  - 检查 OpenClaw 版本
  - 自动更新（如需要）
  - 清理缓存
  - 记录日志

### 任务2：登录时运行
- **名称**: OpenClaw On Login
- **触发器**: 用户登录时
- **运行**: Python 脚本
- **权限**: 最高
- **功能**:
  - 抓取 RSS 源
  - 生成每日简报
  - 系统健康检查

## 验证步骤

```powershell
# 1. 检查任务是否存在
schtasks /query | Select-String "OpenClaw"

# 2. 手动触发测试
schtasks /run /tn "OpenClaw Auto Start"

# 3. 查看运行日志
Get-Content "C:\Users\殇\.openclaw\workspace\auto_start.log" -Tail 20

# 4. 检查上次运行结果
Get-ScheduledTaskInfo -TaskName "OpenClaw Auto Start"
```

## 故障排除

### 问题1：任务不运行
```powershell
# 检查任务状态
Get-ScheduledTask -TaskName "OpenClaw Auto Start" | Select-Object State

# 查看任务错误
Get-ScheduledTask -TaskName "OpenClaw Auto Start" | 
    Get-ScheduledTaskInfo | 
    Select-Object LastTaskResult, LastRunTime
```

### 问题2：权限不足
```powershell
# 以管理员身份重新创建任务
schtasks /delete /tn "OpenClaw Auto Start" /f
# 然后重新运行创建脚本
```

### 问题3：脚本路径错误
```powershell
# 确认路径存在
Test-Path "C:\Users\殇\.openclaw\workspace\auto_start.py"
Test-Path "C:\Users\殇\.openclaw\workspace\auto_update.ps1"
```

## 一键配置脚本

```powershell
# 将以下内容保存为 setup_scheduler.ps1 并以管理员身份运行

# 创建所有任务
& {
    # 开机任务
    $action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-ExecutionPolicy Bypass -File 'C:\Users\殇\.openclaw\workspace\auto_start.ps1'"
    $trigger = New-ScheduledTaskTrigger -AtStartup -RandomDelay (New-TimeSpan -Minutes 2)
    $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -StartWhenAvailable -RunElevated $true
    Register-ScheduledTask -TaskName "OpenClaw Auto Start" -Action $action -Trigger $trigger -Settings $settings -Description "OpenClaw 自动更新" -RunLevel Highest -ErrorAction SilentlyContinue
    
    # 登录任务
    $loginAction = New-ScheduledTaskAction -Execute "python.exe" -Argument "C:\Users\殇\.openclaw\workspace\auto_start.py" -WorkingDirectory "C:\Users\殇\.openclaw\workspace"
    $loginTrigger = New-ScheduledTaskTrigger -AtLogOn
    Register-ScheduledTask -TaskName "OpenClaw On Login" -Action $loginAction -Trigger $loginTrigger -Description "OpenClaw 登录运行" -RunLevel Highest -ErrorAction SilentlyContinue
    
    Write-Host "✅ 计划任务创建完成" -ForegroundColor Green
}
```

---
*创建时间: 2026-02-12*
