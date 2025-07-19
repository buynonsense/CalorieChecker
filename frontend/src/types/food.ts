export interface FoodItem {
  id: string;
  name: string;
  category: string;
  calories: number;
  calorie_level: 1 | 2 | 3 | 4 | 5; // 改为下划线命名以匹配后端
  portion: string; // 例如: "330ml", "70g", "1只"
  emoji: string;
  description: string;
  source?: string;
  summary?: string;
}

export interface FoodCategory {
  id: string;
  name: string;
  emoji: string;
  count: number; // 类别中食物数量
}

export interface SearchParams {
  q?: string; // 修改为匹配后端API
  category?: string;
  limit?: number;
  offset?: number;
}

export interface StatsData {
  total_foods: number;
  calories_stats: {
    average: number;
    max: number;
    min: number;
  };
  calorie_level_distribution: Record<number, number>;
  category_distribution: Record<string, number>;
}
