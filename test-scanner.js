// 独立测试 skill-scanner
const { scanGitHub, scanClawHub } = require('./libs/skill-scanner.js');

(async () => {
  console.log('🔍 测试 GitHub...\n');
  const github = await scanGitHub();
  console.log(`\n✅ GitHub: ${github.length} 个技能\n`);
  
  if (github.length > 0) {
    console.log('示例:');
    github.slice(0, 2).forEach(s => {
      console.log(`- ${s.title} (⭐${s.stars})`);
      console.log(`  url: ${s.url || 'N/A'}`);
      console.log(`  clone_url: ${s.clone_url || 'N/A'}\n`);
    });
  }
  
  console.log('🔍 测试 ClawHub...\n');
  const clawhub = await scanClawHub();
  console.log(`\n✅ ClawHub: ${clawhub.length} 个技能\n`);
  
  if (clawhub.length > 0) {
    console.log('示例:');
    clawhub.slice(0, 2).forEach(s => {
      console.log(`- ${s.title}`);
      console.log(`  url: ${s.url || 'N/A'}`);
      console.log(`  install_url: ${s.install_url || 'N/A'}\n`);
    });
  }
})();
