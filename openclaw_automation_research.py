#!/usr/bin/env python3
"""
OpenClaw 自动化研究 - Proactive Agent + Tavily Search 完整流程
"""

import os
import tavily
from datetime import datetime

# ============== 配置 ==============
API_KEY = "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"

# ============== 场景背景 ==============
CONTEXT = {
    "user_query": "如何让 OpenClaw 实现自动化",
    "user_interests": ["automation", "OpenClaw", "AI agents"],
    "trust_level": 0.7,
    "autonomy_preference": "moderate"
}

# ============== Phase 1: 机会检测 ==============
class OpportunityDetection:
    @staticmethod
    def analyze_request(request):
        """分析用户请求中的自动化机会"""
        opportunities = []
        
        keywords = {
            "automation": {
                "type": "capability_gap",
                "description": "用户希望提升自动化能力",
                "response": "研究和提供 OpenClaw 自动化方案"
            },
            "integration": {
                "type": "integration_opportunity", 
                "description": "可能需要与其他工具集成",
                "response": "提供集成方案和最佳实践"
            },
            "workflow": {
                "type": "workflow_optimization",
                "description": "可能存在可以自动化的重复任务",
                "response": "识别并建议自动化工作流"
            }
        }
        
        request_lower = request.lower()
        for keyword, config in keywords.items():
            if keyword in request_lower:
                opportunities.append({
                    "type": config["type"],
                    "description": config["description"],
                    "response": config["response"],
                    "confidence": 0.8
                })
        
        return opportunities

# ============== Phase 2: Tavily 搜索 ==============
class TavilyResearch:
    def __init__(self, api_key):
        self.client = tavily.TavilyClient(api_key=api_key)
    
    def search_with_framework(self, query, depth="advanced"):
        """使用 Tavily 进行结构化搜索"""
        print(f"\n[搜索] {query}")
        
        result = self.client.search(
            query=query,
            search_depth=depth,
            max_results=10,
            include_answer=True,
            include_raw_content=True
        )
        
        return {
            "query": query,
            "answer": result.get("answer"),
            "results": result.get("results", []),
            "source_count": len(result.get("results", []))
        }
    
    def multi_angle_search(self, topic):
        """多角度搜索"""
        search_queries = [
            f"OpenClaw automation workflows",
            f"OpenClaw AI agent self-improvement", 
            f"OpenClaw integration examples",
            f"OpenClaw cron scheduling automation"
        ]
        
        all_results = {}
        
        for query in search_queries:
            result = self.search_with_framework(query)
            all_results[query] = result
        
        return all_results

# ============== Phase 3: 自治度评估 ==============
class AutonomyAssessment:
    @staticmethod
    def evaluate_action(initiative):
        """评估应该给多少自治度"""
        
        reversibility = initiative.get("reversibility", "partially_reversible")
        impact = initiative.get("impact", "medium")
        
        # 决策矩阵
        if reversibility == "fully_reversible" and impact == "minimal":
            return {
                "level": 4,
                "action": "执行并提供详细报告",
                "permission": "无需许可，直接执行",
                "notification": "完成后通知"
            }
        elif reversibility == "fully_reversible" and impact == "medium":
            return {
                "level": 3,
                "action": "执行并提供选项",
                "permission": "告知后执行",
                "notification": "过程中同步"
            }
        else:
            return {
                "level": 2,
                "action": "提供建议和方案",
                "permission": "需要明确批准",
                "notification": "执行前确认"
            }
    
    @staticmethod
    def suggest_autonomy():
        """基于用户偏好建议自治度"""
        trust = 0.7  # CONTEXT 中的信任级别
        
        if trust >= 0.8:
            return "high"
        elif trust >= 0.5:
            return "moderate"
        else:
            return "minimal"

# ============== Phase 4: 提案生成 ==============
class ProposalGenerator:
    @staticmethod
    def generate_research_proposal(query, context):
        """生成研究提案"""
        autonomy = AutonomyAssessment.suggest_autonomy()
        
        proposal = {
            "title": f"深度研究: {query}",
            "rationale": "用户希望了解 OpenClaw 自动化方案，这是一个高价值话题。",
            "scope": [
                "搜索 OpenClaw 自动化相关资料",
                "整理最佳实践和方案",
                "提供可执行的建议"
            ],
            "estimated_time": "5-10分钟",
            "autonomy_level": autonomy,
            "execution_plan": [
                "使用 Tavily 搜索相关信息",
                "分析搜索结果并整理",
                "生成结构化报告",
                "提供下一步建议"
            ]
        }
        
        return proposal

