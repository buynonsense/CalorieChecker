<template>
  <div class="home-view">
    <!-- 页面头部 -->
    <header class="app-header">
      <h1 class="app-title">
        <span class="title-emoji">🍎</span>
        卡路里小助手
        <span class="title-emoji">🥤</span>
      </h1>
      <p class="app-subtitle">真实数据，智能查询</p>
    </header>

    <!-- 搜索栏 -->
    <SearchBar 
      :search-results="foodStore.searchResults"
      @search="handleSearch"
      @clear="handleClearSearch"
    />

    <!-- 分类过滤器 -->
    <CategoryFilter 
      :categories="foodStore.categories"
      :selected-category="foodStore.selectedCategory"
      @update:selected-category="handleCategoryChange"
    />

    <!-- 视图模式切换 -->
    <div class="view-controls">
      <button 
        @click="toggleCompactMode"
        class="view-toggle-btn"
        :class="{ active: isCompactMode }"
      >
        <span>{{ isCompactMode ? '📱' : '🖥️' }}</span>
        {{ isCompactMode ? '紧凑模式' : '详细模式' }}
      </button>
      <div class="results-info">
        显示 {{ foodStore.filteredFoods.length }} 个食物
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="foodStore.loading" class="loading">
      <div class="loading-spinner">🍩</div>
      <p>正在加载美食数据...</p>
    </div>

    <!-- 食物卡片网格 -->
    <div v-else class="food-grid" :class="{ compact: isCompactMode }">
      <TransitionGroup name="food-cards" tag="div" class="grid-container">
        <FoodCard 
          v-for="food in foodStore.filteredFoods"
          :key="food.id"
          :food="food"
          :compact="isCompactMode"
        />
      </TransitionGroup>
    </div>

    <!-- 空状态 -->
    <div v-if="!foodStore.loading && foodStore.filteredFoods.length === 0" class="empty-state">
      <div class="empty-emoji">{{ getEmptyStateEmoji() }}</div>
      <h3>{{ getEmptyStateTitle() }}</h3>
      <p>{{ getEmptyStateMessage() }}</p>
      <button v-if="foodStore.searchResults !== null" @click="handleClearSearch" class="retry-btn">
        🔄 查看全部食物
      </button>
    </div>

    <!-- 页面底部 -->
    <footer class="app-footer">
      <p>数据来源：维基百科 | 共收录 {{ foodStore.foods.length }} 种食物</p>
      <div class="footer-emojis">🌟 🍓 🥕 🍇 🥑</div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { useFoodStore } from '../stores/foodStore'
import FoodCard from '../components/FoodCard.vue'
import CategoryFilter from '../components/CategoryFilter.vue'
import SearchBar from '../components/SearchBar.vue'

const foodStore = useFoodStore()
const isCompactMode = ref(false)

// 检测屏幕大小，自动启用紧凑模式
const checkScreenSize = () => {
  isCompactMode.value = window.innerWidth <= 768
}

onMounted(() => {
  // 初始化食物数据
  foodStore.initializeFoods()
  
  // 检测屏幕大小
  checkScreenSize()
  window.addEventListener('resize', checkScreenSize)
})

const handleSearch = (query: string) => {
  foodStore.searchFoods(query)
}

const handleClearSearch = () => {
  foodStore.clearSearch()
}

const handleCategoryChange = (category: string) => {
  foodStore.selectedCategory = category
  // 如果正在搜索，重新执行搜索以应用新的分类过滤
  if (foodStore.searchQuery) {
    foodStore.searchFoods(foodStore.searchQuery)
  }
}

const toggleCompactMode = () => {
  isCompactMode.value = !isCompactMode.value
}

const getEmptyStateEmoji = () => {
  if (foodStore.searchResults !== null) {
    return '🔍'
  }
  return '🍽️'
}

const getEmptyStateTitle = () => {
  if (foodStore.searchResults !== null) {
    return '没有找到相关食物'
  }
  return '暂无食物数据'
}

const getEmptyStateMessage = () => {
  if (foodStore.searchResults !== null) {
    return '试试搜索其他关键词或更换分类'
  }
  return '正在加载食物数据...'
}
</script>

<style scoped>
.home-view {
  min-height: 100vh;
  padding: 20px;
  background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 50%, #ffeaa7 100%);
}

.app-header {
  text-align: center;
  margin-bottom: 30px;
  padding: 30px 20px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 30px;
  backdrop-filter: blur(10px);
}

.app-title {
  font-size: 3rem;
  color: #fff;
  margin: 0;
  text-shadow: 2px 2px 8px rgba(0,0,0,0.2);
  font-weight: bold;
  animation: bounce 2s ease-in-out infinite;
}

