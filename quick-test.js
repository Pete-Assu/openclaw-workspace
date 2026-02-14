const fetch = require('./libs/skill-scanner.js').fetch || null;

// 简化测试
(async () => {
  console.log('🔍 测试平台连通性...\n');
  
  const tests = [
    { name: 'Moltbook', url: 'https://www.moltbook.com/api/v1/posts?limit=1' },
    { name: 'GitHub', url: 'https://api.github.com/rate_limit' },
    { name: 'ClawHub', url: 'https://clawhub.com/api/v1/skills' }
  ];
  
  for (const test of tests) {
    console.log(`测试: ${test.name}`);
    try {
      const https = require('https');
      const req = https.get(test.url, { timeout: 5000 }, (res) => {
        console.log(`   ${res.statusCode}`);
        res.resume();
        res.on('end', () => console.log(`   完成`));
      });
      req.on('error', (e) => console.log(`   错误: ${e.message}`));
      req.on('timeout', () => { req.destroy(); console.log(`   超时`); });
    } catch (e) {
      console.log(`   异常: ${e.message}`);
    }
  }
})();
