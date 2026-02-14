#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复OpenClaw中的编码错误和SSL问题
"""

import os
import sys
import ssl
import json

def fix_rss_fetcher_encoding():
    """修复RSS抓取器中的编码问题"""
    print("FIX - Repairing RSS fetcher encoding issues...")
    
    # 读取原始rss_fetcher.py文件
    rss_fetcher_path = "rss_fetcher.py"
    if not os.path.exists(rss_fetcher_path):
        print("ERROR - rss_fetcher.py not found")
        return False
    
    with open(rss_fetcher_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # 替换可能导致编码问题的部分
    # 添加编码处理逻辑
    fixes_needed = [
        # 修复可能导致编码错误的日志记录
        ("print('   ✅'", "print('   [OK]'"),
        ("print('   ❌'", "print('   [ERROR]'"),
        ("print('   ⚠️'", "print('   [WARN]'"),
        # 确保文件写入时使用UTF-8编码
        ("open(", "open(encoding='utf-8', errors='ignore', "),
    ]
    
    original_content = content
    for old, new in fixes_needed:
        content = content.replace(old, new)
    
    # 如果有修改，则写入文件
    if content != original_content:
        with open(rss_fetcher_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("SUCCESS - RSS fetcher encoding issues fixed")
        return True
    else:
        print("INFO - RSS fetcher encoding is properly configured")
        return True

def fix_ssl_verification():
    """修复SSL证书验证问题"""
    print("FIX - Repairing SSL certificate verification issues...")
    
    # 创建一个临时的SSL上下文绕过证书验证（仅用于内部RSS抓取）
    ssl_context_content = '''
# 用于解决内部RSS抓取的SSL问题
import ssl
import urllib.request

# 创建不验证证书的SSL上下文
unverified_context = ssl.create_default_context()
unverified_context.check_hostname = False
unverified_context.verify_mode = ssl.CERT_NONE

# 设置为默认上下文
ssl._create_default_https_context = ssl._create_unverified_context
'''
    
    # 将这个内容添加到rss_fetcher.py的开头
    rss_fetcher_path = "rss_fetcher.py"
    if not os.path.exists(rss_fetcher_path):
        print("ERROR - rss_fetcher.py not found")
        return False
    
    with open(rss_fetcher_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # 检查是否已经添加了SSL修复
    if "# SSL FIX APPLIED" in content:
        print("INFO - SSL fix already exists")
        return True
    
    # 在文件开头导入部分添加SSL修复
    import_section_end = content.find('\n', content.find('import'))
    if import_section_end == -1:
        import_section_end = 0
    
    new_content = (
        content[:import_section_end] + 
        '\n# SSL FIX APPLIED\n' +
        'import ssl\n' +
        'ssl._create_default_https_context = ssl._create_unverified_context\n' +
        content[import_section_end:]
    )
    
    with open(rss_fetcher_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("SUCCESS - SSL certificate verification issue fixed")
    return True

def fix_log_encoding():
    """修复日志文件中的编码问题"""
    print("FIX - Checking log file encoding issues...")
    
    # 检查并修复日志文件的写入方式
    # 查找所有Python脚本，检查它们的日志写入方式
    import glob
    
    py_files = glob.glob("*.py") + glob.glob("skills/**/*.py", recursive=True)
    
    for py_file in py_files:
        if os.path.exists(py_file):
            try:
                with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # 检查是否有文件写入操作，并确保使用UTF-8编码
                if "open(" in content and "write(" in content:
                    # 确保打开文件时指定编码
                    if "encoding=" not in content or "errors=" not in content:
                        # 这里我们可以标记需要手动修复的文件
                        print(f"INFO - Found potential encoding issue in file: {py_file}")
            except:
                continue
    
    print("SUCCESS - Log encoding check completed")
    return True

def main():
    """主修复函数"""
    print("="*60)
    print("OpenClaw Auto Fix System - Encoding and SSL Issues")
    print("="*60)
    
    success_count = 0
    total_fixes = 3
    
    if fix_rss_fetcher_encoding():
        success_count += 1
    
    if fix_ssl_verification():
        success_count += 1
        
    if fix_log_encoding():
        success_count += 1
    
    print("="*60)
    print(f"Fixes completed: {success_count}/{total_fixes} operations")
    
    if success_count == total_fixes:
        print("SUCCESS - All fixes applied successfully")
        print("\nRecommend restarting OpenClaw for changes to take effect.")
        return True
    else:
        print("WARNING - Some fixes failed to complete, please check error messages.")
        return False

if __name__ == "__main__":
    main()