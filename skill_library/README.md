# OpenClaw All-in-One Skill Library

**OpenClaw 全功能技能库** - 整合所有自动化能力

## 📋 Library Metadata

- **Library Version:** 1.0.0
- **Created:** 2026-02-10
- **Author:** MoltClaw_Shang
- **Status:** Active

## 🎯 整合的技能模块

### 1. 🤖 Proactive Agent（主动式代理）
- **文件:** `proactive_agent.py`
- **功能:** 主动检测机会、自动提案、自治度决策
- **依赖:** 无

### 2. 🔍 Tavily Search（深度搜索）
- **文件:** `tavily_search.py`
- **功能:** AI 优化搜索引擎、多角度研究
- **依赖:** tavily-python

### 3. 🧠 Self-Evolving System（自我改进）
- **文件:** `self_evolving_v2.py`
- **功能:** 错误检测、自动修复、自愈循环、定期自检
- **依赖:** 无

### 4. 🎙️ OGG Speech Parser（语音转写）
- **文件:** `transcribe.py`
- **功能:** OGG 语音转文本、本地 Whisper
- **依赖:** openai-whisper, librosa

## 📁 文件结构

```
skill_library/
├── README.md                    # 本文档
├── proactive_agent.py          # 主动式代理模块
├── tavily_search.py            # 深度搜索模块
├── self_evolving_v2.py         # 自我改进模块
├── transcribe.py               # 语音转写模块
├── learning_data.json          # 学习数据库
├── auto_fixes.py              # 自动修复代码库
└── health_metrics.json         # 健康指标
```

## 🚀 快速开始

### 方法 1: 导入整个技能库

```python
from skill_library import OpenClawAllInOne

# 初始化
agent = OpenClawAllInOne()

# 运行主动式代理
agent.run_proactive_mode()

# 进行深度搜索
results = agent.tavily_search("OpenClaw automation")

# 语音转写
text = agent.transcribe_ogg("audio.ogg")

# 自我修复
agent.self_heal_on_error(error_msg)
```

### 方法 2: 单独使用模块

```python
# 主动式代理
from skill_library.proactive_agent import ProactiveAgent
agent = ProactiveAgent()
agent.detect_opportunities()

# 深度搜索
from skill_library.tavily_search import TavilySearch
search = TavilySearch(api_key="your-key")
results = search.deep_research("topic")

# 自我改进
from skill_library.self_evolving_v2 import SelfEvolvingSystem
system = SelfEvolvingSystem()
system.run_self_inspection()
```

## 📊 健康分数目标: 100/100

### 当前状态

| 指标 | 当前 | 目标 | 状态 |
|------|------|------|------|
| Proactive Mode | ✅ | ✅ | 已完成 |
| Tavily Search | ✅ | ✅ | 已完成 |
| Self-Evolving | ✅ | ✅ | 已完成 |
| OGG Parser | ✅ | ✅ | 已完成 |
| 集成度 | 🔄 45% | 100% | 进行中 |
| 自动修复 | ✅ | ✅ | 已完成 |

### 提升方案

1. **整合所有模块** (当前进行中)
2. **添加更多自动修复** (12/18 = 66%)
3. **增加成功案例** (当前 100%)
4. **持续自检** (需要定期运行)

## 🎯 核心功能详解

### Proactive Agent 模块

```python
class ProactiveAgent:
    def detect_opportunities(self):
        """检测用户需求和机会"""
        
    def generate_proposal(self, opportunity):
        """生成主动提案"""
        
    def execute_with_autonomy(self, proposal, level):
        """根据自治度执行"""
```

### Tavily Search 模块

```python
class TavilySearch:
    def quick_search(self, query):
        """快速搜索 (3 结果)"""
        
    def deep_research(self, topic):
        """深度研究 (10 结果)"""
        
    def multi_angle_search(self, topic):
        """多角度搜索"""
```

### Self-Evolving 模块

