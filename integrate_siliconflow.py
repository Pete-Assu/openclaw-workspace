#!/usr/bin/env python3
"""
Add Silicon Flow to OpenClaw configuration
"""

import json
import codecs

def add_siliconflow_config():
    """Add Silicon Flow configuration"""
    
    # 使用 UTF-8 编码读取
    config_path = "C:/Users/殇/.openclaw/openclaw.json"
    
    with codecs.open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    print("[OK] Read config successfully")
    
    # 1. Add Silicon Flow provider
    config['models']['providers']['siliconflow'] = {
        "baseUrl": "https://api.siliconflow.cn/v1",
        "apiKey": "siliconflow-api-key",
        "api": "openai-completions",
        "models": [
            {
                "id": "deepseek-ai/DeepSeek-V2.5",
                "name": "DeepSeek V2.5",
                "reasoning": False,
                "input": ["text"],
                "cost": {"input": 0.5, "output": 1.0, "cacheRead": 0.1, "cacheWrite": 0.2},
                "contextWindow": 128000,
                "maxTokens": 8192
            }
        ]
    }
    print("[OK] Added provider: siliconflow")
    
    # 2. Add auth profile
    config['auth']['profiles']['siliconflow:default'] = {
        "provider": "siliconflow",
        "mode": "api_key"
    }
    print("[OK] Added auth profile: siliconflow:default")
    
    # 3. Add to fallbacks
    fallback_model = "siliconflow/deepseek-ai/DeepSeek-V2.5"
    if fallback_model not in config['agents']['defaults']['model']['fallbacks']:
        config['agents']['defaults']['model']['fallbacks'].append(fallback_model)
    print("[OK] Added fallback: " + fallback_model)
    
    # 4. Add model alias
    config['agents']['defaults']['models']['siliconflow/deepseek-ai/DeepSeek-V2.5'] = {
        "alias": "deepseek"
    }
    print("[OK] Added alias: deepseek")
    
    # Save config with UTF-8 BOM
    with codecs.open(config_path, 'w', encoding='utf-8-sig') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print("")
    print("[OK] Silicon Flow integrated into openclaw.json")
    print("")
    print("Config Summary:")
    print("-" * 50)
    print("Provider: siliconflow")
    print("Endpoint: https://api.siliconflow.cn/v1")
    print("Model: deepseek-ai/DeepSeek-V2.5")
    print("Auth Mode: api_key")
    print("Fallback: siliconflow/deepseek-ai/DeepSeek-V2.5")
    print("Alias: deepseek")
    print("-" * 50)
    
    return True

if __name__ == "__main__":
    try:
        add_siliconflow_config()
        print("")
        print("[DONE] Integration complete!")
    except Exception as e:
        print("[ERROR] " + str(e))
        import traceback
        traceback.print_exc()