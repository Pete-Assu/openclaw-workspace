// 简单测试 GitHub 扫描
const { scanGitHub } = require('./libs/skill-scanner.js');

(async () => {
  console.log('🔍 测试 GitHub 扫描...\n');
  const start = Date.now();
  
  const skills = await scanGitHub();
  const elapsed = Date.now() - start;
  
  console.log(`\n✅ 完成: ${skills.length} 个技能 (${elapsed}ms)\n`);
  
  if (skills.length > 0) {
    skills.forEach((s, i) => {
      console.log(`${i+1}. ${s.title} (⭐${s.stars})`);
      console.log(`   URL: ${s.url}`);
      console.log(`   Clone: ${s.clone_url}\n`);
    });
  }
  
  process.exit(0);
})();
