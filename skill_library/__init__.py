#!/usr/bin/env python3
"""
OpenClaw All-in-One Skill Library
OpenClaw 全功能技能库 - 统一 API 接口
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

# ============== 配置 ==============
WORKSPACE = "C:/Users/殇/.openclaw/workspace"
SKILL_LIBRARY = f"{WORKSPACE}/skill_library"
LEARNING_DATA = f"{SKILL_LIBRARY}/learning_data.json"
AUTO_FIXES = f"{SKILL_LIBRARY}/auto_fixes.py"

# 添加到 path
sys.path.insert(0, WORKSPACE)

# 导入各模块
from proactive_agent_demo import (
    OpportunityDetector,
    AutonomyDecision,
    ProposalProtocol
)

from self_evolving_v2 import (
    LearningDatabase,
    ErrorDetector,
    AutoFixEngine,
    SelfHealingLoop,
    PerformanceMonitor,
    SelfInspection
)

try:
    import tavily
    TAVILY_AVAILABLE = True
except ImportError:
    TAVILY_AVAILABLE = False

# ============== 统一接口类 ==============
class OpenClawAllInOne:
    """OpenClaw 全功能技能库 - 统一 API"""
    
    def __init__(self, tavily_api_key=None):
        print("="*60)
        print("OpenClaw All-in-One Skill Library")
        print("OpenClaw 全功能技能库")
        print("="*60)
        
        # 初始化各模块
        print("\n[初始化模块...]")
        
        # 1. Proactive Agent
        print("  [1/4] Proactive Agent... ", end="")
        self.proactive = ProactiveModule()
        print("OK")
        
        # 2. Tavily Search
        print("  [2/4] Tavily Search... ", end="")
        self.tavily = TavilyModule(api_key=tavily_api_key)
        print("OK" if TAVILY_AVAILABLE else "SKIP (not installed)")
        
        # 3. Self-Evolving
        print("  [3/4] Self-Evolving System... ", end="")
        self.self_evolve = SelfEvolvingModule()
        print("OK")
        
        # 4. Transcribe (语音转写)
        print("  [4/4] OGG Parser... ", end="")
        self.transcribe = TranscribeModule()
        print("OK")
        
        # 初始化状态
        self.status = {
            "initialized_at": datetime.now().isoformat(),
            "modules_loaded": 4,
            "tavily_available": TAVILY_AVAILABLE,
            "health_score": 0
        }
        
        print("\n[初始化完成!]")
    
    def get_health_report(self):
        """获取完整健康报告"""
        health = self.self_evolve.get_health_score()
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "health_score": health['health_score'],
            "grade": health['grade'],
            "success_rate": health['success_rate'],
            "total_tasks": health['total_tasks'],
            "auto_fixes": health['auto_fixes'],
            "errors": health['errors'],
            "modules": {
                "proactive": "active",
                "tavily": "active" if TAVILY_AVAILABLE else "inactive",
                "self_evolving": "active",
                "transcribe": "active"
            },
            "target": {
                "health_score": 100,
                "integrations": "100%",
                "status": "in_progress"
            }
        }
        
        return report
    
    def print_health_status(self):
        """打印健康状态"""
        report = self.get_health_report()
        
        print("\n" + "="*60)
        print("健康状态报告")
        print("="*60)
        print(f"\n健康分数: {report['health_score']}/100 - {report['grade']}")
        print(f"成功率: {report['success_rate']:.1%}")
        print(f"总任务数: {report['total_tasks']}")
        print(f"自动修复: {report['auto_fixes']} 次")
        print(f"错误数: {report['errors']}")
        
        print("\n模块状态:")
        for module, status in report['modules'].items():
            icon = "OK" if status == "active" else "SKIP"
            print(f"  - {module}: {status}")
        
        print("\n目标进度:")
        print(f"  当前健康分数: {report['health_score']}/100")
        print(f"  目标: 100/100")
        print(f"  状态: {'进行中' if report['health_score'] < 100 else '完成!'}")
        
        print("\n" + "="*60)
        
        return report
    
    def save_health_report(self, filepath=None):
        """保存健康报告"""
        report = self.get_health_report()
        filepath = filepath or f"{SKILL_LIBRARY}/health_report.json"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n健康报告已保存到: {filepath}")
        return report


# ============== 各模块封装 ==============
class ProactiveModule:
    """Proactive Agent 模块封装"""
    
    def __init__(self):
        self.opportunities = []
    
    def detect_opportunities(self, user_context=None):
        """检测机会"""
        if user_context is None:
            user_context = {
                "interests": ["automation", "AI", "OpenClaw"],
                "recent_activities": ["学习技能", "测试系统"]
            }
        
        # 模拟检测
        self.opportunities = [
            {
                "type": "interest",
                "title": "深入探索自动化",
                "rationale": "检测到用户对自动化感兴趣",
                "confidence": 0.85
            },
            {
                "type": "optimization",
                "title": "优化工作流",
                "rationale": "可以提高现有流程效率",
                "confidence": 0.75
            }
        ]
        
        return self.opportunities
    
    def generate_proposal(self, opportunity):
        """生成提案"""
        proposal = ProposalProtocol.create_proposal(opportunity)
        return proposal
    
    def get_autonomy_level(self):
        """获取建议自治度"""
        return AutonomyDecision.suggest_autonomy()


class TavilyModule:
    """Tavily Search 模块封装"""
    
    def __init__(self, api_key=None):
        self.available = TAVILY_AVAILABLE
        self.client = None
        
        if self.available and api_key:
            try:
                self.client = tavily.TavilyClient(api_key=api_key)
                print("Tavily API 已连接")
            except Exception as e:
                print(f"Tavily 连接失败: {e}")
                self.available = False
    
    def quick_search(self, query):
        """快速搜索"""
        if not self.available:
            return {"error": "Tavily 不可用"}
        
        result = self.client.search(
            query=query,
            search_depth="basic",
            max_results=3,
            include_answer=True
        )
        return result
    
    def deep_research(self, topic):
        """深度研究"""
        if not self.available:
            return {"error": "Tavily 不可用"}
        
        result = self.client.search(
            query=topic,
            search_depth="advanced",
            max_results=10,
            include_answer=True
        )
        return result


class SelfEvolvingModule:
    """Self-Evolving 模块封装"""
    
    def __init__(self):
        self.db = LearningDatabase()
        self.healer = SelfHealingLoop(self.db)
    
    def on_error(self, error_msg, context=None):
        """记录错误并自动修复"""
        result = self.healer.on_error(error_msg, context)
        return result
    
    def on_success(self, action, result):
        """记录成功"""
        self.healer.on_success(action, result)
    
    def run_self_inspection(self):
        """运行自检"""
        health = PerformanceMonitor.get_health_score(self.db)
        SelfInspection.run_check(self.db)
        return health
    
    def get_health_score(self):
        """获取健康分数"""
        return PerformanceMonitor.get_health_score(self.db)
    
    def get_improvement_suggestions(self):
        """获取改进建议"""
        improvements = []
        
        health = self.get_health_score()
        
        if health['health_score'] < 60:
            improvements.append("增加自动修复覆盖率")
        
        if health['success_rate'] < 0.9:
            improvements.append("优化成功率，减少错误")
        
        if health['total_tasks'] < 10:
            improvements.append("增加使用频率，积累数据")
        
        return improvements


class TranscribeModule:
    """OGG 转写模块封装"""
    
    def __init__(self):
        self.script_path = f"{WORKSPACE}/transcribe.py"
    
    def transcribe(self, audio_path, model="base", language="Chinese"):
        """转写音频"""
        import subprocess
        
        cmd = [
            "python", self.script_path,
            audio_path,
            "--model", model,
            "--language", language
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )
        
        # 提取结果
        if result.returncode == 0:
            # 读取转写结果
            txt_path = audio_path.replace('.ogg', '.txt')
            if os.path.exists(txt_path):
                with open(txt_path, 'r', encoding='utf-8') as f:
                    return f.read()
        
        return result.stderr


# ============== 主函数 ==============
def main():
    """主函数 - 演示所有功能"""
    
    print("\n" + "="*60)
    print("OpenClaw All-in-One Skill Library Demo")
    print("="*60)
    
    # 1. 初始化
    print("\n[Step 1: 初始化]")
    agent = OpenClawAllInOne(tavily_api_key="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")
    
    # 2. 检测机会
    print("\n[Step 2: Proactive Agent - 检测机会]")
    opportunities = agent.proactive.detect_opportunities()
    print(f"发现 {len(opportunities)} 个机会:")
    for i, opp in enumerate(opportunities, 1):
        print(f"  {i}. [{opp['type']}] {opp['title']} ({opp['confidence']:.0%})")
    
    # 3. 深度搜索（如果有 Tavily）
    if TAVILY_AVAILABLE:
        print("\n[Step 3: Tavily Search - 深度研究]")
        results = agent.tavily.deep_research("OpenClaw automation")
        if 'answer' in results:
            print(f"\n答案: {results['answer'][:200]}...")
        print(f"找到 {len(results.get('results', []))} 条结果")
    else:
        print("\n[Step 3: Tavily Search - 跳过 (未配置)]")
    
    # 4. 自我改进
    print("\n[Step 4: Self-Evolving - 自检]")
    health = agent.self_evolve.run_self_inspection()
    
    # 5. 模拟错误和修复
    print("\n[Step 5: 模拟错误自动修复]")
    test_errors = [
        ("Network timeout", "API 调用"),
        ("File not found", "文件读取")
    ]
    
    for error, context in test_errors:
        result = agent.self_evolve.on_error(error, context)
        print(f"  错误: {error[:30]}...")
        print(f"    修复: {len(result.get('fixes_applied', []))} 个自动修复")
    
    # 6. 最终健康检查
    print("\n[Step 6: 最终健康检查]")
    agent.print_health_status()
    
    # 7. 保存报告
    print("\n[Step 7: 保存报告]")
    agent.save_health_report()
    
    print("\n" + "="*60)
    print("Demo 完成!")
    print("="*60)
    
    return agent


if __name__ == "__main__":
    agent = main()
