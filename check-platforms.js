const https = require('https');

async function fetch(url, options = {}) {
  return new Promise((resolve, reject) => {
    const start = Date.now();
    
    const req = https.request(url, {
      method: 'GET',
      timeout: 8000,
      headers: {
        'Accept': 'application/json',
        'User-Agent': 'OpenClaw-Agent/1.0',
        ...options.headers
      }
    }, (res) => {
      const latency = Date.now() - start;
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        resolve({
          status: res.statusCode,
          latency: `${latency}ms`,
          data: data.substring(0, 200)
        });
      });
    });
    
    req.on('error', (err) => reject(err));
    req.on('timeout', () => { req.destroy(); reject(new Error('timeout')); });
    req.end();
  });
}

(async () => {
  console.log('🔍 检查平台连通性...\n');
  
  // 1. Moltbook
  try {
    const url = new URL('https://www.moltbook.com/api/v1/posts?limit=1');
    const result = await fetch(url);
    console.log(`✅ Moltbook: ${result.status} (${result.latency})`);
  } catch (err) {
    console.log(`❌ Moltbook: ${err.message}`);
  }
  
  // 2. GitHub
  try {
    const url = new URL('https://api.github.com/rate_limit');
    const result = await fetch(url);
    console.log(`✅ GitHub: ${result.status} (${result.latency})`);
  } catch (err) {
    console.log(`❌ GitHub: ${err.message}`);
  }
  
  // 3. ClawHub
  try {
    const url = new URL('https://clawhub.com/api/skills');
    const result = await fetch(url);
    console.log(`✅ ClawHub: ${result.status} (${result.latency})`);
  } catch (err) {
    console.log(`❌ ClawHub: ${err.message}`);
  }
  
  console.log('\n完成');
})();
