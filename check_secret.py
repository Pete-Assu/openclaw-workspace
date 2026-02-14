import json

config_path = r'C:\Users\殇\.openclaw\openclaw.json'
with open(config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

secret = config.get('channels', {}).get('feishu', {}).get('appSecret', '')
if secret:
    print('App Secret (first 8 chars):', secret[:8] + '***')
    print('Secret length:', len(secret))
else:
    print('No App Secret found')
