#!/usr/bin/env node
/**
 * System Health Check & Auto-Fix Script
 * 检查系统健康状态，发现问题自动尝试修复
 */

const { exec, execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const https = require('https');

const CONFIG = {
  workspace: 'C:\\Users\\殇\\.openclaw\\workspace',
  skillsDir: 'C:\\Users\\殇\\node_modules\\openclaw\\skills',
  checkTimeout: 5000,
  platforms: [
    { name: 'GitHub', url: 'https://api.github.com/rate_limit' },
    { name: 'Moltbook', url: 'https://www.moltbook.com/api/v1/posts?limit=1' },
    { name: 'ClawHub', url: 'https://clawhub.ai/api/v1/skills' }
  ]
};

const issues = [];
const fixes = [];

function log(msg, type = 'info') {
  const prefix = {
    info: '🔍',
    success: '✅',
    error: '❌',
    fix: '🔧',
    warn: '⚠️'
  }[type] || '•';
  console.log(`${prefix} ${msg}`);
}

function execCommand(cmd, timeout = 10000) {
  try {
    return execSync(cmd, { encoding: 'utf8', timeout, windowsHide: true }).trim();
  } catch (e) {
    return null;
  }
}

function checkOpenClawService() {
  log('检查 OpenClaw 服务状态...', 'info');
  
  try {
    const status = execCommand('openclaw status 2>&1', 15000);
    if (status && !status.includes('not found')) {
      const isRunning = status.includes('running') || status.includes('reachable');
      if (isRunning) {
        log('OpenClaw 服务运行正常', 'success');
        return true;
      } else {
        issues.push({ component: 'OpenClaw', severity: 'high', message: '服务未运行' });
        log('OpenClaw 服务未运行', 'error');
        return false;
      }
    } else {
      issues.push({ component: 'OpenClaw', severity: 'medium', message: '无法获取服务状态' });
      return false;
    }
  } catch (e) {
    issues.push({ component: 'OpenClaw', severity: 'medium', message: e.message });
    return false;
  }
}

function checkSkills() {
  log('检查技能安装状态...', 'info');
  
  try {
    const skillsDir = CONFIG.skillsDir;
    let skillsCount = 0;
    
    if (fs.existsSync(skillsDir)) {
      const skills = fs.readdirSync(skillsDir).filter(f => !f.startsWith('.') && fs.statSync(path.join(skillsDir, f)).isDirectory());
      skillsCount = skills.length;
    }
    
    // Check hooks (context-compression is a hook, not skill)
    const hooksDir = path.join(process.env.USERPROFILE || '', '.openclaw', 'hooks');
    const hooks = fs.existsSync(hooksDir) ? fs.readdirSync(hooksDir) : [];
    const hasContextCompression = hooks.includes('context-compression');
    
    const criticalSkills = ['healthcheck', 'super-skill-library', 'self-repair'];
    const missingCritical = criticalSkills.filter(s => !fs.existsSync(path.join(CONFIG.skillsDir, s)));
    
    if (skillsCount >= 100) {
      log(`技能检查通过: ${skillsCount} 个技能`, 'success');
    } else {
      issues.push({ component: 'Skills', severity: 'low', message: `仅 ${skillsCount} 个技能` });
    }
    
    if (missingCritical.length > 0) {
      log(`缺失关键技能: ${missingCritical.join(', ')}`, 'warn');
      issues.push({ component: 'Skills', severity: 'medium', message: `缺失关键技能: ${missingCritical.join(', ')}` });
    } else if (hasContextCompression) {
      log('所有关键组件正常 (skills + context-compression hook)', 'success');
    }
      
    return skillsCount;
  } catch (e) {
    issues.push({ component: 'Skills', severity: 'medium', message: e.message });
    return 0;
  }
}

function fetchWithTimeout(url, timeout = 5000) {
  return new Promise((resolve, reject) => {
    const urlObj = new URL(url);
    const client = urlObj.protocol === 'https:' ? https : require('http');
    
    const req = client.get(url, { timeout }, (res) => {
      resolve({ status: res.statusCode, location: res.headers.location || null });
    });
    
    req.on('error', reject);
    req.on('timeout', () => {
      req.destroy();
      reject(new Error('Timeout'));
    });
    
    req.setTimeout(timeout);
  });
}

async function checkPlatformConnectivity() {
  log('检查外部平台连通性...', 'info');
  
  const results = { feishu: { status: 'unknown' } };
  
  for (const platform of CONFIG.platforms) {
    try {
      const result = await fetchWithTimeout(platform.url, CONFIG.checkTimeout);
      results[platform.name.toLowerCase()] = {
        ok: result.status >= 200 && result.status < 400,
        status: result.status,
        location: result.location || null
      };
      log(`${platform.name}: ${result.status}`, results[platform.name.toLowerCase()].ok ? 'success' : 'warn');
    } catch (e) {
      results[platform.name.toLowerCase()] = { ok: false, error: e.message };
      log(`${platform.name}: 失败 - ${e.message}`, 'error');
    }
  }
  
  // Check Feishu separately
  try {
    const feishuResult = execSync('python ' + CONFIG.workspace.replace(/\\/g, '/') + '/feishu_auto_fix.py --monitor', {
      encoding: 'utf8',
      timeout: 30000
    });
    results.feishu = { ok: feishuResult.includes('飞书配置正常'), details: feishuResult.trim() };
    log('Feishu: ' + (results.feishu.ok ? '配置正常' : '需关注'), results.feishu.ok ? 'success' : 'warn');
  } catch (e) {
    results.feishu = { ok: false, error: e.message };
    log('Feishu: 检查失败', 'error');
  }
  
  return results;
}

function checkNpmAndOpenClaw() {
  log('检查 npm 和 Node.js...', 'info');
  
  try {
    const npmVersion = execCommand('npm --version');
    const nodeVersion = execCommand('node --version');
    
    if (npmVersion && nodeVersion) {
      log(`npm ${npmVersion} / Node.js ${nodeVersion}`, 'success');
      return true;
    }
  } catch (e) {}
  
  issues.push({ component: 'npm/Node', severity: 'medium', message: '无法检查版本' });
  return false;
}

function checkSystemResources() {
  log('检查系统资源...', 'info');
  
  try {
    const disk = execCommand('wmic logicaldisk get size,freespace,name 2>&1');
    if (disk) {
      const cDrive = disk.split('\n').find(l => l.includes('C:'));
      if (cDrive) {
        const parts = cDrive.split(/\s+/);
        if (parts.length >= 3) {
          const freeGB = Math.round(parseInt(parts[2]) / 1024 / 1024 / 1024);
          log(`C: 盘可用空间: ${freeGB}GB`, freeGB > 20 ? 'success' : 'warn');
        }
      }
    }
  } catch (e) {}
}

function generateReport() {
  const status = {
    passed: 0,
    failed: issues.length,
    warning: fixes.length
  };
  
  return {
    status: issues.length === 0 ? 'healthy' : 'degraded',
    checks: {
      openClaw: issues.filter(i => i.component === 'OpenClaw').length === 0,
      npm: issues.filter(i => i.component === 'npm/Node').length === 0,
      skills: issues.filter(i => i.component === 'Skills').length === 0,
      connectivity: issues.filter(i => i.component === 'Network').length === 0,
      disk: issues.filter(i => i.component === 'Disk').length === 0
    },
    issues: issues,
    fixes: fixes,
    timestamp: new Date().toISOString()
  };
}

function autoFix() {
  log('尝试自动修复...', 'fix');
  
  // 修复1: 清理 npm 缓存
  const npmIssue = issues.find(i => i.message?.includes('cache'));
  if (npmIssue) {
    try {
      log('清理 npm 缓存...', 'fix');
      exec('npm cache clean --force 2>&1', { windowsHide: true });
      fixes.push('已清理 npm 缓存');
    } catch (e) {}
  }
  
  // 修复2: 检查 hosts 文件
  const githubIssue = issues.find(i => i.component.includes('GitHub'));
  if (githubIssue) {
    try {
      const hostsPath = 'C:\\Windows\\System32\\drivers\\etc\\hosts';
      if (fs.existsSync(hostsPath)) {
        const hosts = fs.readFileSync(hostsPath, 'utf8');
        if (hosts.includes('github.com') && !hosts.includes('140.82')) {
          log('发现 GitHub hosts 污染', 'warn');
          issues.push({ component: 'Hosts', severity: 'high', message: 'GitHub hosts 污染' });
          issues.push({ component: 'Network', severity: 'medium', message: 'GitHub hosts 文件污染' });
        } else if (!hosts.includes('github.com')) {
          log('GitHub hosts 正常', 'success');
        }
      }
    } catch (e) {
      log('检查 hosts 文件失败: ' + e.message, 'error');
    }
  }
}

async function main() {
  log('开始系统健康检查...');
  
  checkNpmAndOpenClaw();
  checkOpenClawService();
  checkSkills();
  await checkPlatformConnectivity();
  checkSystemResources();
  
  autoFix();
  const report = generateReport();
  
  // 保存报告
  const reportPath = path.join(CONFIG.workspace, 'health-report.json');
  fs.writeFileSync(reportPath, JSON.stringify({
    timestamp: new Date().toISOString(),
    ...report
  }, null, 2));
  log(`报告已保存: ${reportPath}`, 'info');
}

main().catch(e => {
  log(`检查失败: ${e.message}`, 'error');
  process.exit(1);
});
