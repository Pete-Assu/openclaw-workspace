import('./libs/skill-scanner.js').then(async ({ scanMoltbook, scanGitHub, scanClawHub }) => {
  console.log('🔍 测试三平台扫描...\n');

  // 测试 ClawHub
  console.log('🦞 测试 ClawHub:');
  const clawhub = await scanClawHub();
  console.log(`   找到 ${clawhub.length} 个技能\n`);

  if (clawhub.length > 0) {
    console.log('🎯 前 3 个技能:');
    clawhub.slice(0, 3).forEach((s, i) => {
      console.log(`   ${i+1}. ${s.title}`);
    });
  }

  console.log('\n✅ ClawHub 扫描正常!');
});
