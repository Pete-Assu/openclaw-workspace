#!/usr/bin/env python3
"""
Tavily Search Demo - AI优化搜索引擎演示
"""

import os
import tavily

# ============== 配置 ==============
API_KEY = "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"

# ============== Tavily 客户端 ==============
class TavilyDemo:
    def __init__(self, api_key):
        # 使用 TavilyClient
        self.client = tavily.TavilyClient(api_key=api_key)
    
    def quick_search(self, query):
        """快速搜索"""
        print(f"\n[快速搜索] {query}")
        result = self.client.search(
            query=query,
            search_depth="basic",
            max_results=3,
            include_answer=True
        )
        return result
    
    def deep_search(self, query):
        """深度搜索"""
        print(f"\n[深度搜索] {query}")
        result = self.client.search(
            query=query,
            search_depth="advanced",
            max_results=5,
            include_answer=True,
            include_raw_content=True
        )
        return result
    
    def research_topic(self, topic):
        """研究主题"""
        print(f"\n[研究主题] {topic}")
        
        # 搜索
        print("  -> 执行搜索...")
        search_result = self.client.search(
            query=topic,
            search_depth="advanced",
            max_results=10,
            include_answer=True
        )
        
        return {
            "topic": topic,
            "answer": search_result.get("answer"),
            "results": search_result.get("results", []),
        }

# ============== 演示 ==============
def demo_tavily():
    """演示 Tavily 搜索"""
    
    print("=" * 60)
    print("Tavily Search Demo - AI优化搜索引擎演示")
    print("=" * 60)
    
    demo = TavilyDemo(API_KEY)
    
    # 1. 快速搜索
    print("\n[示例1: 快速搜索]")
    result = demo.quick_search("OpenClaw AI agent")
    if result.get("answer"):
        print(f"\n答案: {result['answer'][:200]}...")
    print(f"\n找到 {len(result.get('results', []))} 条结果")
    
    # 2. 深度搜索
    print("\n" + "-" * 60)
    print("[示例2: 深度搜索]")
    result = demo.deep_search("best AI agent frameworks 2024")
    if result.get("answer"):
        print(f"\n答案: {result['answer'][:300]}...")
    print(f"\n找到 {len(result.get('results', []))} 条结果")
    
    # 3. 主题研究
    print("\n" + "-" * 60)
    print("[示例3: 主题研究]")
    result = demo.research_topic("Whisper speech recognition")
    print(f"\n主题: {result['topic']}")
    if result.get("answer"):
        print(f"\n总结: {result['answer'][:300]}...")
    
    print("\n" + "=" * 60)
    print("[演示完成！]")
    print("=" * 60)

if __name__ == "__main__":
    try:
        demo_tavily()
    except Exception as e:
        print(f"\n[错误] {e}")
