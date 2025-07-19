<template>
  <div class="category-filter">
    <h2 class="filter-title">🍽️ 选择分类</h2>
    <div class="filter-buttons">
      <button 
        class="filter-btn"
        :class="{ active: selectedCategory === 'all' }"
        @click="selectCategory('all')"
      >
        <span class="btn-emoji">🌈</span>
        <span class="btn-text">全部</span>
      </button>
      <button 
        v-for="category in categories"
        :key="category.id"
        class="filter-btn"
        :class="{ active: selectedCategory === category.id }"
        @click="selectCategory(category.id)"
      >
        <span class="btn-emoji">{{ category.emoji }}</span>
        <span class="btn-text">{{ category.name }}</span>
        <span class="btn-count">({{ category.count }})</span>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { FoodCategory } from '../types/food'

interface Props {
  categories: FoodCategory[]
  selectedCategory: string
}

interface Emits {
  (e: 'update:selectedCategory', value: string): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const selectCategory = (categoryId: string) => {
  emit('update:selectedCategory', categoryId)
}
</script>

<style scoped>
.category-filter {
  margin-bottom: 30px;
  text-align: center;
}

.filter-title {
  color: #FF6B9D;
  font-size: 1.8rem;
  margin-bottom: 20px;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
  font-weight: bold;
}

.filter-buttons {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 15px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 25px;
  backdrop-filter: blur(10px);
}

.filter-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 15px 20px;
  border: 3px solid transparent;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.9);
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(255, 182, 193, 0.2);
  min-width: 80px;
}

.filter-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(255, 182, 193, 0.3);
  border-color: #FFB6C1;
}

.filter-btn.active {
  border-color: #FF6B9D;
  background: rgba(255, 255, 255, 0.95);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 107, 157, 0.4);
}

.btn-emoji {
  font-size: 1.5rem;
  margin-bottom: 5px;
  filter: drop-shadow(1px 1px 2px rgba(0,0,0,0.1));
}

.btn-text {
  font-size: 0.9rem;
  font-weight: bold;
  color: #333;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
}

.btn-count {
  font-size: 0.7rem;
  opacity: 0.7;
  margin-left: 4px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .filter-buttons {
    gap: 10px;
    padding: 15px;
  }
  
  .filter-btn {
    padding: 12px 16px;
    min-width: 70px;
  }
  
  .btn-emoji {
    font-size: 1.3rem;
  }
  
  .btn-text {
    font-size: 0.8rem;
  }
  
  .filter-title {
    font-size: 1.5rem;
  }
}
</style>