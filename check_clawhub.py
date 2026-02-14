import http.client
import socket

# Check ClawHub redirect chain
host = 'clawhub.com'
paths = ['/api/v1/skills', '/skills', '/']

print('ClawHub redirect check')
print('='*50)

for path in paths:
    try:
        conn = http.client.HTTPSConnection(host, timeout=10)
        conn.request('HEAD', path)
        resp = conn.getresponse()
        location = resp.getheader('location', '')
        print(f'{path:20} -> {resp.status} {location[:50]}')
    except Exception as e:
        print(f'{path:20} -> Error: {str(e)[:30]}')
