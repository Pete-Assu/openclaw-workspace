#!/usr/bin/env python3
"""
Proactive Agent Demo - 主动式代理演示
基于 proactive-agent 框架的实际应用
"""

import os
from datetime import datetime

# ============== 配置 ==============
USER_PREFERENCES = {
    "trust_level": 0.7,  # 0.0-1.0
    "preferred_autonomy": "moderate",  # minimal/moderate/high
    "notification_style": "concise",  # detailed/concise
    "focus_areas": ["skills", "productivity", "automation"],
    "avoid_areas": []
}

# ============== 自治度决策框架 ==============
class AutonomyDecision:
    @staticmethod
    def evaluate(task_info):
        """评估任务的自治度级别"""
        
        reversibility = task_info.get("reversibility", "partially_reversible")
        impact = task_info.get("impact", "medium")
        urgency = task_info.get("urgency", "normal")
        
        # 决策矩阵
        if reversibility == "fully_reversible" and impact == "minimal":
            return {"level": 4, "action": "直接执行并报告", "notify": "之后"}
        elif reversibility == "fully_reversible" and impact == "medium":
            return {"level": 3, "action": "执行并提供选项", "notify": "过程中"}
        elif reversibility == "irreversible" and impact == "medium":
            return {"level": 1, "action": "请求明确许可", "notify": "之前"}
        else:
            return {"level": 2, "action": "建议并等待批准", "notify": "之前"}
    
    @staticmethod
    def suggest_autonomy_level(preferences, history):
        """根据信任级别建议自治度"""
        trust = preferences.get("trust_level", 0.5)
        
        if trust >= 0.8:
            return "high"
        elif trust >= 0.5:
            return "moderate"
        else:
            return "minimal"

# ============== 机会检测引擎 ==============
class OpportunityDetector:
    @staticmethod
    def detect_friction(conversation_history):
        """检测用户是否在重复做某事"""
        patterns = {}
        for msg in conversation_history[-20:]:  # 最近20条
            topic = msg.get("topic", "unknown")
            patterns[topic] = patterns.get(topic, 0) + 1
        
        # 找出重复的模式
        repeated = [t for t, c in patterns.items() if c >= 3]
        return repeated
    
    @staticmethod
    def detect_interests(conversation_history):
        """检测用户兴趣"""
        topics = []
        for msg in conversation_history[-50:]:  # 最近50条
            if msg.get("type") == "question":
                topics.append(msg.get("topic"))
        
        return list(set(topics))
    
    @staticmethod
    def generate_initiatives(user_context, preferences):
        """生成主动提案"""
        initiatives = []
        
        # 基于兴趣生成提案
        interests = user_context.get("interests", [])
        for interest in interests:
            if interest in preferences.get("focus_areas", []):
                initiatives.append({
                    "type": "interest",
                    "title": f"深入探索 {interest}",
                    "rationale": f"你最近对 {interest} 感兴趣，我可以帮你收集更多信息。",
                    "impact": "medium",
                    "reversibility": "fully_reversible"
                })
        
        # 基于摩擦生成提案
        frictions = user_context.get("frictions", [])
        for friction in frictions:
            initiatives.append({
                "type": "optimization",
                "title": f"自动化 {friction}",
                "rationale": f"检测到你在重复处理 {friction}，可以自动化。",
                "impact": "medium",
                "reversibility": "fully_reversible"
            })
        
        return initiatives

# ============== 提案-执行协议 ==============
class ProposalProtocol:
    @staticmethod
    def create_proposal(initiative):
        """创建提案"""
        return {
            "title": initiative.get("title"),
            "rationale": initiative.get("rationale"),
            "action_plan": f"我将：1) 收集相关信息；2) 制定方案；3) 实施并报告。",
            "impact": initiative.get("impact"),
            "reversibility": initiative.get("reversibility"),
            "estimated_time": "10-30分钟",
            "created_at": datetime.now().isoformat()
        }
    
    @staticmethod
    def execute(proposal, approval=None):
        """执行提案（简化版）"""
        # 模拟执行
        execution_log = {
            "proposal": proposal["title"],
            "started_at": datetime.now().isoformat(),
            "status": "executed",
            "outcome": "完成",
            "artifacts": []
        }
        
        # 这里会实际执行任务
        # ... 执行逻辑 ...
        
        return execution_log

# ============== 主流程演示 ==============
def demo_proactive_agent():
    """演示主动式代理的工作流程"""
    
    print("=" * 60)
    print("Proactive Agent Demo - 主动式代理演示")
    print("=" * 60)
    
    # 1. 模拟用户上下文
    user_context = {
        "interests": ["skills", "productivity", "automation"],
        "frictions": ["重复检查日志", "手动整理笔记"],
        "recent_tasks": ["学习新技能", "配置自动化"]
    }
    
    print("\n[用户上下文分析]")
    print(f"  - 兴趣领域: {', '.join(user_context['interests'])}")
    print(f"  - 痛点/摩擦: {', '.join(user_context['frictions'])}")
    print(f"  - 最近任务: {', '.join(user_context['recent_tasks'])}")
    
    # 2. 检测机会
    print("\n[机会检测]")
    initiatives = OpportunityDetector.generate_initiatives(user_context, USER_PREFERENCES)
    
    for i, init in enumerate(initiatives[:3], 1):  # 只显示前3个
        print(f"\n  {i}. [{init['type']}] {init['title']}")
        print(f"     理由: {init['rationale']}")
    
    # 3. 评估自治度
    print("\n[自治度评估]")
    for init in initiatives[:1]:  # 评估第一个提案
        decision = AutonomyDecision.evaluate(init)
        print(f"  - 任务: {init['title']}")
        print(f"  - 可逆性: {init['reversibility']}")
        print(f"  - 影响: {init['impact']}")
        print(f"  - 建议自治级别: Level {decision['level']}")
        print(f"  - 执行方式: {decision['action']}")
        print(f"  - 通知时机: {decision['notify']}")
    
    # 4. 创建提案
    print("\n[创建提案]")
    proposal = ProposalProtocol.create_proposal(initiatives[0])
    print(f"  标题: {proposal['title']}")
    print(f"  理由: {proposal['rationale']}")
    print(f"  行动计划: {proposal['action_plan']}")
    print(f"  预计时间: {proposal['estimated_time']}")
    
    # 5. 执行（模拟）
    print("\n[执行提案]")
    result = ProposalProtocol.execute(proposal)
    print(f"  状态: {result['status']}")
    print(f"  结果: {result['outcome']}")
    
    print("\n" + "=" * 60)
    print("[演示完成！]")
    print("=" * 60)
    
    return initiatives

if __name__ == "__main__":
    demo_proactive_agent()
