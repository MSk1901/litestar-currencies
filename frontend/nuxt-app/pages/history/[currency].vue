<script setup>
const route = useRoute()
</script>

<template>
  <div>
    <h1>Rate: {{ route.params.currency }}</h1>
  </div>
</template>