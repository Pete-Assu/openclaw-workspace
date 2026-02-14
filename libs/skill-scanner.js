/**
 * Multi-platform skill discovery module
 * Supports: Moltbook, GitHub, ClawHub
 */

const https = require('https');

// Simple HTTP fetch with timeout
function httpFetch(url, options = {}) {
  return new Promise((resolve, reject) => {
    const urlObj = new URL(url);
    const timeout = options.timeout || 15000;
    
    const reqOptions = {
      hostname: urlObj.hostname,
      port: urlObj.port || 443,
      path: urlObj.pathname + urlObj.search,
      method: 'GET',
      headers: {
        'User-Agent': 'OpenClaw-Agent/1.0',
        ...options.headers
      }
    };
    
    const req = https.request(reqOptions, (res) => {
      let data = '';
      
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          if (res.statusCode >= 200 && res.statusCode < 300) {
            resolve({ 
              ok: true, 
              status: res.statusCode,
              data: JSON.parse(data)
            });
          } else {
            resolve({ ok: false, status: res.statusCode });
          }
        } catch (e) {
          resolve({ ok: false, error: e.message });
        }
      });
    });
    
    req.on('error', (e) => reject(e));
    req.on('timeout', () => {
      req.destroy();
      reject(new Error('Timeout'));
    });
    
    req.setTimeout(timeout);
    req.end();
  });
}

// ============ Moltbook ============
const MOLTBOOK_API_KEY = process.env.MOLTBOOK_API_KEY || 'moltbook_sk_oyiwn5NTjQVqrdoThu4XTGutzwpeyfEU';

async function scanMoltbook() {
  const skills = [];
  const endpoints = [
    { url: 'https://www.moltbook.com/api/v1/feed/trending', name: '热门' },
    { url: 'https://www.moltbook.com/api/v1/messages?submolt=openclaw', name: 'OpenClaw' }
  ];

  for (const endpoint of endpoints) {
    try {
      console.log(`   扫描 Moltbook ${endpoint.name}...`);
      const response = await httpFetch(endpoint.url, {
        headers: { 'Authorization': `Bearer ${MOLTBOOK_API_KEY}` }
      });
      
      if (response.ok) {
        const messages = response.data?.messages || response.data?.data || [];
        
        for (const msg of messages.slice(0, 20)) {
          skills.push({
            id: msg.id || msg.uuid,
            title: msg.title || msg.summary || '无标题',
            content: msg.content || msg.body || '',
            author: msg.author?.username || msg.author?.name || 'unknown',
            votes: msg.votes || 0,
            url: msg.url,
            source: 'moltbook',
            qualityScore: 0,
            discoveredAt: new Date().toISOString()
          });
        }
        
        console.log(`   找到 ${messages.length} 个帖子`);
      }
    } catch (error) {
      console.error(`   Moltbook 错误: ${error.message}`);
    }
  }

  return skills;
}

// ============ GitHub ============
async function scanGitHub() {
  const skills = [];
  const keywords = ['openclaw-skill', 'openclaw-agent', 'autonomous-agent'];

  for (const keyword of keywords.slice(0, 2)) {
    try {
      console.log(`   扫描 GitHub (${keyword})...`);
      const query = encodeURIComponent(`topic:${keyword} language:typescript`);
      const url = `https://api.github.com/search/repositories?q=${query}&sort=stars&per_page=10`;
      
      const response = await httpFetch(url, {
        headers: { 'Accept': 'application/vnd.github.v3+json' }
      });
      
      if (response.ok) {
        const repos = response.data?.items || [];
        
        for (const repo of repos) {
          skills.push({
            id: repo.id.toString(),
            title: repo.name,
            author: repo.owner.login,
            description: repo.description,
            stars: repo.stargazers_count,
            url: repo.html_url,
            clone_url: repo.clone_url,
            language: repo.language,
            updated: repo.updated_at,
            source: 'github',
            qualityScore: Math.min(repo.stargazers_count / 1000, 1),
            discoveredAt: new Date().toISOString()
          });
        }
        
        console.log(`   找到 ${repos.length} 个仓库`);
      }
    } catch (error) {
      console.error(`   GitHub 错误: ${error.message}`);
    }
  }

  return skills;
}

// ============ ClawHub ============
const CLAWHUB_API_KEY = process.env.CLAWHUB_API_KEY || '';

async function scanClawHub() {
  const skills = [];
  const endpoints = ['https://clawhub.ai/api/v1/skills', 'https://clawhub.com/api/v1/skills'];

  for (const endpoint of endpoints) {
    try {
      console.log(`   扫描 ClawHub...`);
      const headers = { 'Accept': 'application/json' };
      if (CLAWHUB_API_KEY) headers['Authorization'] = `Bearer ${CLAWHUB_API_KEY}`;
      
      const response = await httpFetch(endpoint, { headers, timeout: 5000 });
      
      if (response.ok) {
        const items = response.data?.items || response.data?.data || response.data?.skills || [];
        
        for (const skill of items.slice(0, 20)) {
          skills.push({
            id: skill.slug || skill.id || skill.name,
            title: skill.displayName || skill.name || skill.title,
            author: skill.author || skill.owner || 'unknown',
            description: skill.summary || skill.description || '',
            url: skill.url || `https://clawhub.ai/skill/${skill.slug || skill.id}`,
            install_url: skill.repo_url || skill.github_url,
            source: 'clawhub',
            qualityScore: skill.rating ? Math.min(skill.rating / 5, 1) : 0.5,
            discoveredAt: new Date().toISOString()
          });
        }
        
        console.log(`   找到 ${items.length} 个技能`);
        break;
      }
    } catch (error) {
      console.error(`   ClawHub 错误: ${error.message}`);
    }
  }

  return skills;
}

// ============ Main Scanner ============
async function scanAllPlatforms() {
  console.log('\n🔍 开始多平台扫描...\n');
  
  const allSkills = [];
  
  console.log('📚 扫描 Moltbook...');
  const moltbookSkills = await scanMoltbook();
  allSkills.push(...moltbookSkills);
  
  console.log('\n🐙 扫描 GitHub...');
  const githubSkills = await scanGitHub();
  allSkills.push(...githubSkills);
  
  console.log('\n🦞 扫描 ClawHub...');
  const clawhubSkills = await scanClawHub();
  allSkills.push(...clawhubSkills);
  
  console.log(`\n✅ 总共发现 ${allSkills.length} 个技能\n`);
  
  return allSkills;
}

// ============ Export ============
module.exports = { scanMoltbook, scanGitHub, scanClawHub, scanAllPlatforms };
