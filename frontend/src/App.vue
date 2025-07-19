<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script setup lang="ts">
// 这是根组件，所有页面都会通过router-view显示
</script>

<style>
#app {
  min-height: 100vh;
  background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%);
}

* {
  box-sizing: border-box;
}
</style>