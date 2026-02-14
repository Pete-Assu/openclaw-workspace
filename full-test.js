// 完整测试扫描和安装
const { scanAllPlatforms } = require('./libs/skill-scanner.js');
const fs = require('fs');
const path = require('path');

const SKILLS_PATH = 'C:/Users/殇/node_modules/openclaw/skills';

function sanitizeName(title) {
  return (title || 'unknown-skill')
    .toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').substring(0, 50);
}

async function testInstall(skill) {
  const name = sanitizeName(skill.title);
  const dir = path.join(SKILLS_PATH, name);
  
  if (fs.existsSync(dir)) {
    console.log(`   ⏭️ 跳过已安装: ${name}`);
    return false;
  }
  
  const installUrl = skill.clone_url || skill.url || skill.install_url;
  
  if (!installUrl) {
    console.log(`   ⚠️ 无安装链接: ${skill.title?.substring(0, 30)}`);
    return false;
  }
  
  console.log(`   📦 安装: ${installUrl}`);
  
  fs.mkdirSync(dir, { recursive: true });
  
  // 创建 package.json
  fs.writeFileSync(path.join(dir, 'package.json'), JSON.stringify({
    name: name,
    version: '1.0.0',
    description: skill.description || skill.title,
    author: skill.author || 'Auto',
    keywords: ['auto-installed', skill.source]
  }, null, 2));
  
  // 创建 SKILL.md
  fs.writeFileSync(path.join(dir, 'SKILL.md'), `# ${skill.title}

**来源**: ${skill.source}
**质量**: ${((skill.qualityScore || 0) * 100).toFixed(0)}%
**URL**: ${installUrl}

## 描述

${skill.description || '自动安装'}
`);
  
  console.log(`   ✅ 已创建: ${name}`);
  return true;
}

(async () => {
  console.log('🚀 测试完整扫描和安装\n');
  
  const skills = await scanAllPlatforms();
  
  console.log(`\n📊 发现 ${skills.length} 个技能`);
  
  // 去重
  const unique = skills.filter((s, i, arr) => arr.findIndex(t => t.title === s.title) === i);
  console.log(`📊 去重后 ${unique.length} 个技能\n`);
  
  // 按质量排序
  unique.sort((a, b) => (b.qualityScore || 0) - (a.qualityScore || 0));
  
  // 安装前 5 个
  console.log('📦 安装 Top 5:\n');
  let installed = 0;
  
  for (const skill of unique.slice(0, 5)) {
    try {
      const result = await testInstall(skill);
      if (result) installed++;
    } catch (e) {
      console.log(`   ❌ 失败: ${e.message}`);
    }
  }
  
  console.log(`\n✅ 完成: ${installed}/${Math.min(5, unique.length)} 个技能`);
  process.exit(0);
})();
