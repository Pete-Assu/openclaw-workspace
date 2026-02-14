import json

# Search for tencent in all session files
files = [
    r'C:\Users\殇\.openclaw\agents\main\sessions\5e50b320-1661-4e62-aa18-b5e2886fb8d5.jsonl',
    r'C:\Users\殇\.openclaw\agents\main\sessions\0ad78a2e-145d-4f1f-815c-1f46b15c37ed.jsonl'
]

for filepath in files:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        print(f'\n=== {filepath.split(chr(92))[-1]} ===')
        print(f'Total lines: {len(lines)}')

        found = False
        for i, line in enumerate(lines):
            try:
                data = json.loads(line)
                if 'message' in data and 'content' in data['message']:
                    content = str(data['message']['content'])
                    if '腾讯' in content or 'cloud.tencent' in content.lower():
                        print(f'\nLine {i}:')
                        print(content[:500])
                        found = True
            except:
                pass

        if not found:
            print('No matches found')
    except Exception as e:
        print(f'Error reading {filepath}: {e}')
