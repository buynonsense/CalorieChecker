// 食物数据处理工具
export interface ProcessedFoodItem {
  id: string;
  name: string;
  displayName: string; // 处理后的显示名称
  category: string;
  calories: number;
  actualCalories: number; // 实际热量（根据重量调整）
  calorie_level: number;
  portion: string;
  actualPortion: string; // 实际分量描述
  emoji: string;
  description: string;
  source?: string;
  summary?: string;
}

// 从名称中提取重量信息
export function extractWeightFromName(name: string): {
  cleanName: string;
  weight: number | null;
} {
  // 匹配模式：食物名（数字g）或食物名（数字ml）
  const weightMatch = name.match(/^(.+?)（(\d+(?:\.\d+)?)(g|ml)）$/);

  if (weightMatch) {
    const cleanName = weightMatch[1].trim();
    const weight = parseFloat(weightMatch[2]);
    return { cleanName, weight };
  }

  return { cleanName: name, weight: null };
}

// 处理食物数据，计算实际热量
export function processFoodData(foodItem: any): ProcessedFoodItem {
  const { cleanName, weight } = extractWeightFromName(foodItem.name);

  let actualCalories = foodItem.calories;
  let actualPortion = foodItem.portion;
  let displayName = foodItem.name;

  // 如果名称中包含重量信息，且分量是100g，则计算实际热量
  if (weight && foodItem.portion === "100g") {
    actualCalories = Math.round(foodItem.calories * (weight / 100));
    actualPortion = `${weight}g`;
    displayName = cleanName;
  }

  return {
    ...foodItem,
    displayName,
    actualCalories,
    actualPortion,
  };
}

// 计算实际的热量等级
export function calculateActualCalorieLevel(actualCalories: number): number {
  if (actualCalories <= 100) return 1;
  if (actualCalories <= 200) return 2;
  if (actualCalories <= 300) return 3;
  if (actualCalories <= 450) return 4;
  return 5;
}
