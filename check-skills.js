const fs = require('fs');
const path = require('path');

const skillsPath = 'C:\\Users\\殇\\node_modules\\openclaw\\skills';

const dirs = fs.readdirSync(skillsPath).filter(f => {
  try {
    return fs.statSync(path.join(skillsPath, f)).isDirectory();
  } catch (e) { return false; }
});

console.log('Skills count:', dirs.length);

// 查找今天安装的
const today = dirs.filter(d => d.includes('usdc') || d.includes('project'));

console.log('\n可能新安装的技能:');
today.forEach(d => console.log('  -', d));

// 检查 CLAWROUTER
const clawrouter = dirs.find(d => d.toLowerCase().includes('clawrouter'));
console.log('\nClawRouter:', clawrouter || '未找到');
