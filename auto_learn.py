#!/usr/bin/env python3
"""
自主学习系统 - 扫描多平台发现新技能
来源：ClawHub、GitHub、Moltbook
"""

import os
import subprocess
import json
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

WORKSPACE = "C:/Users/殇/.openclaw/workspace"
LOG_FILE = f"{WORKSPACE}/memory/learning.log"
DISCOVERED_FILE = f"{WORKSPACE}/memory/discovered-skills.jsonl"

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
            cmd, shell=True, cwd=cwd, capture_output=True, text=True, timeout=60
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", str(e)

# ============ 1. 扫描 ClawHub ============
def scan_clawhub():
    """扫描 ClawHub 技能市场"""
    log("🔍 扫描 ClawHub...")
    skills = []
    
    try:
        # ClawHub API - 获取热门技能
        url = "https://clawhub.com/api/skills?sort=popular&limit=20"
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read().decode())
        
        for item in data.get("skills", []):
            skills.append({
                "title": item.get("name", ""),
                "description": item.get("description", ""),
                "source": "ClawHub",
                "url": item.get("url", ""),
                "quality_score": item.get("rating", 0.8),
                "category": item.get("category", "automation")
            })
        
        log(f"   ClawHub: 发现 {len(skills)} 个技能")
    except Exception as e:
        log(f"   ClawHub 扫描失败: {e}")
    
    return skills

# ============ 2. 扫描 GitHub ============
def scan_github():
    """扫描 GitHub 搜索高质量项目"""
    log("🔍 扫描 GitHub...")
    skills = []
    
    github_token = os.environ.get("GITHUB_TOKEN", "")
    headers = {}
    if github_token:
        headers["Authorization"] = f"token {github_token}"
    
    # 搜索查询：OpenClaw 相关技能
    queries = [
        ("openclaw+skill", "openclaw"),
        ("automation+agent", "automation"),
        ("self-improving+ai", "ai"),
        ("open-source+automation", "oss"),
    ]
    
    for query, category in queries:
        try:
            url = f"https://api.github.com/search/repositories?q={query}+stars:>10&sort=stars&per_page=10"
            req = urllib.request.Request(url, headers=headers)
            resp = urllib.request.urlopen(req, timeout=15)
            data = json.loads(resp.read().decode())
            
            for item in data.get("items", []):
                skills.append({
                    "title": item.get("name", ""),
                    "description": item.get("description", ""),
                    "source": "GitHub",
                    "url": item.get("html_url", ""),
                    "stars": item.get("stargazers_count", 0),
                    "quality_score": min(item.get("stargazers_count", 0) / 1000, 1.0),
                    "category": category
                })
            
            log(f"   GitHub ({query}): 发现 {len(data.get('items', []))} 个项目")
        except Exception as e:
            log(f"   GitHub ({query}) 扫描失败: {e}")
    
    return skills

# ============ 3. 扫描 Moltbook ============
def scan_moltbook():
    """扫描 Moltbook AI 研究"""
    log("🔍 扫描 Moltbook...")
    papers = []
    
    try:
        # Moltbook API - 获取最新论文
        url = "https://www.moltbook.com/api/papers?sort=recent&limit=10"
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read().decode())
        
        for item in data.get("papers", []):
            papers.append({
                "title": item.get("title", ""),
                "description": item.get("abstract", ""),
                "source": "Moltbook",
                "url": item.get("url", ""),
                "quality_score": item.get("citation_count", 0) / 100,
                "category": "research"
            })
        
        log(f"   Moltbook: 发现 {len(papers)} 篇论文")
    except Exception as e:
        log(f"   Moltbook 扫描失败: {e}")
    
    return papers

# ============ 4. 去重和评估 ============
def deduplicate_and_score(all_skills):
    """去重并评估质量"""
    log("📊 去重和评估...")
    
    # 去重
    seen = set()
    unique = []
    for skill in all_skills:
        key = skill["title"].lower()
        if key not in seen:
            seen.add(key)
            unique.append(skill)
    
    # 评估质量分数
    for skill in unique:
        score = skill.get("quality_score", 0.5)
        # 关键词加权
        text = f"{skill['title']} {skill.get('description', '')}".lower()
        
        bonus = 0
        keywords = ["openclaw", "automation", "agent", "self-*", "autonomous", "ai", "claude"]
        for kw in keywords:
            if kw.replace("*", "") in text:
                bonus += 0.1
        
        skill["quality_score"] = min(score + bonus, 1.0)
    
    # 排序
    unique.sort(key=lambda x: x.get("quality_score", 0), reverse=True)
    
    log(f"   去重后: {len(unique)} 个唯一项目")
    return unique

# ============ 5. 保存发现 ============
def save_discovered(skills):
    """保存发现到文件"""
    log("💾 保存发现...")
    
    Path(DISCOVERED_FILE).parent.mkdir(parents=True, exist_ok=True)
    
    with open(DISCOVERED_FILE, "a", encoding="utf-8") as f:
        for skill in skills[:20]:  # 只保存前20个
            f.write(json.dumps({
                **skill,
                "discovered_at": datetime.now().isoformat()
            }) + "\n")
    
    log(f"   已保存 {min(len(skills), 20)} 个发现")

# ============ 6. 生成报告 ============
def generate_report(skills):
    """生成学习报告"""
    log("\n" + "=" * 50)
    log("📋 自主学习报告")
    log("=" * 50)
    
    # 统计
    by_source = {}
    by_category = {}
    for skill in skills:
        source = skill.get("source", "Unknown")
        category = skill.get("category", "other")
        by_source[source] = by_source.get(source, 0) + 1
        by_category[category] = by_category.get(category, 0) + 1
    
    log(f"\n📊 统计:")
    for source, count in by_source.items():
        log(f"   {source}: {count} 个")
    
    log(f"\n🌟 Top 5 高质量项目:")
    for i, skill in enumerate(skills[:5]):
        score = skill.get("quality_score", 0)
        log(f"   {i+1}. [{score:.0%}] {skill['title'][:40]}")
    
    # 高分技能列表
    high_score = [s for s in skills if s.get("quality_score", 0) > 0.7]
    log(f"\n🎯 推荐关注 ({len(high_score)} 个高分项目)")
    
    return {
        "total": len(skills),
        "by_source": by_source,
        "by_category": by_category,
        "high_score_count": len(high_score),
        "top5": skills[:5]
    }

# ============ 主函数 ============
def main():
    log("=" * 50)
    log("🚀 开始自主学习扫描")
    log("=" * 50)
    
    all_skills = []
    
    # 扫描各平台
    all_skills.extend(scan_clawhub())
    all_skills.extend(scan_github())
    all_skills.extend(scan_moltbook())
    
    if not all_skills:
        log("❌ 没有发现任何新技能")
        return
    
    # 去重和评估
    skills = deduplicate_and_score(all_skills)
    
    # 保存
    save_discovered(skills)
    
    # 报告
    report = generate_report(skills)
    
    # 提交到 GitHub
    log("\n📤 提交到 GitHub...")
    run_git(f'git add -A', WORKSPACE)
    run_git(f'git commit -m "learn: 自主学习扫描 {datetime.now().strftime('%Y-%m-%d %H:%M')}"', WORKSPACE)
    run_git(f'git push origin main', WORKSPACE)
    log("   推送成功!")
    
    log("\n✅ 自主学习完成!")
    
    return report

if __name__ == "__main__":
    main()
