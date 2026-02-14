const https = require('https');

function fetch(url) {
  return new Promise((resolve, reject) => {
    const req = https.get(url, { timeout: 8000 }, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        fetch(new URL(res.headers.location, url).toString()).then(resolve).catch(reject);
        return;
      }

      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve({ status: res.statusCode, data: JSON.parse(data) }));
    });
    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('timeout')); });
    req.end();
  });
}

(async () => {
  console.log('🔍 ClawHub API 测试结果\n');
  console.log('========================================\n');

  const url = 'https://clawhub.com/api/v1/skills';
  const result = await fetch(url);

  console.log('API: ' + url);
  console.log('状态: ' + result.status + ' OK\n');

  const skills = result.data.items || [];
  console.log('🎯 发现 ' + skills.length + ' 个技能:\n');

  skills.forEach((skill, i) => {
    console.log(`${i+1}. ${skill.displayName || skill.name}`);
    console.log(`   ${skill.summary?.substring(0, 80) || '无描述'}`);
    console.log(`   🔗 https://clawhub.com/skill/${skill.slug}`);
    console.log('');
  });

  // 查找与自动化/Agent 相关的技能
  const relevant = skills.filter(s => {
    const text = `${s.displayName} ${s.summary}`.toLowerCase();
    return text.includes('agent') || text.includes('automation') || text.includes('self') || text.includes('workflow');
  });

  console.log('========================================');
  console.log('🤖 与自动化相关的技能 (' + relevant.length + '):\n');
  relevant.forEach((s, i) => {
    console.log(`  ${i+1}. ${s.displayName}`);
    console.log(`     ${s.summary?.substring(0, 60)}...`);
    console.log('');
  });
})();
