#!/bin/bash
# 透明代理自动配置脚本
# 支持: OpenWrt / LEDE / 梅林 / 原厂 (需支持 iptables)
# 代理: Clash / V2Ray / Xray

set -e

# ================ 配置区 ================
ROUTER_IP="192.168.2.1"          # 路由器IP
SSH_PORT="22"                  # SSH端口
SSH_USER="root"                # 用户名
SSH_PASS="password"            # 密码（或使用SSH_KEY）
# SSH_KEY="/path/to/key"       # 密钥认证（注释掉则用密码）

PROXY_TYPE="clash"            # clash / v2ray / xray
PROXY_PORT="7892"             # 代理监听端口
PROXY_UI_PORT="9090"          # 控制面板端口

# ================ 透明代理规则 ================
# 哪些IP走代理（CIDR格式）
PROXY_SUBNETS=(
    "192.168.1.0/24"          # 整个局域网
)

# 哪些IP直连
DIRECT_SUBNETS=(
    "192.168.0.0/16"          # 私有地址
    "10.0.0.0/8"
    "172.16.0.0/12"
    "127.0.0.0/8"
    "224.0.0.0/4"
    "192.168.100.0/24"        # 路由器管理网段
)

# ================ 脚本开始 ================
echo "🚀 透明代理配置脚本"
echo "========================"

# 检测代理进程
detect_proxy() {
    if [ "$PROXY_TYPE" = "clash" ]; then
        echo "📡 检测 Clash..."
        ssh -p $SSH_PORT $SSH_USER@$ROUTER_IP "pidof clash && echo 'Clash 运行中' || echo 'Clash 未运行'"
    fi
}

# 安装/配置透明代理
setup_transparent_proxy() {
    echo "⚙️ 配置透明代理..."
    
    # 生成透明代理配置
    ssh -p $SSH_PORT $SSH_USER@$ROUTER_IP << 'PROXY_SCRIPT'
        
        # 检测系统类型
        if [ -f /etc/openwrt_release ]; then
            SYSTEM="OpenWrt"
        elif [ -f /etc，梅林_version ]; then
            SYSTEM="Asuswrt-Merlin"
        else
            SYSTEM="Unknown"
        fi
        
        echo "📟 检测到系统: $SYSTEM"
        
        # 创建透明代理规则
        # iptables 规则说明：
        # 1. PREROUTING - 转发流量
        # 2. OUTPUT - 本机流量
        # 3. TPROXY - 透明代理转发
        
        # 清空旧规则
        iptables -t nat -F PREROUTING 2>/dev/null || true
        iptables -t nat -F OUTPUT 2>/dev/null || true
        
        # 创建新的透明代理链
        iptables -t nat -N PROXY
        
        # 直连规则（本地网段）
        iptables -t nat -A PROXY -d 192.168.0.0/16 -j RETURN
        iptables -t nat -A PROXY -d 10.0.0.0/8 -j RETURN
        iptables -t nat -A PROXY -d 172.16.0.0/12 -j RETURN
        iptables -t nat -A PROXY -d 127.0.0.0/8 -j RETURN
        iptables -t nat -A PROXY -d 224.0.0.0/4 -j RETURN
        
        # 代理规则（其他流量转发到代理端口）
        # Clash 默认为 7892 端口
        iptables -t nat -A PROXY -p tcp -j REDIRECT --to-ports 7892
        
        # 应用到 PREROUTING（影响LAN设备）
        iptables -t nat -I PREROUTING -j PROXY
        
        # 应用到 OUTPUT（影响路由器自身）
        iptables -t nat -I OUTPUT -j PROXY 2>/dev/null || true
        
        echo "✅ iptables 规则已创建"
        iptables -t nat -L PROXY -n -v
        
PROXY_SCRIPT

}

# 测试透明代理
test_transparent_proxy() {
    echo "🧪 测试透明代理..."
    ssh -p $SSH_PORT $SSH_USER@$ROUTER_IP "curl -s --connect-timeout 5 https://api.ipify.org || echo '无法访问外网'"
}

# 启用/禁用透明代理
toggle_proxy() {
    local enable=$1
    ssh -p $SSH_PORT $SSH_USER@$ROUTER_IP << PROXY_TOGGLE
        
        if [ "$enable" = "true" ]; then
            echo "🚀 启用透明代理..."
            iptables -t nat -I PREROUTING -j PROXY 2>/dev/null || echo "规则已存在"
        else
            echo "🛑 禁用透明代理..."
            iptables -t nat -D PREROUTING -j PROXY 2>/dev/null || echo "规则不存在"
        fi
        
        echo "当前状态:"
        iptables -t nat -L PREROUTING -n -v | head -10
        
PROXY_TOGGLE
}

# 主菜单
case "$1" in
    "install")
        setup_transparent_proxy
        ;;
    "test")
        test_transparent_proxy
        ;;
    "enable")
        toggle_proxy "true"
        ;;
    "disable")
        toggle_proxy "false"
        ;;
    "status")
        detect_proxy
        ssh -p $SSH_PORT $SSH_USER@$ROUTER_IP "iptables -t nat -L PREROUTING -n -v | head -5"
        ;;
    *)
        echo "用法: $0 {install|test|enable|disable|status}"
        echo ""
        echo "命令说明:"
        echo "  install  - 安装并配置透明代理"
        echo "  test     - 测试代理是否正常"
        echo "  enable   - 启用透明代理"
        echo "  disable  - 禁用透明代理"
        echo "  status   - 查看当前状态"
        ;;
esac
