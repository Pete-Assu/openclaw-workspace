const { scanGitHub, scanClawHub } = require('./libs/skill-scanner.js');

(async () => {
  console.log('🔍 测试 GitHub...\n');
  const github = await scanGitHub();
  console.log(`找到 ${github.length} 个 GitHub 技能\n`);
  
  if (github.length > 0) {
    console.log('示例:');
    github.slice(0, 3).forEach((s, i) => {
      console.log(`${i+1}. ${s.title} (⭐${s.stars})`);
      console.log(`   ${s.clone_url || s.url}`);
    });
  }
  
  console.log('\n🔍 测试 ClawHub...\n');
  const clawhub = await scanClawHub();
  console.log(`找到 ${clawhub.length} 个 ClawHub 技能\n`);
  
  if (clawhub.length > 0) {
    console.log('示例:');
    clawhub.slice(0, 3).forEach((s, i) => {
      console.log(`${i+1}. ${s.title}`);
      console.log(`   ${s.install_url || s.url}`);
    });
  }
})();
