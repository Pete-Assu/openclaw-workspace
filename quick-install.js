// 快速测试：发现 + 安装
const { scanGitHub, scanClawHub, scanMoltbook } = require('./libs/skill-scanner.js');
const { installSkill } = require('./skills/self-orchestrator/self-orchestrator.js');
const fs = require('fs');

(async () => {
  console.log('🔍 扫描平台...\n');
  
  const all = [];
  
  // GitHub
  console.log('GitHub...');
  const github = await scanGitHub();
  console.log(`  找到 ${github.length} 个`);
  all.push(...github.map(s => ({ ...s, source: 'github' })));
  
  // Moltbook  
  console.log('Moltbook...');
  const moltbook = await scanMoltbook();
  console.log(`  找到 ${moltbook.length} 个`);
  all.push(...moltbook.map(s => ({ ...s, source: 'moltbook' })));
  
  // 按质量排序
  all.sort((a, b) => (b.qualityScore || 0) - (a.qualityScore || 0));
  
  console.log(`\n📊 总共 ${all.length} 个技能`);
  
  // 取前 5 个安装
  const toInstall = all.slice(0, 5);
  console.log(`\n🚀 安装前 ${toInstall.length} 个技能:\n`);
  
  let installed = 0;
  for (const skill of toInstall) {
    console.log(`- ${skill.title} (${skill.source})`);
    try {
      const result = await installSkill(skill);
      if (result) {
        console.log(`  ✅ 已安装`);
        installed++;
      } else {
        console.log(`  ⏭️ 跳过`);
      }
    } catch (e) {
      console.log(`  ❌ 失败: ${e.message}`);
    }
  }
  
  console.log(`\n✅ 完成: ${installed}/${toInstall.length} 个技能已安装`);
})();
