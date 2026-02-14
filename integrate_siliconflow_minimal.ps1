# Silicon Flow OpenClaw 集成脚本
# 使用方法：以管理员身份运行此脚本即可完成配置

$configPath = "C:\Users\殇\.openclaw\openclaw.json"
Write-Host "Integration started..."

# 读取当前配置
$jsonContent = Get-Content $configPath -Raw -Encoding UTF8
$config = $jsonContent | ConvertFrom-Json

# 创建 SiliconFlow provider 结构
$siliconflowProvider = @{baseUrl="https://api.siliconflow.cn/v1";apiKey="siliconflow-api-key";api="openai-completions";models=@(@{id="deepseek-ai/DeepSeek-V2.5";name="DeepSeek V2.5";reasoning=$false;input=@("text");cost=@{input=0.5;output=1.0;cacheRead=0.1;cacheWrite=0.2};contextWindow=128000;maxTokens=8192})}

# 添加 provider
$config.models.providers | Add-Member -NotePropertyMembers $siliconflowProvider -Name "siliconflow" -ErrorAction SilentlyContinue

# 添加 auth profile  
$config.auth.profiles | Add-Member -NotePropertyMembers @{provider="siliconflow";mode="api_key"} -Name "siliconflow:default" -ErrorAction SilentlyContinue

# 添加 fallback
$fallback = "siliconflow/deepseek-ai/DeepSeek-V2.5"
if ($config.agents.defaults.model.fallbacks -notcontains $fallback) {
    $config.agents.defaults.model.fallbacks += $fallback
}

# 添加 alias
$config.agents.defaults.models | Add-Member -NotePropertyMembers @{alias="deepseek"} -Name "siliconflow/deepseek-ai/DeepSeek-V2.5" -ErrorAction SilentlyContinue

# 保存
$config | ConvertTo-Json -Depth 20 | Out-File $configPath -Encoding UTF8

Write-Host "Silicon Flow integration completed!"