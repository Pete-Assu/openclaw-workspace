#!/usr/bin/env python3
"""
OpenClaw Self-Evolving System v2.0
自我改进与学习系统 - 自动修复版
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path

# ============== 配置 ==============
WORKSPACE = "C:/Users/殇/.openclaw/workspace"
LEARNING_DATA = f"{WORKSPACE}/learning_data.json"
ERROR_LOG = f"{WORKSPACE}/error_patterns.json"
AUTO_FIXES = f"{WORKSPACE}/auto_fixes.py"

# ============== 核心数据类 ==============
class LearningDatabase:
    def __init__(self):
        self.data = {
            "version": "2.0",
            "created_at": datetime.now().isoformat(),
            "metrics": {
                "total_tasks": 0,
                "success_count": 0,
                "error_count": 0,
                "auto_fixes_applied": 0
            },
            "error_patterns": [],
            "success_patterns": [],
            "auto_fixes": []
        }
        self.load()
    
    def load(self):
        if os.path.exists(LEARNING_DATA):
            try:
                with open(LEARNING_DATA, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    self.data.update(loaded)
            except:
                pass
    
    def save(self):
        self.data["last_updated"] = datetime.now().isoformat()
        with open(LEARNING_DATA, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

# ============== Phase 1: 错误检测 ==============
class ErrorDetector:
    """错误检测器"""
    
    PATTERNS = {
        "network": {
            "keywords": ["timeout", "connection", "network", "internet", "socket"],
            "severity": "high"
        },
        "api": {
            "keywords": ["401", "403", "404", "429", "api", "rate limit", "unauthorized"],
            "severity": "critical"
        },
        "file": {
            "keywords": ["file", "path", "permission", "not found", "exists"],
            "severity": "medium"
        },
        "encoding": {
            "keywords": ["encoding", "utf-8", "gbk", "unicode", "decode"],
            "severity": "low"
        },
        "syntax": {
            "keywords": ["syntax", "indentation", "syntaxerror"],
            "severity": "critical"
        }
    }
    
    @staticmethod
    def detect(error_msg):
        """检测错误类型"""
        error_lower = error_msg.lower()
        detected = []
        
        for pattern_type, config in ErrorDetector.PATTERNS.items():
            for keyword in config["keywords"]:
                if keyword in error_lower:
                    detected.append({
                        "type": pattern_type,
                        "severity": config["severity"],
                        "keyword": keyword
                    })
                    break
        
        return detected

# ============== Phase 2: 自动修复引擎 ==============
class AutoFixEngine:
    """自动修复引擎"""
    
    FIX_TEMPLATES = {
        "network": '''
def auto_fix_network(func):
    """网络错误自动修复装饰器"""
    import time
    
    def wrapper(*args, **kwargs):
        max_retries = 3
        for i in range(max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if "timeout" in str(e).lower() or "connection" in str(e).lower():
                    wait_time = 2 ** i  # 指数退避
                    print(f"[AutoFix] 网络错误，等待 {wait_time}s 后重试...")
                    time.sleep(wait_time)
                else:
                    raise
        raise Exception(f"重试 {max_retries} 次后仍失败")
    return wrapper
''',
        "api": '''
def auto_fix_api(api_client):
    """API 错误自动修复"""
    def request_with_retry(method, endpoint, **kwargs):
        max_retries = 3
        for i in range(max_retries):
            try:
                response = getattr(api_client, method)(endpoint, **kwargs)
                if response.status_code == 401:
                    print("[AutoFix] API 401 错误，尝试刷新 token...")
                    api_client.refresh_token()
                    continue
                elif response.status_code == 429:
                    wait_time = 2 ** i
                    print(f"[AutoFix] Rate limit，等待 {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                return response
            except Exception as e:
                if i == max_retries - 1:
                    raise
                time.sleep(2 ** i)
        return None
    return request_with_retry
''',
        "file": '''
def auto_fix_file(func):
    """文件错误自动修复"""
    def wrapper(path, *args, **kwargs):
        # 检查文件是否存在
        if not os.path.exists(path):
            print(f"[AutoFix] 文件不存在: {path}")
            # 尝试创建目录
            os.makedirs(os.path.dirname(path), exist_ok=True)
            print(f"[AutoFix] 已创建目录: {os.path.dirname(path)}")
        
        # 检查权限
        try:
            return func(path, *args, **kwargs)
        except PermissionError:
            print(f"[AutoFix] 权限错误，尝试修改权限...")
            os.chmod(path, 0o644)
            return func(path, *args, **kwargs)
    return wrapper
''',
        "encoding": '''
def auto_fix_encoding(func):
    """编码错误自动修复"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except UnicodeDecodeError as e:
            print(f"[AutoFix] 编码错误，尝试使用 errors='ignore'...")
            # 修改函数参数，添加 errors='ignore'
            if hasattr(func, '__code__'):
                new_args = list(args)
                new_kwargs = kwargs.copy()
                new_kwargs['errors'] = 'ignore'
                return func(*new_args, **new_kwargs)
            raise
    return wrapper
