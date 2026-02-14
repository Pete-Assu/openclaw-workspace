/**
 * 测试 Moltbook API - 多种格式
 */

const https = require('https');

const API_KEY = 'moltbook_sk_oyiwn5NTjQVqrdoThu4XTGutzwpeyfEU';

function apiRequest(path) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'www.moltbook.com',
      port: 443,
      path: path,
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Accept': 'application/json'
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        console.log(`   状态: ${res.statusCode}, 内容: ${data.substring(0, 300)}`);
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          resolve({ raw: data, status: res.statusCode });
        }
      });
    });

    req.on('error', reject);
    req.end();
  });
}

async function test() {
  console.log('测试不同 API 路径...\n');

  const paths = [
    '/api/v1/posts?sort=hot',
    '/api/v1/feed',
    '/api/v1/skills/trending',
    '/api/v1/explore/skills',
    '/api/v1/search?q=agent',
  ];

  for (const path of paths) {
    console.log(`测试: ${path}`);
    try {
      await apiRequest(path);
    } catch (e) {
      console.log(`   错误: ${e.message}`);
    }
    console.log('');
  }
}

test();
