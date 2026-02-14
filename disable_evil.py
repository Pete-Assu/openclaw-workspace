import json

config_path = r'C:\Users\殇\.openclaw\openclaw.json'
with open(config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Check hooks config
hooks = config.get('hooks', {})
internal = hooks.get('internal', {})
entries = internal.get('entries', {})

print('Current Hooks:')
for name, conf in entries.items():
    enabled = conf.get('enabled', True)
    status = 'ON' if enabled else 'OFF'
    print(f'  {name}: {status}')

# Add soul-evil as disabled
entries['soul-evil'] = {'enabled': False}
print('\nAdded soul-evil as DISABLED')

with open(config_path, 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

print('Config saved!')
