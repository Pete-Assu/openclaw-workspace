/**
 * 真实 Moltbook API 集成模块
 */

const https = require('https');

const API_KEY = process.env.MOLTBOOK_API_KEY || 'moltbook_sk_oyiwn5NTjQVqrdoThu4XTGutzwpeyfEU';
const BASE_HOST = 'www.moltbook.com';

function apiRequest(path) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: BASE_HOST,
      port: 443,
      path: path,
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Accept': 'application/json'
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          resolve(json);
        } catch (e) {
          resolve({ raw: data, status: res.statusCode });
        }
      });
    });

    req.on('error', reject);
    req.end();
  });
}

// 扫描热门技能
async function scanTrendingSkills(limit = 10) {
  try {
    const result = await apiRequest(`/api/v1/posts?sort=hot&limit=${limit}`);
    
    if (result.success && result.posts) {
      // 过滤可能与 AI/OpenClaw 相关的帖子
      const skills = result.posts
        .filter(post => {
          const keywords = ['skill', 'agent', 'openclaw', 'claude', 'code', 'automation', 'learning'];
          const text = `${post.title} ${post.content}`.toLowerCase();
          return keywords.some(k => text.includes(k));
        })
        .map(post => ({
          id: post.id,
          title: post.title,
          author: post.author?.username || post.authorId,
          votes: post.votes || 0,
          url: post.url,
          content: post.content?.substring(0, 500),
          type: 'trending',
          qualityScore: Math.min((post.votes || 0) / 100, 1), // 质量分数基于投票
          discoveredAt: new Date().toISOString()
        }));
      
      return skills;
    }
    return [];
  } catch (error) {
    console.error(`[Moltbook] 扫描错误: ${error.message}`);
    return [];
  }
}

// 搜索特定技能
async function searchSkills(query, limit = 10) {
  try {
    const result = await apiRequest(`/api/v1/search?q=${encodeURIComponent(query)}&limit=${limit}`);
    
    if (result.success && result.results) {
      return result.results.map(r => ({
        id: r.id,
        title: r.title,
        type: r.type,
        qualityScore: (r.votes || 0) / 100,
        discoveredAt: new Date().toISOString()
      }));
    }
    return [];
  } catch (error) {
    console.error(`[Moltbook] 搜索错误: ${error.message}`);
    return [];
  }
}

// 获取特定 submolt
async function getSubmoltSkills(submoltName, limit = 20) {
  try {
    const result = await apiRequest(`/api/v1/submolts/${submoltName}?limit=${limit}`);
    
    if (result.posts) {
      return result.posts.map(post => ({
        id: post.id,
        title: post.title,
        author: post.author?.username,
        votes: post.votes || 0,
        qualityScore: Math.min((post.votes || 0) / 50, 1),
        discoveredAt: new Date().toISOString()
      }));
    }
    return [];
  } catch (error) {
    console.error(`[Moltbook] Submolt 获取错误: ${error.message}`);
    return [];
  }
}

// 导出函数
module.exports = {
  scanTrendingSkills,
  searchSkills,
  getSubmoltSkills,
  apiRequest
};

// CLI 测试
if (require.main === module) {
  (async () => {
    console.log('🔍 扫描热门技能...\n');
    
    const skills = await scanTrendingSkills(15);
    
    console.log(`找到 ${skills.length} 个相关技能:\n`);
    
    skills.forEach((skill, i) => {
      console.log(`${i+1}. [${skill.votes} 👍] ${skill.title?.substring(0, 60)}`);
      console.log(`   作者: ${skill.author}`);
      console.log(`   质量分: ${(skill.qualityScore * 100).toFixed(0)}%`);
      console.log('');
    });
    
    // 保存到文件
    const fs = require('fs');
    fs.writeFileSync(
      'memory/discovered-skills.jsonl',
      skills.map(s => JSON.stringify(s)).join('\n')
    );
    console.log(`💾 已保存到 memory/discovered-skills.jsonl`);
  })();
}
