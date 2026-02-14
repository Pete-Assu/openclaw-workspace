#!/usr/bin/env node
/**
 * OpenClaw 会话监控器
 * 自动检测 Gateway 和会话状态，发现掉线自动恢复
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const STATE_FILE = path.join(__dirname, 'memory', 'session-state.json');
const HEALTH_CHECK_INTERVAL = 5 * 60 * 1000; // 5分钟
const MAX_INACTIVE_MINUTES = 30; // 30分钟不活跃就重启

function getHealth() {
  try {
    const output = execSync('openclaw health', { encoding: 'utf8', timeout: 10000 });
    
    // 解析文本输出
    const sessions = [];
    const lines = output.split('\n');
    
    for (const line of lines) {
      // 匹配 "- id (时间 ago)" 格式
      const match = line.match(/^\s*-\s+(\S+)\s+\((\d+)m\s+ago\)/);
      if (match) {
        sessions.push({ id: match[1], minutesAgo: parseInt(match[2]) });
      }
    }
    
    return { sessions, raw: output };
  } catch (e) {
    return null;
  }
}

function restartGateway() {
  console.log('🔄 重启 Gateway...');
  try {
    execSync('openclaw gateway restart', { timeout: 10000 });
    return true;
  } catch (e) {
    console.error('Gateway 重启失败:', e.message);
    return false;
  }
}

function restartMainSession() {
  console.log('🔄 重启主会话...');
  try {
    execSync('openclaw agent --to main --message "自动重启连接" --deliver', { timeout: 15000 });
    return true;
  } catch (e) {
    console.error('会话重启失败:', e.message);
    return false;
  }
}

function loadState() {
  try {
    return JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
  } catch {
    return { lastCheck: 0, lastActive: Date.now(), restartCount: 0 };
  }
}

function saveState(state) {
  fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
}

function monitor() {
  const health = getHealth();
  
  if (!health) {
    console.log('❌ Gateway 无响应，尝试重启...');
    restartGateway();
    return;
  }
  
  const mainSession = health.sessions.find(s => s.id === 'main');
  const inactiveMinutes = mainSession?.minutesAgo || 999;
  
  const state = loadState();
  
  console.log(`📊 检查: 主会话 ${inactiveMinutes.toFixed(1)} 分钟前活跃`);
  
  if (inactiveMinutes > MAX_INACTIVE_MINUTES) {
    console.log('⚠️ 会话超过 30 分钟不活跃');
    
    if (state.restartCount < 3) { // 限制重启次数避免死循环
      restartGateway();
      restartMainSession();
      state.restartCount++;
      state.lastActive = Date.now();
      saveState(state);
    } else {
      console.log('⚠️ 已重启 3 次，停止自动恢复');
    }
  } else {
    state.lastActive = Date.now() - (inactiveMinutes * 60 * 1000);
    state.restartCount = 0;
    saveState(state);
  }
}

console.log('🚀 OpenClaw 会话监控器启动');
console.log(`检查间隔: ${HEALTH_CHECK_INTERVAL / 1000 / 60} 分钟`);
console.log(`最大不活跃时间: ${MAX_INACTIVE_MINUTES} 分钟\n`);

// 立即检查一次
monitor();

// 定期检查
setInterval(monitor, HEALTH_CHECK_INTERVAL);
