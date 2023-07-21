<script setup>
import { useUserStore } from '../stores/user'
import axios from 'axios'
</script>

<template>
  <div class="add">
    <div class="inputs">
        <input placeholder="От" type="number" v-model="start" />
        <input placeholder="До" type="number" v-model="end" />
        <input min=1 placeholder="Кол-во" type="number" v-model="count" />
    </div>
    <button @click="submit">+</button>
    <p v-text="error_message" class="error"></p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      start: '',
      end: '',
      count: '',
      error_message: ''
    }
  },
  methods: {
    submit() {
        const path = "http://localhost:8000/create_record"
        const user = useUserStore()

        axios.post(path, {
          token: user.token, 
          start: Number(this.start) || 0, 
          end: Number(this.end) || 100, 
          count: Number(this.count) || 55
        })
          .then((res) => {
              let answer = res.data
              if (!answer.is_ok) {
                  this.error_message = answer.error
                  return
              }
              user.addRecord(answer.id)
          }).catch((err) => {
              this.error_message = err
          })
    }
  }
}
</script>

<style scoped>
.add {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  row-gap: 1vh;
}
.add input {
  font-size: 2vh;
  padding: 10px;
  background: var(--vt-c-white-mute);
  border: none;
  border-radius: 10px;
  outline: none;
  width: 50%;
}
.add button {
  background: var(--color-primary-active);
  border: none;
  padding: 10px;
  font-size: 2vh;
  border-radius: 10px;
  cursor: pointer;
  transition: 0.2s;
  width: 100%;
}
.add button:hover {
  background: var(--color-primary);
}
.inputs {
    display: flex;
    flex-direction: row;
    column-gap: 5px;
}
.error {
  color: var(--vt-c-red-soft);
}
</style>
