@echo off
chcp 65001 >nul

echo 🍎 卡路里小助手 Docker 部署脚本
echo ================================

:: 检查Docker是否安装
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker 未安装，请先安装 Docker Desktop
    pause
    exit /b 1
)

docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose 未安装，请先安装 Docker Compose
    pause
    exit /b 1
)

echo ✅ Docker 环境检查通过

echo.
echo 请选择部署模式：
echo 1^) 生产环境 ^(production^)
echo 2^) 开发环境 ^(development^)
set /p choice="请输入选择 (1 或 2): "

if "%choice%"=="1" (
    echo 🚀 启动生产环境...
    docker-compose down
    docker-compose build --no-cache
    docker-compose up -d
    set "frontend_url=http://localhost"
) else if "%choice%"=="2" (
    echo 🛠️ 启动开发环境...
    docker-compose -f docker-compose.dev.yml down
    docker-compose -f docker-compose.dev.yml build --no-cache
    docker-compose -f docker-compose.dev.yml up -d
    set "frontend_url=http://localhost:5173"
) else (
    echo ❌ 无效选择
    pause
    exit /b 1
)

echo.
echo ⏳ 等待服务启动...
timeout /t 10 /nobreak >nul

echo 📊 服务状态检查:
docker-compose ps

echo.
echo 🎉 部署完成!
echo.
echo 📱 前端访问地址: %frontend_url%
echo 🔧 后端API地址: http://localhost:8000
echo.
echo 📖 查看日志: docker-compose logs -f
echo 🛑 停止服务: docker-compose down

pause
