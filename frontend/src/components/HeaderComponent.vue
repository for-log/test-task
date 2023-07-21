<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
  <header>
    <RouterLink to="/">Home</RouterLink>
  </header>
</template>

<style scoped>
  header {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    position: fixed;
    top: 0;
    left: 0;
    height: 8vh;
    background: var(--color-background);
    border-bottom: solid 1px var(--color-primary);
  }
  header a {
    font-size: 6vh;
    color: var(--color-primary);
  }
</style>
