@echo off
chcp 65001 >nul

echo 🍎 卡路里小助手 Docker Hub 推送脚本
echo ================================

:: 配置变量
set DOCKER_USERNAME=nn1044746809
set IMAGE_NAME=calorie-checker
set VERSION=latest

:: 检查用户名配置
if "%DOCKER_USERNAME%"=="your-dockerhub-username" (
    echo ❌ 请先配置你的 Docker Hub 用户名
    echo 编辑 push-to-dockerhub.bat 文件，将 DOCKER_USERNAME 改为你的用户名
    pause
    exit /b 1
)

:: 检查Docker是否运行
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker 未运行，请启动 Docker Desktop
    pause
    exit /b 1
)


:: 提示用户输入版本号
echo.
echo 请输入版本号 ^(默认: latest^):
set /p user_version="版本号: "
if not "%user_version%"=="" set VERSION=%user_version%

echo.
echo 📋 构建信息:
echo   Docker Hub 用户名: %DOCKER_USERNAME%
echo   镜像名称: %IMAGE_NAME%
echo   版本: %VERSION%
echo.

:: 确认推送
echo 是否继续推送? ^(输入 y 继续，其他任意键取消^)
choice /c yn /n /m "请选择 [y/n]: "
if %errorlevel% neq 1 (
    echo ❌ 取消推送
    pause
    exit /b 0
)

echo.
echo 🏗️ 开始构建镜像...

:: 构建后端镜像
echo 📦 构建后端镜像...
if not exist "backend\Dockerfile" (
    echo ❌ 后端 Dockerfile 不存在
    pause
    exit /b 1
)

cd backend
docker build -t %DOCKER_USERNAME%/%IMAGE_NAME%-backend:%VERSION% .
if %errorlevel% neq 0 (
    echo ❌ 后端镜像构建失败
    cd ..
    pause
    exit /b 1
)
cd ..

:: 构建前端镜像
echo 📦 构建前端镜像...
if not exist "frontend\Dockerfile" (
    echo ❌ 前端 Dockerfile 不存在
    pause
    exit /b 1
)

cd frontend
docker build -t %DOCKER_USERNAME%/%IMAGE_NAME%-frontend:%VERSION% .
if %errorlevel% neq 0 (
    echo ❌ 前端镜像构建失败
    cd ..
    pause
    exit /b 1
)
cd ..

echo ✅ 镜像构建完成

:: 推送镜像
echo.
echo 🚀 推送镜像到 Docker Hub...

echo 📤 推送后端镜像...
docker push %DOCKER_USERNAME%/%IMAGE_NAME%-backend:%VERSION%
if %errorlevel% neq 0 (
    echo ❌ 后端镜像推送失败
    pause
    exit /b 1
)

echo 📤 推送前端镜像...
docker push %DOCKER_USERNAME%/%IMAGE_NAME%-frontend:%VERSION%
if %errorlevel% neq 0 (
    echo ❌ 前端镜像推送失败
    pause
    exit /b 1
)

:: 创建并推送 latest 标签
if not "%VERSION%"=="latest" (
    echo 🏷️ 创建 latest 标签...
    docker tag %DOCKER_USERNAME%/%IMAGE_NAME%-backend:%VERSION% %DOCKER_USERNAME%/%IMAGE_NAME%-backend:latest
    docker tag %DOCKER_USERNAME%/%IMAGE_NAME%-frontend:%VERSION% %DOCKER_USERNAME%/%IMAGE_NAME%-frontend:latest
    
    echo 📤 推送 latest 标签...
    docker push %DOCKER_USERNAME%/%IMAGE_NAME%-backend:latest
    docker push %DOCKER_USERNAME%/%IMAGE_NAME%-frontend:latest
)

echo.
echo 🎉 推送完成!
echo 📖 Docker Hub 链接:
echo   后端: https://hub.docker.com/r/%DOCKER_USERNAME%/%IMAGE_NAME%-backend
echo   前端: https://hub.docker.com/r/%DOCKER_USERNAME%/%IMAGE_NAME%-frontend
echo.
echo 🚀 使用方法:
echo   docker pull %DOCKER_USERNAME%/%IMAGE_NAME%-backend:%VERSION%
echo   docker pull %DOCKER_USERNAME%/%IMAGE_NAME%-frontend:%VERSION%
echo.
echo 💡 提示: 可以使用 docker-compose.hub.yml 一键部署

pause
