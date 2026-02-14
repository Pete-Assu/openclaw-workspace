const fs = require('fs');
const path = require('path');

const root = 'C:\\Users\\殇\\node_modules\\openclaw\\skills';

// 递归搜索
function search(dir, pattern) {
  const results = [];
  
  try {
    const items = fs.readdirSync(dir);
    for (const item of items) {
      const fullPath = path.join(dir, item);
      try {
        const stat = fs.statSync(fullPath);
        if (stat.isDirectory()) {
          if (item.toLowerCase().includes(pattern)) {
            results.push(fullPath);
          }
          results.push(...search(fullPath, pattern));
        }
      } catch (e) {}
    }
  } catch (e) {}
  
  return results;
}

console.log('Searching for skills with usdc/project/hackathon...\n');

const results = search(root, 'usdc');
console.log('Found', results.length, 'matches');
results.forEach(r => console.log(' -', r));

// 检查 workspace 下的 skills
console.log('\n\nChecking workspace skills...');
const wsSkills = search('C:\\Users\\殇\\.openclaw\\workspace\\skills', '');
console.log('Found', wsSkills.length, 'items in workspace/skills');
wsSkills.forEach(r => console.log(' -', r));
