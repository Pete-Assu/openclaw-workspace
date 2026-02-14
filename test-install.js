// 测试多平台扫描和安装
const { scanGitHub, scanClawHub, scanMoltbook } = require('./libs/skill-scanner.js');
const { installSkill } = require('./skills/self-orchestrator/self-orchestrator.js');
const { execSync } = require('child_process');

(async () => {
  console.log('🔍 测试多平台扫描...\n');
  
  // GitHub
  console.log('=== GitHub ===');
  const github = await scanGitHub();
  console.log(`找到 ${github.length} 个 GitHub 技能\n`);
  
  if (github.length > 0) {
    github.slice(0, 3).forEach((s, i) => {
      console.log(`${i+1}. ${s.title} (⭐${s.stars})`);
      console.log(`   clone_url: ${s.clone_url || 'N/A'}\n`);
    });
  }
  
  // ClawHub
  console.log('=== ClawHub ===');
  const clawhub = await scanClawHub();
  console.log(`找到 ${clawhub.length} 个 ClawHub 技能\n`);
  
  // Moltbook
  console.log('=== Moltbook ===');
  const moltbook = await scanMoltbook();
  console.log(`找到 ${moltbook.length} 个 Moltbook 技能\n`);
  
  // 合并并安装
  console.log('=== 安装测试 ===');
  const all = [...github, ...clawhub, ...moltbook];
  const unique = all.filter((s, i, arr) => arr.findIndex(t => t.title === s.title) === i);
  
  // 按质量排序
  unique.sort((a, b) => (b.qualityScore || 0) - (a.qualityScore || 0));
  
  console.log(`总共 ${unique.length} 个唯一技能\n`);
  
  // 测试安装前 3 个
  for (const skill of unique.slice(0, 3)) {
    console.log(`\n测试安装: ${skill.title}`);
    console.log(`  来源: ${skill.source}`);
    console.log(`  质量: ${(skill.qualityScore * 100).toFixed(0)}%`);
    
    try {
      const result = await installSkill(skill);
      console.log(`  结果: ${result ? '✅ 成功' : '⏭️ 跳过'}`);
    } catch (e) {
      console.log(`  错误: ${e.message}`);
    }
  }
  
  console.log('\n✅ 测试完成');
})();
