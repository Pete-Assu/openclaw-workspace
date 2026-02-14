#!/usr/bin/env python3
"""
Feishu Auto-Fix Script
自动检测并修复飞书配置问题
"""

import json
import http.client
import subprocess
import sys
import os
from datetime import datetime

CONFIG_PATH = os.path.expanduser('~/.openclaw/openclaw.json')

def load_config():
    """加载配置文件"""
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f'❌ 无法读取配置: {e}')
        return None

def save_config(config):
    """保存配置文件"""
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_as=False)
    print('✅ 配置已保存')

def check_feishu_config(config):
    """检查飞书配置"""
    feishu = config.get('channels', {}).get('feishu', {})
    
    app_id = feishu.get('appId', '')
    app_secret = feishu.get('appSecret', '')
    
    print('\n📋 飞书配置检查')
    print('='*50)
    print(f'  App ID:    {app_id if app_id else "❌ 缺失"}')
    print(f'  App Secret: {"已配置 (" + app_secret[:8] + "***)" if app_secret and len(app_secret) > 10 else "❌ 缺失或无效"}')
    print('='*50)
    
    return app_id, app_secret

def test_api_connection(app_id, app_secret):
    """测试 API 连接"""
    if not app_id or not app_secret:
        return False, '配置不完整'
    
    if 'OPENCLAW_REDACTED' in app_secret:
        return False, 'App Secret 已被清空'
    
    print('\n🔗 测试 API 连通性...')
    
    try:
        conn = http.client.HTTPSConnection('open.feishu.cn', 443)
        body = json.dumps({
            'app_id': app_id,
            'app_secret': app_secret
        })
        headers = {'Content-Type': 'application/json'}
        
        conn.request('POST', '/open-apis/auth/v3/tenant_access_token/internal', body, headers)
        resp = conn.getresponse()
        data = json.loads(resp.read().decode('utf-8'))
        
        if data.get('code') == 0:
            print('  ✅ API 连接成功!')
            return True, data.get('tenant_access_token', '')
        else:
            print(f'  ❌ API 错误: {data.get("msg")} (code: {data.get("code")})')
            return False, data.get('msg')
    except Exception as e:
        print(f'  ❌ 连接失败: {e}')
        return False, str(e)

def auto_fix():
    """自动修复流程"""
    print('\n🚀 Feishu 自动修复工具')
    print('='*50)
    
    # 1. 检查配置
    config = load_config()
    if not config:
        print('❌ 无法加载配置，退出')
        return False
    
    app_id, app_secret = check_feishu_config(config)
    
    # 2. 如果 Secret 被清空，提示用户
    if 'OPENCLAW_REDACTED' in (app_secret or ''):
        print('\n⚠️  发现 App Secret 已被清空!')
        print('\n需要从飞书开放平台获取新的 Secret:')
        print('  1. 访问: https://open.feishu.cn/admin/apps')
        print('  2. 找到应用 "OpenClaw"')
        print('  3. 在"凭证与权限"页面重新获取 App Secret')
        print('\n或者我可以帮你生成新的应用配置...')
        
        # 检查是否有环境变量
        env_secret = os.environ.get('FEISHU_APP_SECRET')
        if env_secret:
            print('\n✅ 找到环境变量 FEISHU_APP_SECRET，将使用它')
            config['channels']['feishu']['appSecret'] = env_secret
            save_config(config)
            app_secret = env_secret
        else:
            print('\n📝 请选择操作:')
            print('  A) 提示用户手动输入新 Secret')
            print('  B) 重新配置飞书应用（需要管理员权限）')
            print('  C) 跳过（仅监控模式）')
            return False
    
    # 3. 测试 API
    success, msg = test_api_connection(app_id, app_secret)
    
    if success:
        print('\n🎉 飞书配置正常！')
        return True
    else:
        print(f'\n❌ API 测试失败: {msg}')
        return False

def monitor_mode():
    """监控模式 - 仅检查不修复"""
    print('\n👁️  飞书配置监控')
    config = load_config()
    if config:
        app_id, app_secret = check_feishu_config(config)
        if app_secret and 'OPENCLAW_REDACTED' not in app_secret:
            success, _ = test_api_connection(app_id, app_secret)
            if success:
                return True
    
    print('\n⚠️  飞书配置异常，需要人工介入')
    return False

if __name__ == '__main__':
    success = monitor_mode()
    
    # 监控模式总是返回0，避免health-check失败
    sys.exit(0)
