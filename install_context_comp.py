import subprocess
import os
import json

# Check context-compression
skills_dir = r'C:\Users\殇\node_modules\openclaw\skills'
context_comp_path = os.path.join(skills_dir, 'context-compression')

print('检查 context-compression 技能...')

if os.path.exists(context_comp_path):
    print('  已存在:', context_comp_path)
    # Check if it's a valid skill
    skill_json = os.path.join(context_comp_path, 'SKILL.json')
    if os.path.exists(skill_json):
        with open(skill_json, 'r') as f:
            skill = json.load(f)
        print('  名称:', skill.get('name', 'Unknown'))
        print('  状态: 已安装 ✓')
else:
    print('  不存在，需要安装')
    print('  尝试安装...')
    
    # Try npm install
    try:
        result = subprocess.run(
            ['npm', 'install', 'context-compression', '--prefix', skills_dir],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            print('  安装成功!')
        else:
            print('  安装失败:', result.stderr[:200])
    except Exception as e:
        print('  安装错误:', str(e))
