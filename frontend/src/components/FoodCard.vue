<template>
  <div class="food-card" :class="[`calorie-level-${processedFood.actualCalorieLevel}`, { compact: isCompact }]">
    <!-- 食物emoji和名称 -->
    <div class="food-header">
      <div class="food-emoji">{{ food.emoji }}</div>
      <h3 class="food-name">{{ processedFood.displayName }}</h3>
    </div>

    <!-- 热量信息 -->
    <div class="calorie-info">
      <div class="calorie-number">
        <span class="calories">{{ processedFood.actualCalories }}</span>
        <span class="unit">千卡</span>
      </div>
      <div class="portion">{{ processedFood.actualPortion }}</div>
    </div>

    <!-- 星级评分 -->
    <div class="calorie-rating">
      <div class="stars">
        <span v-for="n in 5" :key="n" class="star" :class="{ active: n <= processedFood.actualCalorieLevel }">
          ⭐
        </span>
      </div>
      <div class="rating-text">{{ getRatingText(processedFood.actualCalorieLevel) }}</div>
    </div>

    <!-- 描述信息 (移动端可折叠) -->
    <div v-if="food.description && !isCompact" class="food-description">
      {{ food.description }}
    </div>

    <!-- 热量等级标签 -->
    <div class="calorie-badge" :class="`badge-level-${processedFood.actualCalorieLevel}`">
      {{ getLevelText(processedFood.actualCalorieLevel) }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { FoodItem } from '../types/food'
import { processFoodData, calculateActualCalorieLevel } from '../utils/foodProcessor'

interface Props {
  food: FoodItem
  compact?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  compact: false
})

const isCompact = computed(() => props.compact)

// 处理食物数据
const processedFood = computed(() => {
  const processed = processFoodData(props.food)
  return {
    ...processed,
    actualCalorieLevel: calculateActualCalorieLevel(processed.actualCalories)
  }
})

const getRatingText = (level: number): string => {
  const texts = {
    1: '很健康 😊',
    2: '比较健康 🙂',
    3: '适量享用 😐',
    4: '要注意啦 😟',
    5: '高热量 😱'
  }
  return texts[level as keyof typeof texts] || '未知'
}

const getLevelText = (level: number): string => {
  const texts = {
    1: '低热量',
    2: '较低热量',
    3: '中等热量',
    4: '高热量',
    5: '超高热量'
  }
  return texts[level as keyof typeof texts] || '未知'
}
</script>

<style scoped>
.food-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 20px;
  margin: 10px;
  box-shadow: 0 8px 32px rgba(255, 182, 193, 0.2);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.3);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.food-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #ff9a9e, #fecfef);
  border-radius: 20px 20px 0 0;
}

.food-card:hover {
  transform: translateY(-5px) scale(1.02);
  box-shadow: 0 15px 45px rgba(255, 182, 193, 0.3);
  border-color: #FFB6C1;
}

/* 紧凑模式样式 */
.food-card.compact {
  padding: 8px;
  margin: 3px;
  border-radius: 12px;
  min-height: auto;
}

.food-card.compact:hover {
  transform: translateY(-1px) scale(1.005);
}

/* 根据热量等级设置不同的边框颜色 */
.calorie-level-1 {
  border-left: 6px solid #4CAF50;
}

.calorie-level-2 {
  border-left: 6px solid #8BC34A;
}

.calorie-level-3 {
  border-left: 6px solid #FFC107;
}

.calorie-level-4 {
  border-left: 6px solid #FF9800;
}

.calorie-level-5 {
  border-left: 6px solid #F44336;
}

.food-header {
  text-align: center;
  margin-bottom: 15px;
}

.compact .food-header {
  margin-bottom: 6px;
}

.food-emoji {
  font-size: 3rem;
  margin-bottom: 10px;
  filter: drop-shadow(2px 2px 4px rgba(0, 0, 0, 0.1));
  animation: bounce 2s ease-in-out infinite;
}

.compact .food-emoji {
  font-size: 1.5rem;
  margin-bottom: 3px;
}

.food-name {
  font-size: 1.4rem;
  font-weight: bold;
  color: #333;
  margin: 0;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
}

.compact .food-name {
  font-size: 0.9rem;
  line-height: 1.1;
}

.calorie-info {
  text-align: center;
  margin-bottom: 15px;
  padding: 15px;
  background: rgba(255, 182, 193, 0.1);
  border-radius: 15px;
}

.compact .calorie-info {
  margin-bottom: 6px;
  padding: 6px;
  border-radius: 8px;
}

.calorie-number {
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: 5px;
  margin-bottom: 5px;
}

