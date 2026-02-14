import json
import re

with open(r'C:\Users\殇\.openclaw\agents\main\sessions\7f77628d-15e8-4b89-b160-7b08be201d4a.jsonl', 'r', encoding='utf-8') as f:
    lines = f.readlines()

url_pattern = r'https?://[^\s<>"\'\\]+'
found = []

for i, line in enumerate(lines):
    try:
        data = json.loads(line)
        if 'message' in data and 'content' in data['message']:
            content = str(data['message']['content'])
            if 'cloud.tencent.com' in content.lower():
                urls = re.findall(url_pattern, content)
                for url in urls:
                    if 'cloud.tencent' in url.lower():
                        found.append((i, url))
                        print(f'Line {i}: {url}')

        if 'content' in data:
            content = str(data['content'])
            if 'cloud.tencent.com' in content.lower():
                urls = re.findall(url_pattern, content)
                for url in urls:
                    if 'cloud.tencent' in url.lower():
                        found.append((i, url))
                        print(f'Line {i}: {url}')
    except:
        pass

if not found:
    print('No cloud.tencent URLs found')