# ============== Phase 5: 结果整理 ==============
class ResultSynthesizer:
    @staticmethod
    def synthesize_research(query, results):
        """综合搜索结果"""
        
        synthesis = {
            "topic": query,
            "timestamp": datetime.now().isoformat(),
            "key_findings": [],
            "recommendations": [],
            "next_steps": []
        }
        
        # 从 Tavily 答案中提取关键信息
        if results.get("answer"):
            synthesis["key_findings"].append({
                "source": "Tavily AI Answer",
                "summary": results["answer"][:500]
            })
        
        # 整理推荐结果
        for result in results.get("results", [])[:5]:
            synthesis["recommendations"].append({
                "title": result.get("title"),
                "url": result.get("url"),
                "snippet": result.get("snippet", "")[:200]
            })
        
        # 生成下一步建议
        synthesis["next_steps"] = [
            "尝试配置 cron 自动化任务",
            "集成 Tavily 进行深度搜索",
            "使用 proactive-agent 框架主动提案",
            "定期检查并优化工作流"
        ]
        
        return synthesis

# ============== Phase 6: 报告生成 ==============
class ReportGenerator:
    @staticmethod
    def generate_report(proposal, synthesis, autonomy_assessment):
        """生成完整报告"""
        
        report = f"""
{'='*60}
OpenClaw 自动化研究报告
{'='*60}

[提案信息]
标题: {proposal['title']}
理由: {proposal['rationale']}
自治级别: Level {autonomy_assessment['level']} - {autonomy_assessment['action']}
权限: {autonomy_assessment['permission']}
通知: {autonomy_assessment['notification']}
预计时间: {proposal['estimated_time']}

[执行计划]
"""
        
        for i, step in enumerate(proposal["execution_plan"], 1):
            report += f"  {i}. {step}\n"
        
        report += f"""
[关键发现]
"""
        
        for i, finding in enumerate(synthesis["key_findings"], 1):
            report += f"\n{i}. [{finding['source']}]\n"
            report += f"   {finding['summary'][:300]}...\n"
        
        report += f"""
[推荐资源]
"""
        
        for i, rec in enumerate(synthesis["recommendations"], 1):
            report += f"\n{i}. {rec['title']}\n"
            report += f"   链接: {rec['url']}\n"
            report += f"   摘要: {rec['snippet'][:150]}...\n"
        
        report += f"""
[下一步建议]
"""
        
        for i, step in enumerate(synthesis["next_steps"], 1):
            report += f"  {i}. {step}\n"
        
        report += f"""
{'='*60}
报告生成时间: {synthesis['timestamp']}
{'='*60}
"""
        
        return report

# ============== 主流程 ==============
def main():
    print("="*60)
    print("OpenClaw 自动化研究 - Proactive Agent 完整流程")
    print("="*60)
    
    # 1. 机会检测
    print("\n[Phase 1: 机会检测]")
    opportunities = OpportunityDetection.analyze_request(CONTEXT["user_query"])
    print(f"发现 {len(opportunities)} 个机会:")
    for opp in opportunities:
        print(f"  - [{opp['type']}] {opp['description']}")
    
    # 2. 自治度评估
    print("\n[Phase 2: 自治度评估]")
    autonomy = AutonomyAssessment.suggest_autonomy()
    print(f"建议自治级别: {autonomy}")
    
    # 3. 生成提案
    print("\n[Phase 3: 生成提案]")
    proposal = ProposalGenerator.generate_research_proposal(
        CONTEXT["user_query"], 
        CONTEXT
    )
    print(f"标题: {proposal['title']}")
    print(f"自治级别: {proposal['autonomy_level']}")
    print(f"预计时间: {proposal['estimated_time']}")
    
    # 4. 执行搜索
    print("\n[Phase 4: 执行 Tavily 搜索]")
    research = TavilyResearch(API_KEY)
    results = research.multi_angle_search("OpenClaw automation")
    
    total_sources = sum(r["source_count"] for r in results.values())
    print(f"完成 {len(results)} 个搜索，找到 {total_sources} 个来源")
    
    # 5. 综合结果
    print("\n[Phase 5: 综合结果]")
    synthesis = ResultSynthesizer.synthesize_research(
        CONTEXT["user_query"],
        list(results.values())[0]  # 使用第一个搜索结果
    )
    print(f"主题: {synthesis['topic']}")
    print(f"关键发现: {len(synthesis['key_findings'])} 条")
    print(f"推荐资源: {len(synthesis['recommendations'])} 条")
    print(f"下一步: {len(synthesis['next_steps'])} 项")
    
    # 6. 评估行动
    print("\n[Phase 6: 行动评估]")
    initiative = {
        "reversibility": "fully_reversible",
        "impact": "medium"
    }
    autonomy_assessment = AutonomyAssessment.evaluate_action(initiative)
    print(f"自治级别: Level {autonomy_assessment['level']}")
    print(f"执行方式: {autonomy_assessment['action']}")
    print(f"权限: {autonomy_assessment['permission']}")
    
    # 7. 生成报告
    print("\n[Phase 7: 生成报告]")
    report = ReportGenerator.generate_report(proposal, synthesis, autonomy_assessment)
    print(report)
    
    # 8. 保存报告
    report_path = "C:/Users/殇/.openclaw/workspace/openclaw_automation_report.txt"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\n报告已保存到: {report_path}")
    
    return {
        "opportunities": opportunities,
        "proposal": proposal,
        "results": results,
        "synthesis": synthesis,
        "autonomy_assessment": autonomy_assessment,
        "report": report
    }

if __name__ == "__main__":
    main()
