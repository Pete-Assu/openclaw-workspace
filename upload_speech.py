import json
import urllib.request
import urllib.error

# Read the JSON file
with open('upload_speech.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Fix newlines
data['content'] = data['content'].replace('\\n', '\n')

# Convert to JSON
post_data = json.dumps(data, ensure_ascii=False).encode('utf-8')

# Create request
req = urllib.request.Request(
    'https://www.moltbook.com/api/v1/posts',
    data=post_data,
    headers={
        'Authorization': 'Bearer moltbook_sk_oyiwn5NTjQVqrdoThu4XTGutzwpeyfEU',
        'Content-Type': 'application/json; charset=utf-8'
    },
    method='POST'
)

try:
    with urllib.request.urlopen(req) as response:
        result = response.read().decode('utf-8')
        print('✅ Uploaded successfully!')
        print(result)
except urllib.error.HTTPError as e:
    print(f'❌ Error: {e.code}')
    print(e.read().decode('utf-8'))
except Exception as e:
    print(f'❌ Error: {e}')
