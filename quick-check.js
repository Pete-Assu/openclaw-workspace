const https = require('https');

(async () => {
  const platforms = [
    { name: 'Moltbook', url: 'https://www.moltbook.com/api/v1/posts?limit=1' },
    { name: 'GitHub', url: 'https://api.github.com/rate_limit' },
    { name: 'ClawHub', url: 'https://clawhub.com/api/v1/skills' }
  ];

  console.log('🔍 平台连通性检查\n');

  for (const p of platforms) {
    try {
      const req = https.get(p.url, { timeout: 5000 }, (res) => {
        console.log(`✅ ${p.name}: ${res.statusCode}`);
        res.resume();
        res.on('end', () => {});
      });
      req.on('error', () => console.log(`❌ ${p.name}: 失败`));
      req.on('timeout', () => { req.destroy(); console.log(`❌ ${p.name}: 超时`); });
      req.end();
    } catch (e) {
      console.log(`❌ ${p.name}: ${e.message}`);
    }
  }
})();
