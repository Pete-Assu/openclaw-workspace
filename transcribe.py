#!/usr/bin/env python3
"""OGG 语音转写脚本 - 使用本地 Whisper + 自定义音频加载"""

import sys
import os
import whisper
import librosa
import numpy as np

# 覆盖 whisper 的 load_audio 函数
def custom_load_audio(filename, sr: int = 16000):
    """加载音频文件 (支持 OGG)"""
    audio, sr = librosa.load(filename, sr=sr, mono=True)
    return audio.astype(np.float32)

# 替换 whisper 的函数
whisper.audio.load_audio = custom_load_audio

def transcribe_audio(audio_path, model_name="base", language="Chinese"):
    """转写音频"""
    print(f"加载模型: {model_name}...")
    model = whisper.load_model(model_name)
    
    print(f"转写中: {audio_path}...")
    result = model.transcribe(audio_path, language=language)
    
    return result["text"]

def main():
    if len(sys.argv) < 2:
        print("用法: python transcribe.py <audio.ogg> [--model base|tiny|small|medium|large] [--language zh|en]")
        sys.exit(1)
    
    audio_path = sys.argv[1]
    model_name = "base"
    language = "Chinese"
    
    # 解析参数
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--model":
            model_name = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--language":
            language = sys.argv[i + 1]
            i += 2
        else:
            i += 1
    
    if not os.path.exists(audio_path):
        print(f"错误: 文件不存在 {audio_path}")
        sys.exit(1)
    
    print(f"文件: {audio_path}")
    
    # 转写 (librosa 直接支持 ogg)
    text = transcribe_audio(audio_path, model_name, language)
    
    print("\n===== 转写结果 =====")
    print(text.strip())
    print("====================")
    
    # 保存结果
    txt_path = os.path.splitext(audio_path)[0] + '.txt'
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(text.strip())
    print(f"已保存到: {txt_path}")

if __name__ == "__main__":
    main()
