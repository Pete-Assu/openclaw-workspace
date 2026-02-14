#!/usr/bin/env python3
"""
OpenClaw Auto Start - 启动时自动运行
1. 版本自动检查和更新
2. 抓取 RSS 科技源
3. 生成每日简报
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path

# ============== 配置 ==============
WORKSPACE = "C:/Users/殇/.openclaw/workspace"
RSS_DATA = f"{WORKSPACE}/rss_feed.json"
REPORT_FILE = f"{WORKSPACE}/daily_briefing.md"
LOG_FILE = f"{WORKSPACE}/auto_start.log"
UPDATE_SCRIPT = f"{WORKSPACE}/auto_update.ps1"

class AutoStart:
    """自动启动类"""
    
    def __init__(self):
        self.start_time = datetime.now()
        self.results = {}
    
    def log(self, message):
        """日志记录"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_entry)
        
        clean_message = message.replace("✅", "[OK]").replace("❌", "[FAIL]")
        print(f"[{timestamp}] {clean_message}")
    
    def run_version_check(self):
        """自动版本检查和更新"""
        self.log("="*60)
        self.log("OpenClaw Auto Start - Version 2.0")
        self.log(f"启动时间: {self.start_time.isoformat()}")
        self.log("="*60)
        self.log("[1/4] 自动版本检查...")
        
        try:
            # 检查是否存在更新脚本
            if not os.path.exists(UPDATE_SCRIPT):
                self.log("  [WARN] 未找到更新脚本，跳过版本检查")
                self.results["version_check"] = "skipped"
                return True
            
            # 运行 PowerShell 更新脚本
            result = subprocess.run(
                ["powershell", "-File", UPDATE_SCRIPT, "-CheckOnly"],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                # 检查输出中是否有更新提示
                output = result.stdout
                if "已是最新版本" in output or "无需更新" in output:
                    self.log("  [OK] OpenClaw 已是最新版本")
                    self.results["version_check"] = "up_to_date"
                elif "发现新版本" in output:
                    self.log("  [INFO] 发现新版本，开始更新...")
                    # 执行完整更新
                    update_result = subprocess.run(
                        ["powershell", "-File", UPDATE_SCRIPT],
                        capture_output=True,
                        text=True,
                        timeout=120
                    )
                    if update_result.returncode == 0:
                        self.log("  [OK] OpenClaw 已更新到最新版本")
                        self.results["version_check"] = "updated"
                        self.results["needs_restart"] = True
                    else:
                        self.log(f"  [FAIL] 更新失败: {update_result.stderr}")
                        self.results["version_check"] = "update_failed"
                else:
                    self.log("  [OK] 版本检查完成")
                    self.results["version_check"] = "completed"
            else:
                self.log(f"  [FAIL] 版本检查失败: {result.stderr}")
                self.results["version_check"] = "error"
                
        except subprocess.TimeoutExpired:
            self.log("  [FAIL] 版本检查超时")
            self.results["version_check"] = "timeout"
        except Exception as e:
            self.log(f"  [FAIL] 版本检查异常: {e}")
            self.results["version_check"] = "error"
        
        return True
    
    def run_rss_fetcher(self):
        """运行 RSS 抓取"""
        self.log("="*60)
        self.log("OpenClaw Auto Start")
        self.log(f"启动时间: {self.start_time.isoformat()}")
        self.log("="*60)
        self.log("[1/2] 抓取 RSS 科技源...")
        
        try:
            # 导入 RSS 抓取器
            sys.path.insert(0, WORKSPACE)
            from rss_fetcher import RSSFetcher
            
            fetcher = RSSFetcher()
            results = fetcher.fetch_all()
            
            self.results["rss_sources"] = len(results)
            self.results["rss_articles"] = sum(len(r['articles']) for r in results)
            
            self.log(f"  [OK] 成功抓取 {len(results)} 个源，{self.results['rss_articles']} 篇文章")
            
            return results
            
        except Exception as e:
            self.log(f"  [FAIL] RSS 抓取失败: {e}")
            self.results["rss_sources"] = 0
            self.results["rss_articles"] = 0
            return []
    
    def generate_briefing(self, rss_results):
        """生成每日简报"""
        self.log("[2/2] 生成每日简报...")
        
        # 读取 RSS 数据
        if os.path.exists(RSS_DATA):
            with open(RSS_DATA, 'r', encoding='utf-8') as f:
                rss_data = json.load(f)
        else:
            rss_data = {"feeds": rss_results}
        
        # 生成 Markdown 报告
        report = f"""# 📰 OpenClaw Daily Briefing

**生成时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 📊 统计

- **RSS 源**: {rss_data.get('sources_count', len(rss_results))}
- **文章总数**: {rss_data.get('total_articles', sum(len(r['articles']) for r in rss_results))}

---
"""
        
        # 按类别组织
        by_category = {}
        for feed in rss_data.get('feeds', rss_results):
            cat = feed.get('category', '其他')
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(feed)
        
        # 生成每个类别的内容
        for category, feeds in by_category.items():
            report += f"\n## 📁 {category}\n\n"
            
            for feed in feeds:
                report += f"\n### 🔗 {feed['source']}\n\n"
                
                for article in feed.get('articles', [])[:5]:
                    title = article.get('title', '')[:80]
                    link = article.get('link', '')
                    summary = article.get('summary', '')[:150]
                    
                    report += f"- **{title}**\n"
                    report += f"  - {summary}...\n"
                    report += f"  - [阅读更多]({link})\n\n"
        
        # 添加时间戳
        report += f"""
---
*Generated by OpenClaw Auto Start at {datetime.now().isoformat()}*
"""
        
        # 保存报告
        with open(REPORT_FILE, 'w', encoding='utf-8') as f:
            f.write(report)
        
        self.log(f"  [OK] 简报已保存到: daily_briefing.md")
        self.results["report_file"] = REPORT_FILE
        
        return report
    
    def run(self):
        """主运行流程"""
        self.log("="*60)
        self.log("OpenClaw Auto Start - Version 2.0")
        self.log(f"启动时间: {self.start_time.isoformat()}")
        self.log("="*60)
        
        # Step 1: 版本检查和更新
        self.log("[1/4] 自动版本检查...")
        self.run_version_check()
        
        # Step 2: 抓取 RSS
        self.log("[2/4] 抓取 RSS 科技源...")
        rss_results = self.run_rss_fetcher()
        
        # Step 3: 生成简报
        self.log("[3/4] 生成每日简报...")
        self.generate_briefing(rss_results)
        
        # Step 4: 完成
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        self.log("="*60)
        self.log(f"完成! 耗时: {duration:.2f}秒")
        self.log(f"版本检查: {self.results.get('version_check', 'N/A')}")
        self.log(f"RSS 源: {self.results.get('rss_sources', 0)}")
        self.log(f"文章数: {self.results.get('rss_articles', 0)}")
        self.log("="*60)
        
        return self.results


def main():
    """主入口"""
    auto_start = AutoStart()
    results = auto_start.run()
    return results


if __name__ == "__main__":
    main()
