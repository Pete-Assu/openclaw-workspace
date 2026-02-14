const https = require('https');

const options = {
  hostname: 'api.github.com',
  path: '/search/repositories?q=topic:openclaw-skill+language:typescript&per_page=5',
  headers: {
    'Accept': 'application/vnd.github.v3+json',
    'User-Agent': 'OpenClaw-Agent'
  },
  timeout: 10000
};

console.log('🔍 测试 GitHub API...\n');

const req = https.request(options, (res) => {
  let data = '';
  
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    try {
      const parsed = JSON.parse(data);
      console.log('✅ GitHub 连接成功!');
      console.log(`找到 ${parsed.total_count || 0} 个仓库\n`);
      
      if (parsed.items && parsed.items.length > 0) {
        console.log('示例:');
        parsed.items.slice(0, 2).forEach((repo, i) => {
          console.log(`${i+1}. ${repo.name} (⭐${repo.stargazers_count})`);
          console.log(`   clone_url: ${repo.clone_url}\n`);
        });
      }
    } catch (e) {
      console.log('❌ JSON 解析失败:', e.message);
      console.log(data.substring(0, 500));
    }
  });
});

req.on('error', (e) => {
  console.log('❌ GitHub API 错误:', e.message);
});

req.on('timeout', () => {
  console.log('❌ 超时');
  req.destroy();
});

req.end();
