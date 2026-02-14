#!/usr/bin/env python3
"""
RSS Feed Fetcher - 启动时自动抓取科技源
"""

import os
# SSL FIX APPLIED
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import json
import feedparser
from datetime import datetime
from pathlib import Path

# ============== 配置 ==============
WORKSPACE = "C:/Users/殇/.openclaw/workspace"
RSS_DATA = f"{WORKSPACE}/rss_feed.json"
RSS_LOG = f"{WORKSPACE}/rss_fetch.log"

# 科技 RSS 源
RSS_FEEDS = [
    {
        "name": "TechCrunch",
        "url": "https://techcrunch.com/feed/",
        "category": "科技"
    },
    {
        "name": "The Verge",
        "url": "https://www.theverge.com/rss/index.xml",
        "category": "科技"
    },
    {
        "name": "Wired",
        "url": "https://www.wired.com/feed/rss",
        "category": "科技"
    },
    {
        "name": "MIT Technology Review",
        "url": "https://www.technologyreview.com/feed/",
        "category": "科技"
    },
    {
        "name": "Hacker News",
        "url": "https://hnrss.org/frontpage",
        "category": "科技"
    },
    {
        "name": "Product Hunt",
        "url": "https://www.producthunt.com/feed",
        "category": "产品"
    },
    {
        "name": "GitHub Blog",
        "url": "https://github.blog/feed/",
        "category": "开发"
    },
    {
        "name": "OpenAI Blog",
        "url": "https://openai.com/blog/rss.xml",
        "category": "AI"
    }
]

class RSSFetcher:
    """RSS 抓取器"""
    
    def __init__(self):
        self.feeds = RSS_FEEDS
        self.results = []
        self.start_time = datetime.now()
    
    def log(self, message):
        """日志记录"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        with open(RSS_LOG, 'a', encoding='utf-8', errors='ignore') as f:
            f.write(log_entry)
        
        # 移除 emoji 避免编码问题
        clean_message = message.replace("✅", "[OK]").replace("❌", "[FAIL]").replace("⚠️", "[WARN]")
        print(f"[{timestamp}] {clean_message}")
    
    def fetch_feed(self, feed):
        """抓取单个 RSS 源"""
        try:
            self.log(f"抓取: {feed['name']}...")
            
            # 解析 RSS
            parsed = feedparser.parse(feed['url'])
            
            if parsed.bozo:
                self.log(f"  [WARN] 解析错误: {parsed.bozo_exception}")
                return None
            
            # 提取文章
            articles = []
            for entry in parsed.entries[:5]:  # 每个源取前5条
                article = {
                    "title": entry.get("title", ""),
                    "link": entry.get("link", ""),
                    "published": entry.get("published", ""),
                    "summary": entry.get("summary", "")[:200],
                    "source": feed['name'],
                    "category": feed['category'],
                    "fetched_at": datetime.now().isoformat()
                }
                articles.append(article)
            
            self.log(f"  [OK] 获取 {len(articles)} 篇文章")
            
            return {
                "source": feed['name'],
                "category": feed['category'],
                "url": feed['url'],
                "articles": articles,
                "fetched_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.log(f"  [FAIL] 失败: {e}")
            return None
    
    def fetch_all(self):
        """抓取所有 RSS 源"""
        self.log("="*60)
        self.log("RSS Feed Fetcher - 科技源抓取")
        self.log(f"启动时间: {self.start_time.isoformat()}")
        self.log(f"源数量: {len(self.feeds)}")
        self.log("="*60)
        
        results = []
        
        for feed in self.feeds:
            result = self.fetch_feed(feed)
            if result:
                results.append(result)
        
        # 保存结果
        self.save_results(results)
        
        # 完成
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        self.log("="*60)
        self.log(f"抓取完成! 耗时: {duration:.2f}秒")
        self.log(f"成功: {len(results)}/{len(self.feeds)} 个源")
        self.log(f"文章总数: {sum(len(r['articles']) for r in results)}")
        self.log("="*60)
        
        return results
    
    def save_results(self, results):
        """保存抓取结果"""
        data = {
            "fetched_at": datetime.now().isoformat(),
            "sources_count": len(results),
            "total_articles": sum(len(r['articles']) for r in results),
            "feeds": results
        }
        
        with open(RSS_DATA, 'w', encoding='utf-8', errors='ignore') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        self.log(f"结果已保存到: {RSS_DATA}")
    
    def get_summary(self):
        """获取摘要"""
        if not os.path.exists(RSS_DATA):
            return None
        
        with open(RSS_DATA, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        summary = f"""
📰 RSS 科技源摘要
抓取时间: {data['fetched_at']}
源数量: {data['sources_count']}
文章总数: {data['total_articles']}

最新文章:
"""
        
        for feed in data['feeds'][:3]:  # 显示前3个源
            summary += f"\n[{feed['source']}]\n"
            for article in feed['articles'][:3]:  # 每个源显示前3条
                summary += f"  • {article['title'][:50]}...\n"
                summary += f"    {article['link']}\n"
        
        return summary


def main():
    """主入口"""
    fetcher = RSSFetcher()
    results = fetcher.fetch_all()
    return results


if __name__ == "__main__":
    main()
