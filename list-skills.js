const scanner = require('./libs/skill-scanner.js');

(async () => {
  console.log('🔍 扫描三平台技能...\n');

  const skills = await scanner.scanAllPlatforms();

  console.log('\n📊 按来源统计:');
  const bySource = {};
  skills.forEach(s => {
    bySource[s.source] = (bySource[s.source] || 0) + 1;
  });
  Object.entries(bySource).forEach(([source, count]) => {
    console.log(`   ${source}: ${count}`);
  });

  console.log('\n🎯 全部技能列表:');
  skills.forEach((s, i) => {
    console.log(`${i+1}. [${((s.qualityScore || 0) * 100).toFixed(0)}%] ${s.title?.substring(0, 50)} (${s.source})`);
  });
})();
