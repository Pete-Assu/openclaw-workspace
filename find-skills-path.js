const fs = require('fs');
const path = require('path');

const possiblePaths = [
  'C:\\Users\\殇\\.openclaw\\workspace\\node_modules\\openclaw\\skills',
  'C:\\Users\\殇\\node_modules\\openclaw\\skills',
  'C:\\Users\\殇\\.openclaw\\skills',
  'C:\\Users\\殇\\AppData\\Roaming\\npm\\node_modules\\openclaw\\skills'
];

for (const p of possiblePaths) {
  try {
    if (fs.existsSync(p)) {
      const dirs = fs.readdirSync(p).filter(f => {
        try { return fs.statSync(path.join(p, f)).isDirectory(); } catch(e) { return false; }
      });
      console.log(`✓ ${p}`);
      console.log(`  ${dirs.length} skills found\n`);
    } else {
      console.log(`✗ ${p} (not exists)\n`);
    }
  } catch (e) {
    console.log(`✗ ${p}: ${e.message}\n`);
  }
}

// 检查 workspace 下是否有 node_modules
console.log('\nChecking workspace structure...');
const wsPath = 'C:\\Users\\殇\\.openclaw\\workspace';
try {
  const items = fs.readdirSync(wsPath);
  const modules = items.filter(i => i === 'node_modules');
  console.log('node_modules exists in workspace:', modules.length > 0);
  
  if (modules.length > 0) {
    const nmPath = path.join(wsPath, 'node_modules');
    console.log('\nContents of workspace/node_modules:');
    fs.readdirSync(nmPath).forEach(i => console.log(' -', i));
  }
} catch (e) {
  console.log('Error:', e.message);
}
