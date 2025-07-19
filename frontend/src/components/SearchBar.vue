<template>
  <div class="search-container">
    <div class="search-box">
      <div class="search-input-wrapper">
        <span class="search-icon">🔍</span>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="搜索食物..."
          class="search-input"
          @input="handleSearch"
          @keyup.enter="handleSearch"
        />
        <button 
          v-if="searchQuery"
          @click="clearSearch"
          class="clear-btn"
        >
          ✕
        </button>
      </div>
    </div>
    
    <!-- 搜索结果提示 -->
    <div v-if="searchQuery && searchResults !== null" class="search-results-info">
      <span class="results-count">
        {{ searchResults.length }} 个结果
      </span>
      <span class="search-term">
        "{{ searchQuery }}"
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import type { FoodItem } from '../types/food'

interface Props {
  searchResults: FoodItem[] | null
}

interface Emits {
  (e: 'search', query: string): void
  (e: 'clear'): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const searchQuery = ref('')

let searchTimeout: NodeJS.Timeout | null = null

const handleSearch = () => {
  // 防抖处理
  if (searchTimeout) {
    clearTimeout(searchTimeout)
  }
  
  searchTimeout = setTimeout(() => {
    emit('search', searchQuery.value)
  }, 300)
}

const clearSearch = () => {
  searchQuery.value = ''
  emit('clear')
}

// 监听外部清空操作
watch(() => props.searchResults, (newResults) => {
  if (newResults === null && searchQuery.value) {
    // 外部清空了搜索结果，但输入框还有内容时，清空输入框
    searchQuery.value = ''
  }
})
</script>

<style scoped>
.search-container {
  margin-bottom: 20px;
}

.search-box {
  display: flex;
  justify-content: center;
  margin-bottom: 10px;
}

.search-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  width: 100%;
  max-width: 400px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 25px;
  box-shadow: 0 4px 20px rgba(255, 182, 193, 0.2);
  backdrop-filter: blur(10px);
  border: 2px solid transparent;
  transition: all 0.3s ease;
}

.search-input-wrapper:focus-within {
  border-color: #FF6B9D;
  box-shadow: 0 6px 25px rgba(255, 107, 157, 0.3);
  transform: translateY(-2px);
}

.search-icon {
  font-size: 1.2rem;
  padding: 0 15px;
  color: #FF6B9D;
  pointer-events: none;
}

.search-input {
  flex: 1;
  padding: 12px 15px 12px 0;
  border: none;
  background: transparent;
  font-size: 1rem;
  color: #333;
  outline: none;
  border-radius: 25px;
}

.search-input::placeholder {
  color: #999;
  font-style: italic;
}

.clear-btn {
  padding: 8px 15px;
  background: none;
  border: none;
  color: #999;
  cursor: pointer;
  font-size: 1rem;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.clear-btn:hover {
  background: rgba(255, 107, 157, 0.1);
  color: #FF6B9D;
  transform: scale(1.1);
}

.search-results-info {
  text-align: center;
  padding: 8px 16px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 20px;
  backdrop-filter: blur(5px);
  display: inline-block;
  margin: 0 auto;
  box-shadow: 0 2px 10px rgba(255, 182, 193, 0.2);
}

.results-count {
  font-weight: bold;
  color: #FF6B9D;
  margin-right: 8px;
}

.search-term {
  color: #666;
  font-style: italic;
}

/* 移动端优化 */
@media (max-width: 768px) {
  .search-input-wrapper {
    max-width: 100%;
    margin: 0 10px;
  }
  
  .search-input {
    font-size: 16px; /* 防止iOS缩放 */
  }
  
  .search-icon {
    font-size: 1.1rem;
    padding: 0 12px;
  }
  
  .clear-btn {
    padding: 6px 12px;
    font-size: 0.9rem;
  }
}

@media (max-width: 480px) {
  .search-input-wrapper {
    margin: 0 5px;
  }
  
  .search-input {
    padding: 10px 12px 10px 0;
  }
  
  .search-icon {
    padding: 0 10px;
  }
  
  .search-results-info {
    font-size: 0.9rem;
    padding: 6px 12px;
  }
}
</style>