```python
class SelfEvolvingSystem:
    def detect_error(self, error_msg):
        """检测错误模式"""
        
    def auto_fix(self, error_pattern):
        """自动生成修复代码"""
        
    def self_inspection(self):
        """定期自检"""
        
    def get_health_score(self):
        """计算健康分数"""
```

## 📈 使用示例

### 示例 1: 完整工作流

```python
from skill_library import OpenClawAllInOne

agent = OpenClawAllInOne()

# 1. 检测机会
opportunities = agent.proactive.detect_opportunities()

# 2. 深度研究选定的机会
if opportunities:
    research = agent.tavily.deep_research(opportunities[0]['topic'])
    
# 3. 语音输入（如果有）
# text = agent.transcribe_ogg("voice.ogg")
    
# 4. 自我改进
agent.self_evolve.run_self_inspection()

# 5. 检查健康分数
health = agent.self_evolve.get_health_score()
print(f"健康分数: {health}/100")
```

### 示例 2: 错误自动修复

```python
from skill_library import SelfEvolvingSystem

system = SelfEvolvingSystem()

# 检测到错误
result = system.on_error("Network timeout...")
print(result)

# 自动生成修复
if result['fixes_applied']:
    print("已应用修复!")
```

### 示例 3: 深度研究

```python
from skill_library import TavilySearch

search = TavilySearch(api_key="tvly-dev-...")

# 多角度研究
results = search.multi_angle_search("OpenClaw automation")

# 提取关键信息
for angle, data in results.items():
    print(f"{angle}: {len(data['results'])} 条结果")
```

## 🔧 配置

### 环境变量

```bash
# Tavily API Key
export TAVILY_API_KEY="tvly-dev-..."

# OpenClaw 配置
export OPENCLAW_WORKSPACE="/path/to/workspace"
```

### 初始化配置

```python
from skill_library import OpenClawAllInOne

agent = OpenClawAllInOne(
    tavily_api_key="your-key",
    workspace="/path/to/workspace",
    auto_save=True,
    health_target=100
)
```

## 📊 监控与报告

### 健康检查

```python
# 获取完整健康报告
report = agent.get_health_report()
print(report)

# 保存到文件
agent.save_report("health_report.txt")
```

### 定期自检

```python
# 运行完整自检
inspection = agent.self_evolve.run_self_inspection()

# 获取改进建议
suggestions = agent.self_evolve.get_improvement_suggestions()
```

## 🎓 最佳实践

### 1. 定期运行自检
```bash
# 每天运行一次
python skill_library/self_evolving_v2.py
```

### 2. 主动检测机会
```python
# 每次会话开始时
agent.proactive.detect_opportunities()
```

### 3. 使用深度搜索进行研究
```python
# 当需要了解新话题时
results = agent.tavily.deep_research("new_topic")
```

### 4. 及时修复错误
```python
# 当检测到错误时
agent.self_evolve.on_error(error_msg)
```

## 🔗 相关文档

- [Proactive Agent 原始文档](../skills/proactive-agent/SKILL.md)
- [Tavily Search 原始文档](../skills/tavily-search/SKILL.md)
- [Self-Evolving 原始文档](self_evolving_v2.py)
- [OGG Parser 原始文档](../skills/ogg-speech-parser/SKILL.md)

## 📝 更新日志

### v1.0.0 (2026-02-10)
- ✨ 初始版本
- ✅ 整合 4 个核心模块
- ✅ 统一 API 接口
- ✅ 健康分数追踪
- ✅ 自动修复系统

## 🎯 目标完成度

- [x] Proactive Agent 模块
- [x] Tavily Search 模块
- [x] Self-Evolving 模块
- [x] OGG Speech Parser 模块
- [ ] 统一 API 接口 (进行中)
- [ ] 健康分数 100/100 (当前 46/100)
- [ ] 完整集成文档 (进行中)

---

**Library Version:** 1.0.0  
**Last Updated:** 2026-02-10  
**Goal:** 健康分数 100/100
