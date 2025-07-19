import requests
import wikipedia
from bs4 import BeautifulSoup
import re
from typing import List, Dict, Optional, Tuple
import json
import os

class WikipediaFoodScraper:
    def __init__(self):
        # 设置中文维基百科
        wikipedia.set_lang("zh")
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'CalorieChecker/1.0 (Educational Purpose)'
        })
        
        # 常见食物的标准分量定义
        self.standard_portions = {
            '可乐': {'amount': 330, 'unit': 'ml'},
            '雪碧': {'amount': 330, 'unit': 'ml'},
            '果汁': {'amount': 250, 'unit': 'ml'},
            '奶茶': {'amount': 500, 'unit': 'ml'},
            '咖啡': {'amount': 240, 'unit': 'ml'},
            '牛奶': {'amount': 250, 'unit': 'ml'},
            '酸奶': {'amount': 150, 'unit': 'g'},
            '鸡腿': {'amount': 100, 'unit': 'g'},
            '鸡翅': {'amount': 100, 'unit': 'g'},
            '牛排': {'amount': 150, 'unit': 'g'},
            '排骨': {'amount': 100, 'unit': 'g'},
            '热狗': {'amount': 1, 'unit': '根'},
            '香肠': {'amount': 100, 'unit': 'g'},
            '汉堡': {'amount': 1, 'unit': '个'},
            '三明治': {'amount': 1, 'unit': '个'},
            '薯片': {'amount': 50, 'unit': 'g'},
            '饼干': {'amount': 100, 'unit': 'g'},
            '巧克力': {'amount': 50, 'unit': 'g'},
            '蛋糕': {'amount': 1, 'unit': '块'},
            '甜甜圈': {'amount': 1, 'unit': '个'},
            '面条': {'amount': 100, 'unit': 'g'},
            '米饭': {'amount': 150, 'unit': 'g'},
            '面包': {'amount': 100, 'unit': 'g'},
            '苹果': {'amount': 1, 'unit': '个'},
            '香蕉': {'amount': 1, 'unit': '根'},
            '橙子': {'amount': 1, 'unit': '个'},
            '土豆': {'amount': 150, 'unit': 'g'},
            '玉米': {'amount': 150, 'unit': 'g'},
            '沙拉': {'amount': 200, 'unit': 'g'},
        }
        
        # 基于真实页面分析的搜索策略优化
        self.search_strategies = {
            '鸡腿': ['鸡肉 营养', '鸡腿肉', '鸡肉 热量', '禽肉 营养'],
            '鸡翅': ['鸡肉 营养', '鸡翅肉', '鸡肉 热量', '禽肉 营养'],
            '可乐': ['可口可乐 营养', '碳酸饮料 热量', '软饮料 营养', '可乐 卡路里'],
            '米饭': ['大米 营养', '稻米 热量', '白米 营养成分', '米饭 卡路里'],
            '面包': ['小麦面包 营养', '面包 热量', '谷物面包 营养成分'],
        }
    
    def get_food_calories(self, food_name: str) -> Optional[Dict]:
        """从维基百科获取食物热量信息 - 基于真实页面分析优化"""
        try:
            # 使用针对性搜索策略
            search_terms = self._get_optimized_search_terms(food_name)
            
            for search_term in search_terms:
                try:
                    print(f"   尝试搜索: {search_term}")
                    search_results = wikipedia.search(search_term, results=5)
                    
                    for result in search_results:
                        try:
                            page = wikipedia.page(result)
                            
                            # 跳过明显不相关的页面
                            if self._is_irrelevant_page(page.title, food_name):
                                continue
                            
                            # 检查页面内容质量
                            if not self._is_food_related_page(page.content, food_name):
                                continue
                            
                            print(f"   分析页面: {page.title}")
                            calories_info = self._extract_calories_from_content(page.content, food_name)
                            if calories_info:
                                print(f"   ✅ 找到数据: {calories_info['calories']}卡/{calories_info['portion']}")
                                return {
                                    'name': food_name,
                                    'calories': calories_info['calories'],
                                    'portion': calories_info['portion'],
                                    'original_data': calories_info['original_data'],
                                    'source': page.url,
                                    'summary': page.summary[:200] + "..."

                                }
                                
                        except wikipedia.exceptions.DisambiguationError as e:
                            # 智能处理歧义页面
                            best_option = self._find_best_disambiguation_option(e.options, food_name)
                            if best_option:
                                try:
                                    page = wikipedia.page(best_option)
                                    calories_info = self._extract_calories_from_content(page.content, food_name)
                                    if calories_info:
                                        return {
                                            'name': food_name,
                                            'calories': calories_info['calories'],
                                            'portion': calories_info['portion'],
                                            'original_data': calories_info['original_data'],
                                            'source': page.url,
                                            'summary': page.summary[:200] + "..."
                                        }
                                except:
                                    continue
                        except Exception as e:
                            print(f"   页面访问错误: {e}")
                            continue
                    
                except Exception as e:
                    print(f"   搜索错误 '{search_term}': {e}")
                    continue
            
            return None
            
        except Exception as e:
            print(f"获取 {food_name} 信息时出错: {e}")
            return None
    
    def _get_optimized_search_terms(self, food_name: str) -> List[str]:
        """基于真实页面分析获取优化的搜索词"""
        # 如果有特定的搜索策略，使用它
        if food_name in self.search_strategies:
            return self.search_strategies[food_name]
        
        # 通用搜索策略
        return [
            f"{food_name} 营养成分",
            f"{food_name} 营养价值", 
            f"{food_name} 热量",
            f"{food_name} 卡路里",
            f"{food_name}",
            f"{food_name} 食品营养",
            f"{food_name} 营养信息"
        ]
    
    def get_food_data_batch(self, food_list: List[str]) -> List[Dict]:
        """批量获取食物数据"""
        results = []
        for food in food_list:
            print(f"正在处理: {food}")
            data = self.get_food_calories(food)
            if data:
                results.append(data)
                print(f"✅ {food}: {data['calories']}卡/{data['portion']}")
            else:
                print(f"❌ {food}: 未找到数据")
        return results

    def _is_irrelevant_page(self, page_title: str, food_name: str) -> bool:
        """判断页面是否与食物不相关"""
        irrelevant_keywords = [
            '公司', '集团', '企业', '品牌', '商标', '历史', '文化', 
            '节日', '传说', '故事', '电影', '小说', '歌曲', '游戏',
            '地名', '人名', '化学', '医学', '药物', '疾病'
        ]
        
        for keyword in irrelevant_keywords:
            if keyword in page_title:
                return True
        
        # 如果页面标题与食物名称相关性很低，也认为是不相关的
        if food_name not in page_title and not any(char in page_title for char in food_name):
            return True
            
        return False
    
    def _find_best_disambiguation_option(self, options: List[str], food_name: str) -> Optional[str]:
        """从歧义选项中找到最佳匹配"""
        food_keywords = ['食品', '食物', '菜', '饮料', '饮品', '小吃', '点心', '料理']
        
        for option in options:
            # 优先选择包含食物关键词的选项
            if any(keyword in option for keyword in food_keywords):
                return option
            # 或者选择与食物名称最相似的选项
            if food_name in option:
                return option
        
        # 如果没有明显的食物相关选项，返回第一个
        return options[0] if options else None
    
    def _extract_calories_from_content(self, content: str, food_name: str) -> Optional[Dict]:
        """从页面内容中提取热量信息并进行份量换算 - 基于真实页面分析优化"""
        
        # 基于真实页面分析的优化模式
        calorie_patterns = [
            # 基于牛奶页面的成功模式："一杯500毫升的纯牛乳，热量在300大卡左右"
            (r'一[杯瓶罐份块个]\s*(\d+)\s*[毫升克ml g]*[^，。]*?热量[在约为]*\s*(\d+)\s*[千大]*卡', 'specific_portion'),
            (r'(\d+)\s*[毫升克ml g]+[^，。]*?热量[在约为]*\s*(\d+)\s*[千大]*卡', 'specific_portion'),
            
            # 基于巧克力页面的成功模式："100克的牛奶巧克力可以提供540卡路里的能量"
            (r'(\d+)\s*克[^，。]*?提供\s*(\d+)\s*卡路里', '100g_energy'),
            (r'(\d+)\s*克[^，。]*?含有\s*(\d+)\s*[千大]*卡', '100g_energy'),
            (r'(\d+)\s*克[^，。]*?能量\s*(\d+)\s*[千大]*卡', '100g_energy'),
            
            # 专门的热量章节模式
            (r'==\s*热量\s*==[^=]*?(\d+)\s*[千大]*卡', 'calorie_section'),
            (r'热量\s*[:：]\s*(\d+)', 'calorie_label'),
            (r'能量\s*[:：]\s*(\d+)', 'energy_label'),
            
            # 营养成分表格模式
            (r'营养成分[^。]*?热量[^。]*?(\d+)', 'nutrition_table'),
            (r'每100[克毫升gml][^。]*?(\d+)\s*[千大]*卡', '100g'),
            (r'(\d+)\s*[千大]*卡[^。]*?每100[克毫升gml]', '100g'),
            
            # 通用模式（优先级较低）
            (r'热量[约大概为是在]*\s*(\d+)\s*[千大]*卡', 'general'),
            (r'能量[约大概为是在]*\s*(\d+)\s*[千大]*卡', 'general'),
            (r'(\d+)\s*kcal', 'kcal'),
        ]
        
        for pattern, unit_type in calorie_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                try:
                    # 处理不同的匹配结果格式
                    if unit_type in ['specific_portion', '100g_energy']:
                        # 这些模式有两个数字：分量和热量
                        if len(matches[0]) == 2:
                            portion_amount, calories_value = matches[0]
                            portion_amount = int(portion_amount)
                            calories_value = int(calories_value)
                            
                            # 验证数据合理性
                            if self._is_reasonable_specific_calorie_value(
                                calories_value, portion_amount, unit_type, food_name
                            ):
                                # 转换到标准分量
                                converted = self._convert_specific_portion_to_standard(
                                    calories_value, portion_amount, unit_type, food_name
                                )
                                if converted:
                                    return converted
                    else:
                        # 单个数字的模式
                        calories_value = int(matches[0])
                        
                        # 判断数值合理性
                        if self._is_reasonable_calorie_value(calories_value, unit_type, food_name):
                            # 进行份量换算
                            converted_calories = self._convert_to_standard_portion(
                                calories_value, unit_type, food_name
                            )
                            
                            if converted_calories:
                                return converted_calories
                        
                except (ValueError, IndexError):
                    continue
        
        return None
    
    def _is_reasonable_specific_calorie_value(self, calories: int, portion: int, unit_type: str, food_name: str) -> bool:
        """判断特定分量的热量数值是否合理"""
        
        if unit_type == 'specific_portion':
            # 针对"一杯500ml热量300卡"这类模式
            if portion >= 200:  # 大分量（如500ml）
                if '牛奶' in food_name and 200 <= calories <= 400:
                    return True
                elif '可乐' in food_name and 100 <= calories <= 250:
                    return True
                elif 50 <= calories <= 800:  # 一般大分量食物的合理范围
                    return True
            elif portion >= 50:  # 中等分量（如100g）
                if 20 <= calories <= 600:
                    return True
        
        elif unit_type == '100g_energy':
            # 针对"100克含540卡"这类模式
            if portion == 100 and 20 <= calories <= 800:
                return True
        
        return False
    
    def _convert_specific_portion_to_standard(self, calories: int, portion_amount: int, unit_type: str, food_name: str) -> Optional[Dict]:
        """将特定分量的热量转换为标准分量"""
        
        # 获取标准分量
        standard_portion = self._get_standard_portion(food_name)
        
        if unit_type == 'specific_portion':
            # 计算每单位热量，然后转换到标准分量
            calories_per_unit = calories / portion_amount
            converted_calories = calories_per_unit * standard_portion['amount']
            original_info = f"{calories}卡/{portion_amount}{'ml' if '牛奶' in food_name or '可乐' in food_name else 'g'}"
            
        elif unit_type == '100g_energy':
            # 每100g的热量，直接按比例换算
            converted_calories = (calories * standard_portion['amount']) / 100
            original_info = f"{calories}卡/100g"
        
        else:
            return None
        
        return {
            'calories': int(round(converted_calories)),
            'portion': f"{standard_portion['amount']}{standard_portion['unit']}",
            'original_data': original_info
        }
    
    def _is_reasonable_calorie_value(self, calories: int, unit_type: str, food_name: str) -> bool:
        """判断热量数值是否合理"""
        
        # 过滤掉明显过小的数值（如阿斯巴甜的4卡/克）
        if unit_type == 'per_gram' and calories < 2:
            return False
        
        # 过滤掉明显过大的数值
        if calories > 10000:
            return False
        
        # 根据单位类型和食物类型判断合理性
        if unit_type == '100g':
            if '饮料' in food_name or '可乐' in food_name or '果汁' in food_name or '牛奶' in food_name:
                # 饮料类：每100ml通常在20-80卡之间
                return 10 <= calories <= 200
            elif '肉' in food_name or '排骨' in food_name or '鸡腿' in food_name or '鸡肉' in food_name:
                # 肉类：每100g通常在100-400卡之间
                return 80 <= calories <= 600
            elif '薯片' in food_name or '饼干' in food_name:
                # 零食类：每100g通常在400-600卡之间
                return 300 <= calories <= 800
            elif '水果' in food_name or '苹果' in food_name:
                # 水果类：每100g通常在30-100卡之间
                return 20 <= calories <= 150
        
        elif unit_type in ['calorie_section', 'calorie_label', 'energy_label']:
            # 专门热量章节的数值通常比较准确
            return 10 <= calories <= 2000
        
        elif unit_type == 'nutrition_table':
            # 营养表格的数据
            return 10 <= calories <= 1000
        
        elif unit_type == 'general':
            # 通用模式，范围稍宽
            return 5 <= calories <= 3000
        
        elif unit_type == 'kcal':
            # kcal格式，通常是准确数据
            return 10 <= calories <= 2000
        
        # 其他情况的基本范围检查
        return 5 <= calories <= 5000
    
    def _convert_to_standard_portion(self, calories: int, unit_type: str, food_name: str) -> Optional[Dict]:
        """将热量转换为标准分量"""
        
        # 获取标准分量
        standard_portion = self._get_standard_portion(food_name)
        
        # 根据单位类型进行换算
        if unit_type == '100g':
            # 每100克/毫升的热量
            converted_calories = (calories * standard_portion['amount']) / 100
            original_info = f"{calories}卡/100{standard_portion['unit']}"
            
        elif unit_type in ['calorie_section', 'calorie_label', 'energy_label']:
            # 专门热量章节，可能是每100g或总量，需要根据上下文判断
            # 暂时假设是每100g的数据
            converted_calories = (calories * standard_portion['amount']) / 100
            original_info = f"{calories}卡(热量章节)"
            
        elif unit_type == 'nutrition_table':
            # 营养表格，通常是每100g
            converted_calories = (calories * standard_portion['amount']) / 100
            original_info = f"{calories}卡(营养表格)"
            
        elif unit_type == 'general':
            # 通用模式，可能需要根据数值大小判断
            if calories > 200:
                # 可能是每100g的数据
                converted_calories = (calories * standard_portion['amount']) / 100
                original_info = f"{calories}卡(推测100{standard_portion['unit']})"
            else:
                # 可能是总量或每份数据
                converted_calories = calories
                original_info = f"{calories}卡(总量)"
                
        elif unit_type == 'kcal':
            # kcal格式，通常是每100g
            converted_calories = (calories * standard_portion['amount']) / 100
            original_info = f"{calories}kcal/100g"
            
        else:
            # 默认按每100g处理
            converted_calories = (calories * standard_portion['amount']) / 100
            original_info = f"{calories}卡/100{standard_portion['unit']}"
        
        return {
            'calories': int(round(converted_calories)),
            'portion': f"{standard_portion['amount']}{standard_portion['unit']}",
            'original_data': original_info
        }
    
    def _get_standard_portion(self, food_name: str) -> Dict[str, any]:
        """获取食物的标准分量"""
        
        # 精确匹配
        if food_name in self.standard_portions:
            return self.standard_portions[food_name]
        
        # 模糊匹配
        for key in self.standard_portions:
            if key in food_name or food_name in key:
                return self.standard_portions[key]
        
        # 根据食物类型推断标准分量
        if any(drink in food_name for drink in ['可乐', '汽水', '饮料', '果汁']):
            return {'amount': 330, 'unit': 'ml'}
        elif any(meat in food_name for meat in ['肉', '鸡', '牛', '猪', '鱼']):
            return {'amount': 100, 'unit': 'g'}
        elif any(snack in food_name for snack in ['薯片', '饼干', '巧克力']):
            return {'amount': 50, 'unit': 'g'}
        elif any(staple in food_name for staple in ['面', '饭', '粥']):
            return {'amount': 150, 'unit': 'g'}
        else:
            return {'amount': 100, 'unit': 'g'}  # 默认分量
    
    def _is_food_related_page(self, content: str, food_name: str) -> bool:
        """检查页面内容是否与食物相关"""
        food_keywords = [
            '营养', '热量', '卡路里', '蛋白质', '脂肪', '碳水化合物',
            '维生素', '矿物质', '食用', '食品', '饮食', '烹饪',
            '每100克', '每100毫升', '能量', '膳食', '营养成分',
            '食谱', '制作', '原料', '配料', '口感', '味道'
        ]
        
        # 检查内容中是否包含食物相关关键词
        content_lower = content.lower()
        food_keyword_count = sum(1 for keyword in food_keywords if keyword in content_lower)
        
        # 如果包含多个食物关键词，认为是相关的
        if food_keyword_count >= 2:
            return True
        
        # 检查是否包含食物名称
        if food_name.lower() in content_lower:
            return True
        
        return False

