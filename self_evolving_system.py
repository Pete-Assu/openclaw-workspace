#!/usr/bin/env python3
"""
OpenClaw Self-Evolving System - 自我改进与学习系统
基于 proactive-agent 的自主学习框架
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path

# ============== 配置 ==============
WORKSPACE = "C:/Users/殇/.openclaw/workspace"
LEARNING_DATA = f"{WORKSPACE}/learning_data.json"
ERROR_LOG = f"{WORKSPACE}/error_patterns.json"
IMPROVEMENTS = f"{WORKSPACE}/improvements.json"

# ============== 数据结构 ==============
class LearningData:
    """学习数据结构"""
    
    def __init__(self):
        self.data = {
            "version": "1.0",
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "error_patterns": [],
            "success_patterns": [],
            "improvements": [],
            "metrics": {
                "total_tasks": 0,
                "success_rate": 0.0,
                "common_errors": {},
                "learned_skills": []
            }
        }
        
        # 加载现有数据
        self.load()
    
    def load(self):
        """加载学习数据"""
        if os.path.exists(LEARNING_DATA):
            try:
                with open(LEARNING_DATA, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    self.data.update(loaded)
            except:
                pass
    
    def save(self):
        """保存学习数据"""
        self.data["last_updated"] = datetime.now().isoformat()
        with open(LEARNING_DATA, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

# ============== Phase 1: 错误分析 ==============
class ErrorAnalyzer:
    """错误模式分析器"""
    
    @staticmethod
    def analyze_error(error_msg, context=None):
        """分析错误并提取模式"""
        patterns = {
            "network": ["timeout", "connection", "network", "internet"],
            "api": ["api", "401", "403", "404", "rate limit"],
            "file": ["file", "path", "permission", "not found"],
            "memory": ["memory", "out of", "overflow"],
            "encoding": ["encoding", "utf-8", "unicode", "gbk"]
        }
        
        error_lower = error_msg.lower()
        detected_patterns = []
        
        for pattern_type, keywords in patterns.items():
            for keyword in keywords:
                if keyword in error_lower:
                    detected_patterns.append(pattern_type)
                    break
        
        return {
            "error_msg": error_msg,
            "patterns": detected_patterns,
            "timestamp": datetime.now().isoformat(),
            "context": context or {}
        }
    
    @staticmethod
    def generate_solution(pattern):
        """根据错误模式生成解决方案"""
        solutions = {
            "network": {
                "strategy": "retry_with_backoff",
                "timeout": 30,
                "retries": 3,
                "message": "网络问题：使用指数退避重试"
            },
            "api": {
                "strategy": "check_auth",
                "timeout": 10,
                "message": "API 问题：检查认证和权限"
            },
            "file": {
                "strategy": "check_paths",
                "timeout": 5,
                "message": "文件问题：检查路径和权限"
            },
            "encoding": {
                "strategy": "safe_decode",
                "timeout": 5,
                "message": "编码问题：使用安全解码"
            }
        }
        
        for p in pattern["patterns"]:
            if p in solutions:
                return solutions[p]
        
        return {
            "strategy": "generic_retry",
            "timeout": 10,
            "message": "通用策略：温和重试"
        }

# ============== Phase 2: 成功模式学习 ==============
class SuccessLearner:
    """成功模式学习器"""
    
    @staticmethod
    def record_success(action, context, result):
        """记录成功模式"""
        return {
            "action": action,
            "context": context,
            "result": result,
            "timestamp": datetime.now().isoformat(),
            "success_score": result.get("success_rate", 1.0)
        }

# ============== Phase 3: 改进建议生成 ==============
class ImprovementGenerator:
    """改进建议生成器"""
    
    @staticmethod
    def generate_improvements(learning_data):
        """基于学习数据生成改进建议"""
        improvements = []
        
        # 基于错误模式生成建议
        error_counts = {}
        for error in learning_data.data.get("error_patterns", []):
            for p in error.get("patterns", []):
                error_counts[p] = error_counts.get(p, 0) + 1
        
        # 常见错误优先处理
        sorted_errors = sorted(error_counts.items(), key=lambda x: x[1], reverse=True)
        
        for error_type, count in sorted_errors[:3]:
            improvements.append({
                "type": "error_prevention",
                "priority": count,
                "error_type": error_type,
                "suggestion": ImprovementGenerator.get_suggestion(error_type),
                "implementation": ImprovementGenerator.get_implementation(error_type)
            })
        
        return improvements
    
    @staticmethod
    def get_suggestion(error_type):
        """获取错误类型对应的建议"""
        suggestions = {
            "network": "增加网络请求的超时时间和重试次数",
            "api": "实现 API 密钥自动刷新和错误处理",
            "file": "添加文件路径验证和权限检查",
            "memory": "优化内存使用，分批处理大数据",
            "encoding": "统一使用 UTF-8 编码，添加错误回退"
        }
        return suggestions.get(error_type, "添加通用错误处理")
    
    @staticmethod
    def get_implementation(error_type):
        """获取错误类型对应的实现方案"""
        implementations = {
            "network": """