.title-emoji {
  font-size: 2.5rem;
  margin: 0 10px;
  display: inline-block;
  animation: rotate 3s linear infinite;
}

.app-subtitle {
  font-size: 1.2rem;
  color: #fff;
  margin: 10px 0 0 0;
  opacity: 0.9;
  text-shadow: 1px 1px 4px rgba(0,0,0,0.2);
}

.view-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 0 20px;
}

.view-toggle-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: rgba(255, 255, 255, 0.9);
  border: 2px solid transparent;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
  font-weight: 500;
}

.view-toggle-btn:hover {
  background: rgba(255, 255, 255, 1);
  border-color: #FFB6C1;
  transform: translateY(-2px);
}

.view-toggle-btn.active {
  background: #FF6B9D;
  color: white;
  border-color: #FF6B9D;
}

.results-info {
  font-size: 0.9rem;
  color: #fff;
  background: rgba(255, 255, 255, 0.2);
  padding: 8px 16px;
  border-radius: 15px;
  backdrop-filter: blur(5px);
}

.loading {
  text-align: center;
  padding: 60px 20px;
  color: #fff;
}

.loading-spinner {
  font-size: 4rem;
  animation: spin 2s linear infinite;
  margin-bottom: 20px;
}

.food-grid {
  max-width: 1200px;
  margin: 0 auto;
}

.grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  padding: 20px 0;
}

/* 紧凑模式网格布局 */
.food-grid.compact .grid-container {
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 8px;
}

.empty-state {
  text-align: center;
  padding: 80px 20px;
  color: #fff;
}

.empty-emoji {
  font-size: 4rem;
  margin-bottom: 20px;
  opacity: 0.8;
}

.empty-state h3 {
  font-size: 1.5rem;
  margin: 20px 0 10px 0;
  text-shadow: 1px 1px 4px rgba(0,0,0,0.2);
}

.empty-state p {
  font-size: 1rem;
  opacity: 0.9;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
  margin-bottom: 20px;
}

.retry-btn {
  padding: 12px 24px;
  background: rgba(255, 255, 255, 0.9);
  border: 2px solid transparent;
  border-radius: 25px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 1rem;
  font-weight: 500;
  color: #FF6B9D;
}

.retry-btn:hover {
  background: rgba(255, 255, 255, 1);
  border-color: #FFB6C1;
  transform: translateY(-2px);
}

.app-footer {
  text-align: center;
  margin-top: 60px;
  padding: 30px 20px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 25px;
  backdrop-filter: blur(10px);
  color: #fff;
}

.app-footer p {
  margin: 0 0 15px 0;
  opacity: 0.8;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
}

.footer-emojis {
  font-size: 1.5rem;
  animation: wave 3s ease-in-out infinite;
}

/* 动画效果 */
@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-10px);
  }
  60% {
    transform: translateY(-5px);
  }
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

@keyframes wave {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}

/* 卡片过渡动画 */
.food-cards-enter-active,
.food-cards-leave-active {
  transition: all 0.5s ease;
}

.food-cards-enter-from,
.food-cards-leave-to {
  opacity: 0;
  transform: translateY(30px) scale(0.9);
}

.food-cards-move {
  transition: transform 0.5s ease;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .home-view {
    padding: 15px;
  }
  
  .app-title {
    font-size: 2.2rem;
  }
  
  .title-emoji {
    font-size: 2rem;
    margin: 0 5px;
  }
  
  .app-subtitle {
    font-size: 1rem;
  }
  
  .view-controls {
    flex-direction: column;
    gap: 10px;
    padding: 0 10px;
  }
  
  .grid-container {
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: 8px;
  }
  
  .food-grid.compact .grid-container {
    grid-template-columns: repeat(auto-fill, minmax(110px, 1fr));
    gap: 6px;
  }
  
  .loading-spinner {
    font-size: 3rem;
  }
  
  .empty-emoji {
    font-size: 3rem;
  }
}

@media (max-width: 480px) {
  .grid-container {
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    gap: 6px;
  }
  
  .food-grid.compact .grid-container {
    grid-template-columns: repeat(auto-fill, minmax(90px, 1fr));
    gap: 4px;
  }
  
  .app-title {
    font-size: 1.8rem;
  }
  
  .app-header {
    padding: 20px 15px;
  }
  
  .view-controls {
    padding: 0 5px;
  }
}

/* 超小屏幕优化 */
@media (max-width: 360px) {
  .grid-container {
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
    gap: 4px;
  }
  
  .food-grid.compact .grid-container {
    grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
    gap: 3px;
  }
  
  .app-title {
    font-size: 1.6rem;
  }
  
  .app-header {
    padding: 15px 10px;
  }
  
  .view-controls {
    padding: 0 3px;
  }
}
</style>