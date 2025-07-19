#!/bin/bash

# 卡路里小助手 Docker Hub 推送脚本
# 使用前请先登录: docker login

# 配置变量
DOCKER_USERNAME="nn1044746809"  # 替换为你的Docker Hub用户名
IMAGE_NAME="calorie-checker"
VERSION="latest"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🍎 卡路里小助手 Docker Hub 推送脚本${NC}"
echo "================================"

# 检查Docker是否登录
if ! docker info >/dev/null 2>&1; then
    echo -e "${RED}❌ Docker 未运行，请启动 Docker Desktop${NC}"
    exit 1
fi

# 检查用户名配置
if [ "$DOCKER_USERNAME" = "your-dockerhub-username" ]; then
    echo -e "${RED}❌ 请先在脚本中配置你的 Docker Hub 用户名${NC}"
    echo -e "${YELLOW}编辑 push-to-dockerhub.sh 文件，将 DOCKER_USERNAME 改为你的用户名${NC}"
    exit 1
fi

# 提示用户选择版本
echo -e "${YELLOW}请输入版本号 (默认: latest):${NC}"
read -p "版本号: " user_version
if [ ! -z "$user_version" ]; then
    VERSION=$user_version
fi

echo -e "${BLUE}📋 构建信息:${NC}"
echo "  Docker Hub 用户名: $DOCKER_USERNAME"
echo "  镜像名称: $IMAGE_NAME"
echo "  版本: $VERSION"
echo ""

# 确认推送
echo -e "${YELLOW}是否继续推送? (y/n):${NC}"
read -p "确认: " confirm
if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo -e "${YELLOW}❌ 取消推送${NC}"
    exit 0
fi

echo -e "${BLUE}🏗️ 开始构建镜像...${NC}"

# 构建后端镜像
echo -e "${BLUE}📦 构建后端镜像...${NC}"
cd backend
docker build -t $DOCKER_USERNAME/$IMAGE_NAME-backend:$VERSION .
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ 后端镜像构建失败${NC}"
    exit 1
fi
cd ..

# 构建前端镜像
echo -e "${BLUE}📦 构建前端镜像...${NC}"
cd frontend
docker build -t $DOCKER_USERNAME/$IMAGE_NAME-frontend:$VERSION .
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ 前端镜像构建失败${NC}"
    exit 1
fi
cd ..

echo -e "${GREEN}✅ 镜像构建完成${NC}"

# 推送镜像
echo -e "${BLUE}🚀 推送镜像到 Docker Hub...${NC}"

echo -e "${BLUE}📤 推送后端镜像...${NC}"
docker push $DOCKER_USERNAME/$IMAGE_NAME-backend:$VERSION
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ 后端镜像推送失败${NC}"
    exit 1
fi

echo -e "${BLUE}📤 推送前端镜像...${NC}"
docker push $DOCKER_USERNAME/$IMAGE_NAME-frontend:$VERSION
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ 前端镜像推送失败${NC}"
    exit 1
fi

# 创建并推送 latest 标签
if [ "$VERSION" != "latest" ]; then
    echo -e "${BLUE}🏷️ 创建 latest 标签...${NC}"
    docker tag $DOCKER_USERNAME/$IMAGE_NAME-backend:$VERSION $DOCKER_USERNAME/$IMAGE_NAME-backend:latest
    docker tag $DOCKER_USERNAME/$IMAGE_NAME-frontend:$VERSION $DOCKER_USERNAME/$IMAGE_NAME-frontend:latest
    
    docker push $DOCKER_USERNAME/$IMAGE_NAME-backend:latest
    docker push $DOCKER_USERNAME/$IMAGE_NAME-frontend:latest
fi

echo ""
echo -e "${GREEN}🎉 推送完成!${NC}"
echo -e "${BLUE}📖 Docker Hub 链接:${NC}"
echo "  后端: https://hub.docker.com/r/$DOCKER_USERNAME/$IMAGE_NAME-backend"
echo "  前端: https://hub.docker.com/r/$DOCKER_USERNAME/$IMAGE_NAME-frontend"
echo ""
echo -e "${BLUE}🚀 使用方法:${NC}"
echo "  docker pull $DOCKER_USERNAME/$IMAGE_NAME-backend:$VERSION"
echo "  docker pull $DOCKER_USERNAME/$IMAGE_NAME-frontend:$VERSION"
echo ""
echo -e "${YELLOW}💡 提示: 记得在 docker-compose.yml 中更新镜像名称${NC}"
