#!/bin/bash

# 卡路里小助手 Docker 部署脚本

echo "🍎 卡路里小助手 Docker 部署脚本"
echo "================================"

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，请先安装 Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose 未安装，请先安装 Docker Compose"
    exit 1
fi

echo "✅ Docker 环境检查通过"

# 选择部署模式
echo ""
echo "请选择部署模式："
echo "1) 生产环境 (production)"
echo "2) 开发环境 (development)"
read -p "请输入选择 (1 或 2): " choice

case $choice in
    1)
        echo "🚀 启动生产环境..."
        docker-compose down
        docker-compose build --no-cache
        docker-compose up -d
        ;;
    2)
        echo "🛠️ 启动开发环境..."
        docker-compose -f docker-compose.dev.yml down
        docker-compose -f docker-compose.dev.yml build --no-cache
        docker-compose -f docker-compose.dev.yml up -d
        ;;
    *)
        echo "❌ 无效选择"
        exit 1
        ;;
esac

echo ""
echo "⏳ 等待服务启动..."
sleep 10

# 检查服务状态
echo "📊 服务状态检查:"
docker-compose ps

echo ""
echo "🎉 部署完成!"
echo ""
if [ $choice -eq 1 ]; then
    echo "📱 前端访问地址: http://localhost"
    echo "🔧 后端API地址: http://localhost:8000"
else
    echo "📱 前端访问地址: http://localhost:5173"
    echo "🔧 后端API地址: http://localhost:8000"
fi
echo ""
echo "📖 查看日志: docker-compose logs -f"
echo "🛑 停止服务: docker-compose down"
