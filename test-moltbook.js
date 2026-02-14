/**
 * 测试 Moltbook API 连接
 */

const https = require('https');

const API_KEY = process.env.MOLTBOOK_API_KEY || 'moltbook_sk_oyiwn5NTjQVqrdoThu4XTGutzwpeyfEU';
const BASE_URL = 'www.moltbook.com';

function apiRequest(path) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: BASE_URL,
      port: 443,
      path: path,
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 'application/json'
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          resolve(data);
        }
      });
    });

    req.on('error', reject);
    req.end();
  });
}

async function test() {
  console.log('测试 Moltbook API...\n');

  try {
    // 1. 热门帖子
    console.log('1. 获取热门技能...');
    const hot = await apiRequest('/api/v1/posts?sort=hot&limit=10');
    console.log(`   找到 ${hot.data?.length || 0} 个热门帖子`);
    
    if (hot.data?.length > 0) {
      console.log('\n   前5个:');
      hot.data.slice(0, 5).forEach((post, i) => {
        console.log(`   ${i+1}. [${post.votes || 0} 👍] ${post.title?.substring(0, 50)}`);
      });
    }

    // 2. 搜索 OpenClaw 技能
    console.log('\n2. 搜索 OpenClaw 相关...');
    const search = await apiRequest('/api/v1/search?q=OpenClaw+skill&limit=10');
    console.log(`   找到 ${search.data?.length || 0} 个结果`);

    // 3. 我的 submolts
    console.log('\n3. 获取 submolts...');
    const submolts = await apiRequest('/api/v1/submolts');
    console.log(`   找到 ${submolts.data?.length || 0} 个 submolts`);
    
    if (submolts.data?.length > 0) {
      submolts.data.slice(0, 5).forEach((sub, i) => {
        console.log(`   ${i+1}. ${sub.name} (${sub.memberCount} 成员)`);
      });
    }

    console.log('\n✅ API 连接成功！');
    
  } catch (error) {
    console.log(`❌ API 错误: ${error.message}`);
  }
}

test();
