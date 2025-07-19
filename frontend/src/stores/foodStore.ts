import { defineStore } from "pinia";
import { ref, computed } from "vue";
import type {
  FoodItem,
  FoodCategory,
  SearchParams,
  StatsData,
} from "../types/food";
import axios from "axios";

// 在Docker环境中，API请求通过nginx代理，不需要设置baseURL
// axios.defaults.baseURL = "http://localhost:8000";

export const useFoodStore = defineStore("food", () => {
  const foods = ref<FoodItem[]>([]);
  const categories = ref<FoodCategory[]>([]);
  const selectedCategory = ref<string>("all");
  const loading = ref(false);
  const searchResults = ref<FoodItem[] | null>(null);
  const searchQuery = ref("");
  const stats = ref<StatsData | null>(null);

  const filteredFoods = computed(() => {
    // 如果有搜索结果，优先显示搜索结果
    if (searchResults.value !== null) {
      return searchResults.value;
    }

    // 否则按分类过滤
    if (selectedCategory.value === "all") {
      return foods.value;
    }
    return foods.value.filter(
      (food) => food.category === selectedCategory.value
    );
  });

  // 获取所有食物
  const fetchFoods = async (params?: SearchParams) => {
    loading.value = true;
    try {
      const response = await axios.get("/api/foods", { params });
      foods.value = response.data;
      console.log(`✅ 成功加载了 ${foods.value.length} 个食物数据`);
    } catch (error) {
      console.error("获取食物数据失败:", error);
      foods.value = [];
    } finally {
      loading.value = false;
    }
  };

  // 获取类别列表
  const fetchCategories = async () => {
    try {
      const response = await axios.get("/api/categories");
      categories.value = response.data.categories;
      console.log(`✅ 成功加载了 ${categories.value.length} 个类别`);
    } catch (error) {
      console.error("获取类别数据失败:", error);
      categories.value = [];
    }
  };

  // 获取统计信息
  const fetchStats = async () => {
    try {
      const response = await axios.get("/api/stats");
      stats.value = response.data;
    } catch (error) {
      console.error("获取统计数据失败:", error);
      stats.value = null;
    }
  };

  // 搜索食物
  const searchFoods = async (query: string) => {
    if (!query.trim()) {
      clearSearch();
      return;
    }

    loading.value = true;
    searchQuery.value = query;

    try {
      const params: any = {
        q: query, // 后端期望的参数名是 q
        limit: 50,
      };

      if (selectedCategory.value !== "all") {
        params.category = selectedCategory.value;
      }

      const response = await axios.get("/api/foods/search", { params });
      searchResults.value = response.data;
      console.log(`🔍 搜索 "${query}" 找到了 ${response.data.length} 个结果`);
    } catch (error) {
      console.error("搜索失败:", error);
      searchResults.value = [];
    } finally {
      loading.value = false;
    }
  };

  // 按类别获取食物
  const fetchFoodsByCategory = async (category: string) => {
    loading.value = true;
    try {
      const response = await axios.get(`/api/foods/category/${category}`, {
        params: { limit: 100 },
      });
      foods.value = response.data;
    } catch (error) {
      console.error("获取类别食物失败:", error);
      foods.value = [];
    } finally {
      loading.value = false;
    }
  };

  const clearSearch = () => {
    searchResults.value = null;
    searchQuery.value = "";
  };

  // 初始化所有数据
  const initializeFoods = async () => {
    await Promise.all([
      fetchFoods({ limit: 100 }),
      fetchCategories(),
      fetchStats(),
    ]);
  };

  return {
    foods,
    categories,
    selectedCategory,
    loading,
    searchResults,
    searchQuery,
    filteredFoods,
    stats,
    fetchFoods,
    fetchCategories,
    fetchStats,
    fetchFoodsByCategory,
    searchFoods,
    clearSearch,
    initializeFoods,
  };
});
