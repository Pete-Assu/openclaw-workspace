import json

config_path = r'C:\Users\殇\.openclaw\openclaw.json'
with open(config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

feishu = config.get('channels', {}).get('feishu', {})
print('Feishu 配置:')
print('  App ID:', feishu.get('appId', '缺失'))
print('  App Secret:', '已配置' if feishu.get('appSecret') else '缺失')
print('  Domain:', feishu.get('domain', '缺失'))
