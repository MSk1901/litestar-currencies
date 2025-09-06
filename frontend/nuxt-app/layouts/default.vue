<script setup>
const route = useRoute()
const activeIndex = route.path
</script>

<template>
  <div>
    <el-header class="header-fixed">
      <el-menu class="header-menu" :default-active="activeIndex" mode="horizontal" router>
        <el-menu-item index="/">Главная</el-menu-item>
        <el-menu-item index="/history/USD">История</el-menu-item>
      </el-menu>
    </el-header>

    <el-main class="main-scrollable">
      <slot />
    </el-main>

    <el-footer class="footer-fixed">
      currencies pet-project &copy; 2025
    </el-footer>
  </div>
</template>

<style scoped>
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

.main-scrollable {
  padding: 60px 100px;
  min-height: 100vh;
  overflow-y: auto;
  box-sizing: border-box;
  background: #f8f8f8;
}
</style>