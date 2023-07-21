<script setup>
import { useUserStore } from '../stores/user'
import axios from 'axios'
import { RouterLink } from 'vue-router';

const getPath = "http://localhost:8000/get_records"
const dropPath = "http://localhost:8000/drop_record"
const user = useUserStore()

axios.post(getPath, {token: user.token})
  .then((res) => {
      let answer = res.data
      if (!answer.is_ok) {
          console.log(answer.error)
          return
      }
      user.setRecords(answer.records)
  }).catch((err) => {
      console.log(err)
  })

function dropRecord(id, index) {
  axios.post(dropPath, {token: user.token, id: id})
    .then((res) => {
        let answer = res.data
        if (!answer.is_ok) {
            console.log(answer.error)
            return
        }
        user.dropRecord(index)
    }).catch((err) => {
        console.log(err)
    })
}
</script>

<template>
  
  <div class="wrapper">
    <div v-for="(record, index) in user.records">
      <RouterLink :to="'/record/'+record" class="green">{{record}}</RouterLink>
      <button @click="() => dropRecord(record, index)">🗑</button>
    </div>
  </div>
</template>

<style scoped>
  .wrapper {
    display: flex;
    height: 40vh;
    overflow: scroll;
    flex-direction: column;
    border: solid 1px var(--color-primary);
    font-size: 5vh;
    border-radius: 10px;
  }
  .wrapper > * {
    display: flex;
    width: 100%;
    text-align: center;
    align-items: center;
  }
  .wrapper > * a {
    width: 80%;
  }
  .wrapper > * button {
    width: 20%;
    background: var(--vt-c-red-soft);
    border: none;
    cursor: pointer;
    transition: 0.3s;
    color: white;
    height: 99%;
  }
  .wrapper > * button:hover {
    background: var(--vt-c-red-active);
  }
</style>
