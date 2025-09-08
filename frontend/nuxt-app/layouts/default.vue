<script setup>
const route = useRoute()
const activeIndex = route.fullPath
</script>

<template>
  <div class="layout-container">
    <el-header class="header-fixed">
      <el-menu class="header-menu" :default-active="activeIndex" mode="horizontal" router>
        <el-menu-item index="/">Главная</el-menu-item>
        <el-menu-item index="/history/USD">История</el-menu-item>
      </el-menu>
    </el-header>

    <el-main class="main-content">
      <slot />
    </el-main>

    <el-footer class="footer-fixed">
      currencies pet-project &copy; 2025
    </el-footer>
  </div>
</template>

<style scoped>
.layout-container {
  height: 100vh;
  overflow: hidden;
  position: relative;
}

.header-fixed {
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 10;
  box-sizing: border-box;
  padding: 0;
}

.header-menu {
  padding-left: 100px;
  padding-right: 100px;
}

.footer-fixed {
  position: fixed;
  bottom: 0;
  width: 100vw;
  height: 60px;
  padding-left: 100px;
  padding-right: 100px;
  text-align: left;
  background: #f8f8f8;
  color: #888;
  z-index: 10;
  line-height: 60px;
}

.main-content {
  padding: 60px 100px;
  height: calc(100vh - 120px); /* Высота минус header и footer */
  overflow: hidden;
  box-sizing: border-box;
  background: #f8f8f8;
  margin-top: 60px; /* Высота header */
}
</style>