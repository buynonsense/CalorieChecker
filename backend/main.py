from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
import json
import os

app = FastAPI(title="卡路里小助手 API", description="可爱的食物热量查询API", version="2.0.0")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # 前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据模型
class FoodItem(BaseModel):
    id: str
    name: str
    category: str
    calories: int
    calorie_level: int
    portion: str
    emoji: str
    description: str
    source: Optional[str] = ""
    summary: Optional[str] = ""

class SearchQuery(BaseModel):
    query: str
    category: Optional[str] = None

# 全局变量
foods_data: List[Dict[str, Any]] = []
categories_mapping = {
    "staples": {"name": "主食", "emoji": "🍚"},
    "drinks": {"name": "饮料", "emoji": "🥤"},
    "fruits": {"name": "水果", "emoji": "🍎"},
    "vegetables": {"name": "蔬菜", "emoji": "🥬"},
    "meat": {"name": "肉类", "emoji": "🥩"},
    "snacks": {"name": "零食", "emoji": "🍿"},
    "dairy": {"name": "乳制品", "emoji": "🥛"},
    "desserts": {"name": "甜品", "emoji": "🍰"},
    "other": {"name": "其他", "emoji": "🍽️"}
}

def load_food_data():
    """加载食物数据"""
    global foods_data
    data_file = os.path.join(os.path.dirname(__file__), "data.json")
    
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            foods_data = json.load(f)
        print(f"✅ 成功加载 {len(foods_data)} 条食物数据")
    except FileNotFoundError:
        print("❌ data.json 文件未找到")
        foods_data = []
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析错误: {e}")
        foods_data = []

@app.on_event("startup")
async def startup_event():
    """应用启动时初始化数据"""
    load_food_data()

# API 路由
@app.get("/", summary="欢迎页面")
async def root():
    return {
        "message": "🎉 欢迎使用卡路里小助手 API!",
        "description": "可爱的食物热量查询API",
        "docs_url": "/docs",
        "total_foods": len(foods_data)
    }

@app.get("/api/foods", response_model=List[FoodItem], summary="获取所有食物")
async def get_all_foods(
    limit: Optional[int] = Query(None, description="限制返回数量"),
    offset: Optional[int] = Query(0, description="偏移量")
):
    """获取所有食物列表"""
    total = len(foods_data)
    
    if limit is None:
        result = foods_data[offset:]
    else:
        result = foods_data[offset:offset + limit]
    
    return [FoodItem(**food) for food in result]

@app.get("/api/foods/search", response_model=List[FoodItem], summary="搜索食物")
async def search_foods(
    q: str = Query(..., description="搜索关键词"),
    category: Optional[str] = Query(None, description="类别筛选"),
    limit: Optional[int] = Query(20, description="限制返回数量")
):
    """搜索食物"""
    if not q.strip():
        raise HTTPException(status_code=400, detail="搜索关键词不能为空")
    
    # 过滤数据
    filtered_foods = []
    query_lower = q.lower()
    
    for food in foods_data:
        # 搜索名称
        if query_lower in food['name'].lower():
            # 如果指定了类别，再过滤类别
            if category is None or food['category'] == category:
                filtered_foods.append(food)
    
    # 限制返回数量
    if limit:
        filtered_foods = filtered_foods[:limit]
    
    return [FoodItem(**food) for food in filtered_foods]

@app.get("/api/foods/category/{category}", response_model=List[FoodItem], summary="按类别获取食物")
async def get_foods_by_category(
    category: str,
    limit: Optional[int] = Query(20, description="限制返回数量"),
    offset: Optional[int] = Query(0, description="偏移量")
):
    """按类别获取食物"""
    if category not in categories_mapping:
        raise HTTPException(status_code=404, detail=f"类别 '{category}' 不存在")
    
    # 过滤指定类别的食物
    category_foods = [food for food in foods_data if food['category'] == category]
    
    # 分页
    if limit:
        result = category_foods[offset:offset + limit]
    else:
        result = category_foods[offset:]
    
    return [FoodItem(**food) for food in result]

@app.get("/api/foods/{food_id}", response_model=FoodItem, summary="获取单个食物详情")
async def get_food_by_id(food_id: str):
    """根据ID获取食物详情"""
    for food in foods_data:
        if food['id'] == food_id:
            return FoodItem(**food)
    
    raise HTTPException(status_code=404, detail=f"未找到ID为 '{food_id}' 的食物")

@app.get("/api/categories", summary="获取所有类别")
async def get_categories():
    """获取所有食物类别"""
    # 统计每个类别的食物数量
    category_counts = {}
    for food in foods_data:
        category = food['category']
        category_counts[category] = category_counts.get(category, 0) + 1
    
    # 返回类别信息
    categories = []
    for category, mapping in categories_mapping.items():
        categories.append({
            "id": category,
            "name": mapping["name"],
            "emoji": mapping["emoji"],
            "count": category_counts.get(category, 0)
        })
    
    return {
        "categories": categories,
        "total": len(foods_data)
    }

@app.get("/api/stats", summary="获取统计信息")
async def get_stats():
    """获取食物数据统计信息"""
    if not foods_data:
        return {"message": "暂无数据"}
    
    # 计算统计信息
    total_foods = len(foods_data)
    calories_list = [food['calories'] for food in foods_data]
    
    avg_calories = sum(calories_list) / total_foods
    max_calories = max(calories_list)
    min_calories = min(calories_list)
    
    # 热量等级分布
    calorie_levels = {}
    for food in foods_data:
        level = food['calorie_level']
        calorie_levels[level] = calorie_levels.get(level, 0) + 1
    
    # 类别分布
    category_distribution = {}
    for food in foods_data:
        category = food['category']
        category_distribution[category] = category_distribution.get(category, 0) + 1
    
    return {
        "total_foods": total_foods,
        "calories_stats": {
            "average": round(avg_calories, 2),
            "max": max_calories,
            "min": min_calories
        },
        "calorie_level_distribution": calorie_levels,
        "category_distribution": category_distribution
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
