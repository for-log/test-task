<script setup>
import { useUserStore } from '../stores/user'

const user = useUserStore()
</script>

<template>
  <div class="greetings">
    <h1 class="green">Hello, User#{{ user.id }}</h1>
  </div>
</template>

<style scoped>
  .greetings {
    width: 30vw;
  }
  .greetings h1 {
    font-size: 10vh;
  }
</style>
