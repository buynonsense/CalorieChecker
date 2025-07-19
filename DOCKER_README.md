# 🍎 卡路里小助手 - Docker 部署指南

一个可爱的食物热量查询应用，采用 Vue 3 + FastAPI 架构，支持 Docker 容器化部署。

## 📋 项目特性

- 🎨 **可爱界面**: 粉色主题，卡通风格 UI
- 📱 **响应式设计**: 支持 PC 和移动端
- 🔍 **智能搜索**: 实时搜索食物信息
- 📊 **数据丰富**: 6000+食物热量数据
- ⭐ **星级评分**: 五星制热量等级
- 🏷️ **分类筛选**: 多种食物分类

## 🏗️ 项目结构

```
CalorieChecker/
├── backend/                 # FastAPI 后端
│   ├── main.py             # 主应用文件
│   ├── data.json           # 食物数据
│   ├── requirements.txt    # Python依赖
│   └── Dockerfile          # 后端Docker配置
├── frontend/               # Vue 3 前端
│   ├── src/                # 源代码
│   ├── package.json        # Node.js依赖
│   ├── Dockerfile          # 生产环境Docker配置
│   ├── Dockerfile.dev      # 开发环境Docker配置
│   └── nginx.conf          # Nginx配置
├── docker-compose.yml      # 生产环境编排
├── docker-compose.dev.yml  # 开发环境编排
├── deploy.sh              # Linux/Mac部署脚本
└── deploy.bat             # Windows部署脚本
```

## 🚀 快速开始

### 前提条件

- Docker Desktop
- Docker Compose

### 方法一：使用部署脚本（推荐）

**Windows 用户:**

```bash
deploy.bat
```

**Linux/Mac 用户:**

```bash
chmod +x deploy.sh
./deploy.sh
```

### 方法二：手动部署

**生产环境:**

```bash
# 构建并启动服务
docker-compose up -d --build

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

**开发环境:**

```bash
# 构建并启动开发服务
docker-compose -f docker-compose.dev.yml up -d --build

# 查看日志
docker-compose -f docker-compose.dev.yml logs -f
```

## 🌐 访问地址

### 生产环境

- **前端应用**: http://localhost
- **后端 API**: http://localhost:8000
- **API 文档**: http://localhost:8000/docs

### 开发环境

- **前端应用**: http://localhost:5173
- **后端 API**: http://localhost:8000
- **API 文档**: http://localhost:8000/docs

## 🛠️ 常用命令

```bash
# 查看运行状态
docker-compose ps

# 查看日志
docker-compose logs -f [service_name]

# 停止服务
docker-compose down

# 重启服务
docker-compose restart

# 删除容器和镜像
docker-compose down --rmi all -v

# 进入容器
docker-compose exec backend bash
docker-compose exec frontend sh
```

## 🔧 技术栈

### 后端

- **框架**: FastAPI
- **语言**: Python 3.11
- **数据**: JSON 文件存储
- **部署**: uvicorn + Docker

### 前端

- **框架**: Vue 3
- **语言**: TypeScript
- **构建工具**: Vite
- **状态管理**: Pinia
- **部署**: Nginx + Docker

## 📊 API 接口

| 接口                             | 方法 | 说明             |
| -------------------------------- | ---- | ---------------- |
| `/api/foods`                     | GET  | 获取所有食物     |
| `/api/foods/search`              | GET  | 搜索食物         |
| `/api/foods/category/{category}` | GET  | 按类别获取食物   |
| `/api/foods/{id}`                | GET  | 获取单个食物详情 |
| `/api/categories`                | GET  | 获取所有类别     |
| `/api/stats`                     | GET  | 获取统计信息     |

## 🔍 环境变量

### 后端环境变量

```env
PYTHONPATH=/app
ENVIRONMENT=production
```

### 前端环境变量

```env
VITE_API_BASE_URL=http://localhost:8000
```

## 📝 开发说明

### 后端开发

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### 前端开发

```bash
cd frontend
npm install
npm run dev
```

## 🐛 故障排除

1. **端口占用问题**

   ```bash
   # 查看端口占用
   netstat -ano | findstr :8000
   netstat -ano | findstr :80
   ```

2. **Docker 权限问题**

   ```bash
   # 确保Docker Desktop正在运行
   # Windows用户需要启用WSL2
   ```

3. **构建失败**
   ```bash
   # 清理Docker缓存
   docker system prune -a
   ```

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**即刻体验** 🌟
运行 `deploy.bat` (Windows) 或 `./deploy.sh` (Linux/Mac) 开始你的健康饮食之旅！