def load_crawled_data():
    """加载爬取的食物数据并转换格式"""
    try:
        with open('crawled_foods.json', 'r', encoding='utf-8') as f:
            crawled_data = json.load(f)
        
        converted_foods = []
        for i, food in enumerate(crawled_data, 1):
            # 智能分类和emoji分配
            category, emoji, portion = categorize_food(food['name'])
            
            converted_food = {
                'id': str(i),
                'name': food['name'],
                'category': category,
                'calories': food['calories'],
                'calorie_level': food['calorie_level'],
                'portion': portion,
                'emoji': emoji,
                'description': food['summary'][:100] + "..." if len(food['summary']) > 100 else food['summary']
            }
            converted_foods.append(converted_food)
        
        return converted_foods
    except FileNotFoundError:
        print("未找到爬取的数据文件，使用空数据")
        return []

def categorize_food(food_name):
    """根据食物名称智能分类并分配emoji和份量"""
    
    # 饮料类
    if any(drink in food_name for drink in ['可乐', '奶茶', '咖啡', '果汁', '牛奶', '酸奶', '豆浆', '烧仙草']):
        return 'drinks', '🥤', '250ml'
    
    # 零食类
    if any(snack in food_name for snack in ['薯片', '饼干', '爆米花', '坚果', '炸春卷', '油条', '甜甜圈']):
        return 'snacks', '🍿', '100g'
    
    # 肉类
    if any(meat in food_name for meat in ['鸡腿', '牛排', '排骨', '猪蹄', '鳗鱼', '牛肉', '虾仁', '香肠', '热狗']):
        return 'meat', '🍖', '1份'
    
    # 甜品类
    if any(dessert in food_name for dessert in ['蛋糕', '巧克力', '甜甜圈', '布丁']):
        return 'desserts', '🍰', '1块'
    
    # 水果蔬菜类
    if any(fruit in food_name for fruit in ['苹果', '香蕉', '西瓜', '菠菜', '苦瓜', '茄子', '玉米', '土豆']):
        return 'fruits', '🥬', '1份'
    
    # 主食类
    if any(staple in food_name for staple in ['面', '饭', '汉堡', '三明治', '咖喱', '沙拉', '热干面', '担担面', '拌面']):
        return 'staples', '🍚', '1份'
    
    # 默认分类
    return 'other', '🍽️', '1份'

def calculate_calorie_level(calories: int) -> int:
    """根据热量值计算等级（1-5星）"""
    if calories <= 100:
        return 1
    elif calories <= 200:
        return 2
    elif calories <= 300:
        return 3
    elif calories <= 450:
        return 4
    else:
        return 5

def get_food_emoji(category: str) -> str:
    """根据分类获取emoji"""
    emoji_map = {
        'drinks': '🥤',
        'snacks': '🍿',
        'meat': '🍖',
        'fruits': '🥬',
        'desserts': '🍰',
        'staples': '🍚',
        'other': '🍽️'
    }
    return emoji_map.get(category, '🍽️')

# 获取默认食物数据（现在来自爬取结果）
def get_default_foods():
    """获取默认食物数据（现在来自爬取结果）"""
    return load_crawled_data()

if __name__ == "__main__":
    # 测试爬虫
    scraper = WikipediaFoodScraper()
    
    test_foods = ['可乐', '薯片', '苹果']
    for food in test_foods:
        result = scraper.get_food_calories(food)
        print(f"{food}: {result}")