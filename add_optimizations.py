#!/usr/bin/env python3
"""添加优化配置到 openclaw.json"""

import json

# 读取当前配置
with open(r'C:\Users\殇\.openclaw\openclaw.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# 添加 contextPruning
config['agents']['defaults']['contextPruning'] = {
    'mode': 'cache-ttl',
    'ttl': '5m'
}

# 添加 heartbeat
config['agents']['defaults']['heartbeat'] = {
    'intervalMinutes': 120,
    'activeHours': {
        'start': '08:00',
        'end': '24:00',
        'timezone': 'Asia/Shanghai'
    }
}

# 添加 session reset
config['agents']['defaults']['session'] = {
    'resetMode': 'idle',
    'idleMinutes': 240
}

# 添加 inbound debounce
config['messages']['inbound'] = {
    'debounceMs': 3000
}

# 写回配置
with open(r'C:\Users\殇\.openclaw\openclaw.json', 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

print('✅ 配置已更新！')