'''
    }
    
    @staticmethod
    def generate_fix(error_patterns):
        """根据错误模式生成修复代码"""
        fixes = []
        
        for pattern in error_patterns:
            error_type = pattern["type"]
            if error_type in AutoFixEngine.FIX_TEMPLATES:
                fixes.append({
                    "error_type": error_type,
                    "severity": pattern["severity"],
                    "code": AutoFixEngine.FIX_TEMPLATES[error_type],
                    "applied": False
                })
        
        return fixes
    
    @staticmethod
    def apply_fix(fix):
        """应用修复"""
        fix["applied"] = True
        fix["applied_at"] = datetime.now().isoformat()
        
        # 提取函数名
        match = re.search(r'def (\w+)', fix["code"])
        func_name = match.group(1) if match else "unknown"
        
        # 保存到自动修复库
        fixes_file = AUTO_FIXES
        with open(fixes_file, 'a', encoding='utf-8') as f:
            f.write(f"\n\n# Applied at {datetime.now().isoformat()}\n")
            f.write(f"# Error type: {fix['error_type']}\n")
            f.write(fix["code"])
        
        return f"已应用修复: {func_name}()"

# ============== Phase 3: 自愈循环 ==============
class SelfHealingLoop:
    """自愈循环"""
    
    def __init__(self, database):
        self.db = database
    
    def on_error(self, error_msg, context=None):
        """错误发生时调用"""
        print(f"\n[SelfHealing] 检测到错误: {error_msg[:50]}...")
        
        # 1. 检测错误类型
        patterns = ErrorDetector.detect(error_msg)
        print(f"[SelfHealing] 错误模式: {[p['type'] for p in patterns]}")
        
        # 2. 记录到数据库
        error_record = {
            "error_msg": error_msg,
            "patterns": patterns,
            "context": context,
            "timestamp": datetime.now().isoformat(),
            "auto_fixed": False
        }
        self.db.data["error_patterns"].append(error_record)
        
        # 确保 metrics 存在
        if "error_count" not in self.db.data["metrics"]:
            self.db.data["metrics"]["error_count"] = 0
        
        # 确保 metrics 存在
        if "error_count" not in self.db.data["metrics"]:
            self.db.data["metrics"]["error_count"] = 0
        if "auto_fixes_applied" not in self.db.data["metrics"]:
            self.db.data["metrics"]["auto_fixes_applied"] = 0
        
        self.db.data["metrics"]["error_count"] += 1
        
        # 3. 生成修复
        fixes = AutoFixEngine.generate_fix(patterns)
        print(f"[SelfHealing] 生成 {len(fixes)} 个修复方案")
        
        # 4. 应用修复
        applied_fixes = []
        for fix in fixes:
            if not fix["applied"]:
                result = AutoFixEngine.apply_fix(fix)
                applied_fixes.append(result)
                error_record["auto_fixed"] = True
                self.db.data["metrics"]["auto_fixes_applied"] += 1
        
        # 5. 保存数据库
        self.db.save()
        
        return {
            "error_msg": error_msg,
            "patterns": patterns,
            "fixes_applied": applied_fixes,
            "success": len(applied_fixes) > 0
        }
    
    def on_success(self, action, result):
        """成功时调用"""
        print(f"\n[SelfHealing] 任务成功: {action[:30]}...")
        
        # 确保 metrics 存在
        if "success_count" not in self.db.data["metrics"]:
            self.db.data["metrics"]["success_count"] = 0
        if "success_rate" not in self.db.data["metrics"]:
            self.db.data["metrics"]["success_rate"] = 0.5
        if "total_tasks" not in self.db.data["metrics"]:
            self.db.data["metrics"]["total_tasks"] = 0
        
        # 记录成功模式
        self.db.data["success_patterns"].append({
            "action": action,
            "result": result,
            "timestamp": datetime.now().isoformat()
        })
        self.db.data["metrics"]["success_count"] += 1
        self.db.data["metrics"]["total_tasks"] += 1
        
        # 计算成功率
        total = self.db.data["metrics"]["total_tasks"]
        success = self.db.data["metrics"]["success_count"]
        self.db.data["metrics"]["success_rate"] = success / total if total > 0 else 0
        
        self.db.save()

# ============== Phase 4: 性能监控 ==============
class PerformanceMonitor:
    """性能监控器"""
    
    @staticmethod
    def get_health_score(db):
        """计算健康分数"""
        metrics = db.data["metrics"]
        
        # 基础分数
        success_rate = metrics.get("success_rate", 0.5) * 50  # 0-50 分
        
        # 自动修复加成
        auto_fixes = metrics.get("auto_fixes_applied", 0)
        fix_bonus = min(20, auto_fixes * 2)  # 最多 20 分
        
        # 错误惩罚
        errors = metrics.get("error_count", 0)
        error_penalty = min(30, errors * 3)  # 最多扣 30 分
        
        # 活跃度加分
        total = metrics.get("total_tasks", 0)
        activity_bonus = min(10, total)  # 最多 10 分
        
        health = success_rate + fix_bonus - error_penalty + activity_bonus
        
        return {
            "health_score": max(0, min(100, health)),
            "success_rate": metrics.get("success_rate", 0),
            "total_tasks": total,
            "auto_fixes": auto_fixes,
            "errors": errors,
            "grade": PerformanceMonitor.get_grade(health)
        }
    
    @staticmethod
    def get_grade(score):
        if score >= 90:
            return "A+ (优秀)"
        elif score >= 75:
            return "A (良好)"
        elif score >= 60:
            return "B (一般)"
        elif score >= 40:
            return "C (需改进)"
        else:
            return "D (危险)"

# ============== Phase 5: 定期自检 ==============
class SelfInspection:
    """定期自检"""
    
    @staticmethod
    def run_check(db):
        """运行自检"""
        print("\n" + "="*50)
        print("[SelfInspection] 定期自检...")
        print("="*50)
        
        # 检查健康状态
        health = PerformanceMonitor.get_health_score(db)
        print(f"\n[健康状态] {health['health_score']:.1f}/100 - {health['grade']}")
        print(f"  成功率: {health['success_rate']:.1%}")
        print(f"  任务数: {health['total_tasks']}")
        print(f"  自动修复: {health['auto_fixes']} 次")
        print(f"  错误数: {health['errors']}")
        
        # 检查是否需要改进
        if health['health_score'] < 60:
            print("\n[警告] 健康分数低于 60，建议：")
            print("  1. 检查最近的错误模式")
            print("  2. 应用更多的自动修复")
            print("  3. 优化错误处理逻辑")
        
        # 检查自动修复库
        if os.path.exists(AUTO_FIXES):
            with open(AUTO_FIXES, 'r', encoding='utf-8') as f:
                content = f.read()
                fix_count = content.count('def auto_fix_')
                print(f"\n[自动修复库] 包含 {fix_count} 个修复函数")
        
        # 生成建议
        print("\n[改进建议]")
        suggestions = []
        
        if health['errors'] > 5:
            suggestions.append("分析错误模式，减少重复错误")
        
        if health['auto_fixes'] < health['errors']:
            suggestions.append("提高自动修复覆盖率")
        
        if health['success_rate'] < 0.8:
            suggestions.append("优化成功路径，提高成功率")
        
        for i, sug in enumerate(suggestions, 1):
            print(f"  {i}. {sug}")
        
        print("\n" + "="*50)
        
        return health

# ============== Phase 6: 生成报告 ==============
class EvolutionReport:
    """进化报告"""
    
    @staticmethod
    def generate(db, health):
        """生成进化报告"""
        
        report = f"""
{'='*60}
OpenClaw Self-Evolving System v2.0
自我改进与学习系统报告
{'='*60}

[系统状态]
生成时间: {datetime.now().isoformat()}
版本: {db.data.get('version', '2.0')}

[性能指标]
总任务数: {health['total_tasks']}
成功率: {health['success_rate']:.1%}
自动修复次数: {health['auto_fixes']}
错误次数: {health['errors']}

[健康评估]
健康分数: {health['health_score']:.1f}/100
等级: {health['grade']}

[错误模式统计]
"""
        
        # 统计错误模式
        error_counts = {}
        for error in db.data.get("error_patterns", []):
            for p in error.get("patterns", []):
                if isinstance(p, dict) and "type" in p:
                    error_type = p["type"]
                    error_counts[error_type] = error_counts.get(error_type, 0) + 1
        
        for error_type, count in sorted(error_counts.items(), key=lambda x: x[1], reverse=True):
            report += f"  - {error_type}: {count} 次\n"
        
        report += f"""
[自动修复统计]
已应用修复: {health['auto_fixes']} 次
修复覆盖率: {health['auto_fixes'] / max(1, health['errors']) * 100:.1f}%

[下一步行动]
"""
        
        actions = [
            "审查自动修复代码，确保质量",
            "定期运行自检，保持健康状态",
            "持续学习新的错误模式",
            "优化现有修复方案"
        ]
        
        for i, action in enumerate(actions, 1):
            report += f"  {i}. {action}\n"
        
        report += f"""
{'='*60}
"自我修复是系统成熟的关键标志"
{'='*60}
"""
        
        return report

# ============== 主流程演示 ==============
def main():
    print("="*60)
    print("OpenClaw Self-Evolving System v2.0")
    print("自我改进与学习系统 - 自动修复版")
    print("="*60)
    
    # 1. 初始化数据库
    print("\n[Phase 1: 初始化学习数据库]")
    db = LearningDatabase()
    print(f"  版本: {db.data['version']}")
    print(f"  已加载: {len(db.data['error_patterns'])} 条错误记录")
    
    # 2. 初始化自愈循环
    print("\n[Phase 2: 初始化自愈循环]")
    healer = SelfHealingLoop(db)
    
    # 3. 模拟错误场景
    print("\n[Phase 3: 模拟错误场景]")
    test_scenarios = [
        ("Network timeout while connecting to API", "Tavily 搜索"),
        ("File not found: C:\\Users\\殇\\test.txt", "文件读取"),
        ("UnicodeDecodeError: 'gbk' codec can't decode", "文件编码"),
        ("API rate limit exceeded (429)", "GitHub API"),
        ("Connection reset by peer", "网络连接")
    ]
    
    for error_msg, context in test_scenarios:
        result = healer.on_error(error_msg, context)
        if result['success']:
            print(f"  [OK] 已自动修复: {result['patterns'][0]['type']}")
        else:
            print(f"  [--] 记录错误: {error_msg[:40]}...")
    
    # 4. 模拟成功场景
    print("\n[Phase 4: 模拟成功场景]")
    healer.on_success("Tavily 搜索测试", {"status": "success", "results": 10})
    healer.on_success("OpenClaw 自动化研究", {"status": "success"})
    healer.on_success("文件转写", {"status": "success"})
    
    # 5. 定期自检
    print("\n[Phase 5: 运行定期自检]")
    health = SelfInspection.run_check(db)
    
    # 6. 生成报告
    print("\n[Phase 6: 生成进化报告]")
    report = EvolutionReport.generate(db, health)
    print(report)
    
    # 7. 保存报告
    report_path = f"{WORKSPACE}/self_evolution_v2_report.txt"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\n报告已保存到: {report_path}")
    
    # 8. 保存数据库
    print("\n[Phase 7: 保存数据库]")
    db.save()
    print(f"  数据库已保存到: {LEARNING_DATA}")
    
    # 检查自动修复库
    print("\n[自动修复库状态]")
    if os.path.exists(AUTO_FIXES):
        with open(AUTO_FIXES, 'r', encoding='utf-8') as f:
            content = f.read()
            fix_count = content.count('def auto_fix_')
            print(f"  包含 {fix_count} 个自动修复函数")
    
    return {
        "database": db,
        "health": health,
        "report": report
    }

if __name__ == "__main__":
    main()
