#!/usr/bin/env python3
"""
OpenClaw Workspace 自动备份脚本
每天自动提交并推送到 GitHub
"""

import os
import subprocess
import json
from datetime import datetime

WORKSPACE = "C:/Users/殇/.openclaw/workspace"
LOG_FILE = "C:/Users/殇/.openclaw/workspace/auto_backup.log"

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

def check_changes():
    """检查是否有变更"""
    code, stdout, _ = run_git("git status --porcelain")
    if code == 0 and stdout.strip():
        return True
    return False

def auto_backup():
    """自动备份"""
    log("=" * 50)
    log("开始自动备份...")

    # 检查是否有变更
    if not check_changes():
        log("没有变更，跳过备份")
        return

    # 获取变更统计
    code, stdout, _ = run_git("git diff --stat")
    if code == 0:
        log(f"变更内容: {stdout.strip()}")

    # 添加所有变更
    code, _, stderr = run_git("git add -A")
    if code != 0:
        log(f"添加变更失败: {stderr}")
        return

    # 提交
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    commit_msg = f"backup: {timestamp}"
    code, _, stderr = run_git(f'git commit -m "{commit_msg}"')
    if code != 0:
        log(f"提交失败: {stderr}")
        return
    log(f"提交成功: {commit_msg}")

    # 推送到 working 分支
    code, stdout, stderr = run_git("git push origin working")
    if code == 0:
        log("推送成功!")
    else:
        log(f"推送失败: {stderr}")

def main():
    """主函数"""
    log("-" * 50)
    log("OpenClaw Workspace 自动备份")
    auto_backup()
    log("备份完成\n")

if __name__ == "__main__":
    main()
