# HEARTBEAT.md

# Keep this file empty (or with only comments) to skip heartbeat API calls.

# Add tasks below when you want the agent to check something periodically.

# 记忆保存检查（每30分钟）
## 检查是否有重要信息未记录
### 触发条件：
- 刚读取外部 URL/文章
- 刚完成重要任务（超过5分钟）
- 用户说"记得..."/"记录..."
### 动作：
- 自动保存到 memory/YYYY-MM-DD.md
- 标记已保存

