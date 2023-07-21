<script setup>
import GreetingComponent from '../components/GreetingComponent.vue'
import RecordsComponent from '../components/RecordsComponent.vue'
import CreateRecordComponent from '../components/CreateRecordComponent.vue'
import { useRouter } from "vue-router"
import { useUserStore } from '../stores/user';

const user = useUserStore()
const router = useRouter()
function logout() {
  user.clear()
  router.replace({name: "login"})
}
</script>


<template>
  <div class="column">
    <GreetingComponent />
    <button @click="logout">Logout</button>
  </div>
  <div class="column">
    <RecordsComponent />
    <CreateRecordComponent />
  </div>
</template>

<style scoped>
  .column {
    display: flex;
    flex-direction: column;
    row-gap: 10px;
  }
  .column button {
    background: var(--color-primary-active);
    border: none;
    padding: 10px;
    font-size: 2vh;
    border-radius: 10px;
    cursor: pointer;
    transition: 0.2s;
    width: fit-content;
  }
  .column button:hover {
    background: var(--color-primary);
  }
</style>