def safe_request(url, retries=3):
    for i in range(retries):
        try:
            return requests.get(url, timeout=30)
        except requests.exceptions.RequestException as e:
            if i == retries - 1:
                raise
            sleep(2 ** i)  # 指数退避
""",
            "api": """
def check_api_health(client):
    try:
        result = client.test()
        return result.status == "healthy"
    except Exception as:
        refresh_token()
        return False
""",
            "file": """
def safe_read(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Path not found: {path}")
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()
""",
            "encoding": """
def safe_decode(data):
    try:
        return data.decode('utf-8')
    except UnicodeDecodeError:
        return data.decode('utf-8', errors='ignore')
""",
            "memory": """
def process_large_file(path, chunk_size=1000):
    with open(path, 'r', encoding='utf-8') as f:
        while True:
            chunk = f.readlines(chunk_size)
            if not chunk:
                break
            yield chunk
"""
        }
        return implementations.get(error_type, "通用错误处理代码")

# ============== Phase 4: 自动化改进执行 ==============
class AutoImprover:
    """自动化改进执行器"""
    
    def __init__(self, learning_data):
        self.data = learning_data
        self.improvements_applied = []
    
    def apply_improvement(self, improvement):
        """应用改进"""
        # 记录改进
        self.improvements_applied.append({
            "improvement": improvement,
            "applied_at": datetime.now().isoformat(),
            "status": "pending"
        })
        
        # 这里可以自动更新配置文件、脚本等
        # 简化版：只记录
        return f"已记录改进建议: {improvement['type']} - {improvement['error_type']}"

# ============== Phase 5: 自我评估 ==============
class SelfEvaluator:
    """自我评估器"""
    
    @staticmethod
    def evaluate_performance(learning_data):
        """评估系统表现"""
        metrics = learning_data.data.get("metrics", {})
        
        return {
            "success_rate": metrics.get("success_rate", 0.0),
            "total_tasks": metrics.get("total_tasks", 0),
            "error_count": len(learning_data.data.get("error_patterns", [])),
            "improvement_count": len(learning_data.data.get("improvements", [])),
            "health_score": SelfEvaluator.calculate_health(metrics)
        }
    
    @staticmethod
    def calculate_health(metrics):
        """计算健康分数"""
        success = metrics.get("success_rate", 0.5)
        errors = metrics.get("total_tasks", 1)
        
        # 健康分数 = 成功率 - 错误率惩罚
        health = success * 100
        
        if errors > 10:
            health -= 10  # 错误太多扣分
        
        return max(0, min(100, health))

# ============== Phase 6: 报告生成 ==============
class EvolutionReport:
    """进化报告生成器"""
    
    @staticmethod
    def generate_report(learning_data, improvements, evaluation):
        """生成自我进化报告"""
        
        report = f"""
{'='*60}
OpenClaw Self-Evolution Report
自我改进与学习系统报告
{'='*60}

[系统状态]
生成时间: {datetime.now().isoformat()}
版本: {learning_data.data.get('version', '1.0')}
上次更新: {learning_data.data.get('last_updated', '未知')}

[性能指标]
总任务数: {evaluation['total_tasks']}
成功率: {evaluation['success_rate']:.1%}
错误次数: {evaluation['error_count']}
改进次数: {evaluation['improvement_count']}
健康分数: {evaluation['health_score']:.1f}/100

[错误模式分析]
"""
        
        # 错误模式统计
        error_counts = {}
        for error in learning_data.data.get("error_patterns", []):
            for p in error.get("patterns", []):
                error_counts[p] = error_counts.get(p, 0) + 1
        
        for error_type, count in sorted(error_counts.items(), key=lambda x: x[1], reverse=True):
            report += f"  - {error_type}: {count} 次\n"
        
        report += f"""
[改进建议]
"""
        
        for i, imp in enumerate(improvements[:5], 1):
            report += f"""
{i}. [{imp['type']}] {imp['error_type']}
   优先级: {imp['priority']}
   建议: {imp['suggestion']}
   实现方案:
   {imp['implementation'][:200]}...
"""
        
        report += f"""
[下一步行动]
"""
        
        next_actions = [
            "审查并应用高优先级改进建议",
            "更新错误处理代码",
            "配置自动化监控",
            "定期运行自我评估"
        ]
        
        for i, action in enumerate(next_actions, 1):
            report += f"  {i}. {action}\n"
        
        report += f"""
{'='*60}
"自我改进是系统持续进化的核心"
{'='*60}
"""
        
        return report

# ============== 主流程 ==============
def main():
    print("="*60)
    print("OpenClaw Self-Evolving System")
    print("自我改进与学习系统演示")
    print("="*60)
    
    # 1. 加载学习数据
    print("\n[Phase 1: 加载学习数据]")
    learning_data = LearningData()
    print(f"已加载 {len(learning_data.data.get('error_patterns', []))} 条错误记录")
    print(f"已记录 {len(learning_data.data.get('success_patterns', []))} 条成功模式")
    
    # 2. 模拟错误分析
    print("\n[Phase 2: 模拟错误分析]")
    test_errors = [
        ("Network timeout while connecting to API", "openai-whisper 转写"),
        ("File not found: C:\\Users\\殇\\test.txt", "文件读取"),
        ("API rate limit exceeded", "Tavily 搜索"),
        ("UnicodeDecodeError: 'gbk' codec can't decode", "文件编码")
    ]
    
    for error_msg, context in test_errors:
        error = ErrorAnalyzer.analyze_error(error_msg, context)
        learning_data.data["error_patterns"].append(error)
        
        solution = ErrorAnalyzer.generate_solution(error)
        print(f"  - 错误: {error_msg[:40]}...")
        print(f"    模式: {error['patterns']}")
        print(f"    方案: {solution['message']}")
    
    # 3. 生成改进建议
    print("\n[Phase 3: 生成改进建议]")
    improvements = ImprovementGenerator.generate_improvements(learning_data)
    print(f"生成 {len(improvements)} 条改进建议:")
    
    for i, imp in enumerate(improvements[:3], 1):
        print(f"  {i}. [{imp['type']}] {imp['error_type']}")
        print(f"     建议: {imp['suggestion'][:50]}...")
    
    # 4. 应用改进
    print("\n[Phase 4: 应用改进]")
    improver = AutoImprover(learning_data)
    
    for imp in improvements[:2]:  # 应用前2条
        result = improver.apply_improvement(imp)
        print(f"  [OK] {result}")
    
    # 5. 自我评估
    print("\n[Phase 5: 自我评估]")
    evaluation = SelfEvaluator.evaluate_performance(learning_data)
    print(f"  成功率: {evaluation['success_rate']:.1%}")
    print(f"  错误次数: {evaluation['error_count']}")
    print(f"  健康分数: {evaluation['health_score']:.1f}/100")
    
    # 6. 保存数据
    print("\n[Phase 6: 保存学习数据]")
    learning_data.save()
    print(f"  [OK] 已保存到: {LEARNING_DATA}")
    
    # 7. 生成报告
    print("\n[Phase 7: 生成进化报告]")
    report = EvolutionReport.generate_report(learning_data, improvements, evaluation)
    print(report)
    
    # 8. 保存报告
    report_path = f"{WORKSPACE}/self_evolution_report.txt"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\n报告已保存到: {report_path}")
    
    return {
        "learning_data": learning_data,
        "improvements": improvements,
        "evaluation": evaluation,
        "report": report
    }

if __name__ == "__main__":
    main()
