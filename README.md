# 🍎 卡路里小助手

一个可爱的食物热量查看器，帮助你了解各种食物的卡路里含量！

## ✨ 特性

- 🎨 **可爱卡通风格** - 粉色主题，俏皮动画效果
- 📊 **五星热量等级** - 直观显示食物热量程度
- 🔍 **智能分类** - 饮料、零食、肉类、水果、甜品
- 📱 **响应式设计** - 支持手机和桌面端
- 🕷️ **数据爬取** - 从维基百科获取真实营养数据
- ⚡ **快速查看** - 常见食物规格（330ml 可乐、70g 薯片等）

## 🏗️ 项目结构

```
CalorieChecker/
├── frontend/          # Vue3 前端项目
│   ├── src/
│   │   ├── components/    # 可复用组件
│   │   ├── views/        # 页面视图
│   │   ├── stores/       # Pinia状态管理
│   │   └── types/        # TypeScript类型定义
├── backend/           # Python 后端API
│   ├── main.py           # FastAPI服务器
│   ├── scraper.py        # 维基百科爬虫
│   └── requirements.txt  # Python依赖
└── start.bat          # 一键启动脚本
```

## 🚀 快速开始

### 方法一：使用启动脚本（推荐）

1. 双击运行 `start.bat` 文件
2. 等待依赖安装和服务启动
3. 浏览器访问 http://localhost:3000

### 方法二：手动启动

#### 启动后端

```bash
cd backend
pip install -r requirements.txt
python main.py
```

#### 启动前端

```bash
cd frontend
npm install
npm run dev
```

## 📋 API 接口

- `GET /api/foods` - 获取所有食物数据
- `GET /api/foods/category/{category}` - 按分类获取食物
- `POST /api/foods/search` - 搜索食物热量
- `GET /api/stats` - 获取统计信息

访问 http://localhost:8000/docs 查看完整 API 文档

## 🎯 热量等级说明

- ⭐ **1 星** - 低热量 (≤100 千卡) 😊
- ⭐⭐ **2 星** - 较低热量 (101-200 千卡) 🙂
- ⭐⭐⭐ **3 星** - 适量享用 (201-300 千卡) 😐
- ⭐⭐⭐⭐ **4 星** - 要注意啦 (301-450 千卡) 😟
- ⭐⭐⭐⭐⭐ **5 星** - 高热量 (>450 千卡) 😱

## 🍔 预置食物

项目包含常见食物的热量数据：

- 🥤 可乐 (330ml/500ml)
- 🍟 薯片 (70g)
- 🍗 鸡腿 (1 只)
- 🍎 苹果 (1 个)
- 🍌 香蕉 (1 根)
- 🍫 巧克力 (30g)
- 🍰 蛋糕 (1 块)
- 🍔 汉堡 (1 个)
- 🧃 橙汁 (250ml)

## 🛠️ 技术栈

### 前端

- **Vue 3** - 渐进式 JavaScript 框架
- **TypeScript** - 类型安全
- **Pinia** - 状态管理
- **Vite** - 快速构建工具

### 后端

- **FastAPI** - 现代 Python Web 框架
- **Wikipedia 库** - 维基百科数据获取
- **BeautifulSoup** - HTML 解析
- **Uvicorn** - ASGI 服务器

## 🎨 设计特色

- 粉色渐变背景
- 卡片悬浮动画
- 星级评分动效
- 可爱 emoji 装饰
- 毛玻璃效果

## 📝 开发说明

### 添加新食物

1. 在 `backend/scraper.py` 的 `DEFAULT_FOODS` 中添加
2. 或通过 API 接口 `POST /api/foods/add` 动态添加

### 自定义分类

修改 `frontend/src/stores/foodStore.ts` 中的 `categories` 数组

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

---

💖 用爱制作，让健康生活更有趣！
