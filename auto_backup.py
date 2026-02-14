#!/usr/bin/env python3
"""
OpenClaw Workspace 自动备份脚本
每天自动提交并推送到 GitHub，保留历史快照
"""

import os
import subprocess
import json
from datetime import datetime

WORKSPACE = "C:/Users/殇/.openclaw/workspace"
LOG_FILE = "C:/Users/殇/.openclaw/workspace/auto_backup.log"
MAX_BACKUPS = 7  # 保留最近 7 个备份分支

def log(message):
    """记录日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"[{timestamp}] {message}")

def run_git(cmd, cwd=WORKSPACE):
    """执行 git 命令"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=120
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", str(e)

def get_current_sha():
    """获取当前分支的 SHA"""
    code, stdout, _ = run_git("git rev-parse HEAD")
    if code == 0:
        return stdout.strip()
    return None

def create_backup_branch(sha):
    """创建备份分支"""
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
    backup_branch = f"backup-{timestamp}"
    
    # 创建备份分支
    code, _, stderr = run_git(f"git branch {backup_branch} {sha}")
    if code != 0:
        log(f"创建备份分支失败: {stderr}")
        return False
    
    # 推送备份分支
    code, _, stderr = run_git(f"git push origin {backup_branch}")
    if code != 0:
        log(f"推送备份分支失败: {stderr}")
        return False
    
    log(f"备份分支创建成功: {backup_branch}")
    return True

def cleanup_old_backups():
    """清理旧的备份分支，保留最近的 N 个"""
    # 获取所有备份分支
    code, stdout, _ = run_git("git branch -r | grep 'origin/backup-'")
    if code != 0 or not stdout.strip():
        return
    
    branches = []
    for line in stdout.strip().split('\n'):
        branch = line.strip().replace('origin/', '')
        if branch.startswith('backup-'):
            branches.append(branch)
    
    # 按时间排序（旧的在前）
    branches.sort()
    
    # 删除旧的分支，保留最近的 MAX_BACKUPS 个
    if len(branches) > MAX_BACKUPS:
        to_delete = branches[:-MAX_BACKUPS]
        for branch in to_delete:
            code, _, stderr = run_git(f"git push origin --delete {branch}")
            if code == 0:
                log(f"删除旧备份分支: {branch}")
            else:
                log(f"删除失败: {branch} - {stderr}")

def auto_backup():
    """自动备份"""
    log("=" * 50)
    log("开始自动备份...")

    # 1. 在提交前，先保存当前状态为备份
    current_sha = get_current_sha()
    if current_sha:
        create_backup_branch(current_sha)
    
    # 2. 检查是否有变更
    code, stdout, _ = run_git("git status --porcelain")
    if not stdout.strip():
        log("没有变更，跳过提交")
        return
    
    # 3. 获取变更统计
    code, diff_stat, _ = run_git("git diff --stat")
    if code == 0:
        log(f"变更内容: {diff_stat.strip()}")
    
    # 4. 添加并提交
    code, _, stderr = run_git("git add -A")
    if code != 0:
        log(f"添加变更失败: {stderr}")
        return
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    commit_msg = f"backup: {timestamp}"
    code, _, stderr = run_git(f'git commit -m "{commit_msg}"')
    if code != 0:
        log(f"提交失败: {stderr}")
        return
    log(f"提交成功: {commit_msg}")
    
    # 5. 推送到 main 分支
    code, stdout, stderr = run_git("git push origin main")
    if code == 0:
        log("推送成功!")
    else:
        log(f"推送失败: {stderr}")
        return
    
    # 6. 清理旧备份
    cleanup_old_backups()
    
    log("备份完成!")

def main():
    """主函数"""
    log("-" * 50)
    log("OpenClaw Workspace 自动备份")
    auto_backup()
    log("备份完成\n")

if __name__ == "__main__":
    main()
