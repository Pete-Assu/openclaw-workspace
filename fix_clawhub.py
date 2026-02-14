#!/usr/bin/env python3
"""Fix ClawHub endpoint in openclaw.json"""

import json

config_path = r'C:\Users\殇\.openclaw\openclaw.json'

with open(config_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix ClawHub URLs
old = 'https://clawhub.com'
new = 'https://clawhub.ai'

if old in content:
    content = content.replace(old, new)
    print(f'Fixed: {old} -> {new}')
    
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print('Config saved!')
else:
    print('No ClawHub URL found to fix')
