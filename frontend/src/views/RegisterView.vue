<script setup>
import axios from 'axios'
import { useUserStore } from '../stores/user.js'
import { RouterLink } from 'vue-router'
</script>

<template>
  <form class="form">
    <h1>Регистрация</h1>
    <input placeholder="Почта" type="email" v-model="email" required/>
    <input placeholder="Пароль" type="password" v-model="password" required/>
    <button @click="submit">Зарегистрироваться</button>
    <RouterLink to="/login">Есть аккаунт?</RouterLink>
    <p v-text="error_message" class="error"></p>
  </form>
</template>

<script>
const path = "http://localhost:8000/register"
const user = useUserStore()

export default {
    data() {
        return {
            email: "",
            password: "",
            error_message: ""
        };
    },
    methods: {
        async submit(e) {
          e.preventDefault()
          axios.post(path, { email: this.email, password: this.password })
              .then((res) => {
              let answer = res.data
              if (!answer.is_ok) {
                  this.error_message = answer.error
                  return;
              }
              user.setToken(answer.token)
              user.setId(answer.id)
              localStorage.setItem("user-token", answer.token)
              localStorage.setItem("user-id", answer.id)
              this.$router.replace("/")
          })
              .catch((error) => {
              this.error_message = error
          });
        }
    },
    components: { RouterLink }
}
</script>

<style scoped>
.form {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100vh;
  row-gap: 1vh;
}
.form input {
  font-size: 2vh;
  padding: 10px;
  background: var(--vt-c-white-mute);
  border: none;
  border-radius: 10px;
  outline: none;
}
.form button {
  background: var(--color-primary-active);
  border: none;
  padding: 10px;
  font-size: 2vh;
  border-radius: 10px;
  cursor: pointer;
  transition: 0.2s;
}
.form button:hover {
  background: var(--color-primary);
}
.error {
  color: var(--vt-c-red-soft);
}
</style>