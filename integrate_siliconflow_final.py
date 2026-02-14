import json
import sys

def integrate_siliconflow():
    """集成 Silicon Flow 到 OpenClaw 配置"""
    
    config_path = r"C:\Users\殇\.openclaw\openclaw.json"
    
    # 读取配置
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    print("✅ 读取配置成功")
    
    # 1. 添加 Silicon Flow provider
    siliconflow_provider = {
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
    
    config['models']['providers']['siliconflow'] = siliconflow_provider
    print("✅ 添加 provider: siliconflow")
    
    # 2. 添加 auth profile
    config['auth']['profiles']['siliconflow:default'] = {
        "provider": "siliconflow",
        "mode": "api_key"
    }
    print("✅ 添加 auth profile: siliconflow:default")
    
    # 3. 添加到 fallbacks
    fallback_model = "siliconflow/deepseek-ai/DeepSeek-V2.5"
    if 'fallbacks' not in config['agents']['defaults']['model']:
        config['agents']['defaults']['model']['fallbacks'] = []
    
    if fallback_model not in config['agents']['defaults']['model']['fallbacks']:
        config['agents']['defaults']['model']['fallbacks'].append(fallback_model)
    print(f"✅ 添加 fallback: {fallback_model}")
    
    # 4. 添加模型别名
    config['agents']['defaults']['models']['siliconflow/deepseek-ai/DeepSeek-V2.5'] = {
        "alias": "deepseek"
    }
    print("✅ 添加 alias: deepseek")
    
    # 保存配置
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print("\n🎉 Silicon Flow 集成完成！")
    print("\n📋 集成摘要:")
    print("- Provider: siliconflow")
    print("- Model: deepseek-ai/DeepSeek-V2.5") 
    print("- Endpoint: https://api.siliconflow.cn/v1")
    print("- Alias: deepseek")
    print("- Fallback: siliconflow/deepseek-ai/DeepSeek-V2.5")
    print("\n💡 下一步:")
    print("  1. 设置环境变量: $env:SILICONFLOW_API_KEY = '你的密钥'")
    print("  2. 重启 OpenClaw")
    print("  3. 使用命令: model deepseek")

if __name__ == "__main__":
    try:
        integrate_siliconflow()
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)