.calories {
  font-size: 2.2rem;
  font-weight: bold;
  color: #FF6B9D;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
}

.compact .calories {
  font-size: 1.3rem;
}

.unit {
  font-size: 1rem;
  color: #666;
  font-weight: normal;
}

.compact .unit {
  font-size: 0.7rem;
}

.portion {
  font-size: 0.9rem;
  color: #888;
  background: rgba(255, 255, 255, 0.7);
  padding: 3px 8px;
  border-radius: 10px;
  display: inline-block;
}

.compact .portion {
  font-size: 0.7rem;
  padding: 1px 4px;
  border-radius: 6px;
}

.calorie-rating {
  text-align: center;
  margin-bottom: 15px;
}

.compact .calorie-rating {
  margin-bottom: 6px;
}

.stars {
  display: flex;
  justify-content: center;
  gap: 2px;
  margin-bottom: 5px;
}

.compact .stars {
  gap: 1px;
  margin-bottom: 3px;
}

.star {
  font-size: 1.2rem;
  opacity: 0.3;
  transition: all 0.3s ease;
  transform: scale(0.8);
}

.compact .star {
  font-size: 0.8rem;
}

.star.active {
  opacity: 1;
  transform: scale(1);
  animation: sparkle 1.5s ease-in-out infinite;
}

.compact .star.active {
  transform: scale(0.8);
}

.rating-text {
  font-size: 0.9rem;
  color: #666;
  font-weight: 500;
}

.compact .rating-text {
  font-size: 0.7rem;
  display: none;
  /* 紧凑模式下隐藏评分文字 */
}

.food-description {
  font-size: 0.8rem;
  color: #777;
  line-height: 1.4;
  margin-bottom: 15px;
  padding: 10px;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 10px;
  border-left: 3px solid #FFB6C1;
}

.calorie-badge {
  position: absolute;
  top: 15px;
  right: 15px;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.7rem;
  font-weight: bold;
  color: white;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
}

.compact .calorie-badge {
  top: 6px;
  right: 6px;
  padding: 2px 4px;
  font-size: 0.5rem;
  border-radius: 6px;
}

.badge-level-1 {
  background: linear-gradient(135deg, #4CAF50, #8BC34A);
  color: white;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}

.badge-level-2 {
  background: linear-gradient(135deg, #8BC34A, #CDDC39);
  color: #333;
  text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.5);
}

.badge-level-3 {
  background: linear-gradient(135deg, #FFC107, #FF9800);
  color: #333;
  text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.5);
}

.badge-level-4 {
  background: linear-gradient(135deg, #FF9800, #FF5722);
  color: white;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}

.badge-level-5 {
  background: linear-gradient(135deg, #F44336, #E91E63);
  color: white;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}

/* 动画效果 */
@keyframes bounce {

  0%,
  20%,
  50%,
  80%,
  100% {
    transform: translateY(0);
  }

  40% {
    transform: translateY(-10px);
  }

  60% {
    transform: translateY(-5px);
  }
}

@keyframes sparkle {

  0%,
  100% {
    transform: scale(1) rotate(0deg);
  }

  50% {
    transform: scale(1.2) rotate(180deg);
  }
}

@keyframes sparkle-compact {

  0%,
  100% {
    transform: scale(0.9) rotate(0deg);
  }

  50% {
    transform: scale(1.1) rotate(180deg);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .food-card {
    padding: 15px;
    margin: 8px;
  }

  .food-card.compact {
    padding: 6px;
    margin: 2px;
  }

  .food-emoji {
    font-size: 2.5rem;
  }

  .compact .food-emoji {
    font-size: 1.3rem;
  }

  .food-name {
    font-size: 1.2rem;
  }

  .compact .food-name {
    font-size: 0.8rem;
  }

  .calories {
    font-size: 1.8rem;
  }

  .compact .calories {
    font-size: 1.1rem;
  }

  .star {
    font-size: 1rem;
  }

  .compact .star {
    font-size: 0.7rem;
  }
}

@media (max-width: 480px) {
  .food-card {
    padding: 12px;
    margin: 5px;
  }

  .food-card.compact {
    padding: 4px;
    margin: 1px;
  }

  .food-emoji {
    font-size: 2rem;
  }

  .compact .food-emoji {
    font-size: 1.1rem;
  }

  .food-name {
    font-size: 1.1rem;
  }

  .compact .food-name {
    font-size: 0.7rem;
  }

  .calories {
    font-size: 1.6rem;
  }

  .compact .calories {
    font-size: 1rem;
  }
}
</style>