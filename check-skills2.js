const fs = require('fs');
const path = require('path');

const skillsPath = 'C:\\Users\\殇\\node_modules\\openclaw\\skills';

try {
  const dirs = fs.readdirSync(skillsPath).filter(f => {
    try {
      return fs.statSync(path.join(skillsPath, f)).isDirectory();
    } catch (e) { return false; }
  });

  console.log('Total skills:', dirs.length);

  // 查找可能的新技能
  const keywords = ['usdc', 'project', 'hackathon', 'commerce', 'router', 'agentic', 'clawrouter', 'prediction'];
  
  const found = dirs.filter(d => {
    const lower = d.toLowerCase();
    return keywords.some(k => lower.includes(k));
  });

  console.log('\nMatching skills:', found.length);
  found.forEach(d => console.log(' -', d));
  
} catch (error) {
  console.error('Error:', error.message);
}
