<script setup>
import { useUserStore } from '../stores/user'
import axios from 'axios'
import { ref, watch } from 'vue'
import { useRoute, useRouter } from "vue-router"

const getPath = "http://localhost:8000/get_record"
const setPath = "http://localhost:8000/set_record"
const getMetadata = "http://localhost:8000/get_metadata"

const user = useUserStore()

const arr = ref([])
const isEnd = ref(false)
const step = ref(1)
const metadataIsLoad = ref(false)

const arrAverage = ref(0)
const arrMins = ref([])
const arrMaxs = ref([])

const route = useRoute()
const id = route.params.id
const router = useRouter()

function getRecord() {
  axios.post(getPath, {token: user.token, id: Number(id), offset: arr.value.length*step.value, step: step.value})
    .then((res) => {
      const answer = res.data
      if (!answer.is_ok) {
        console.log(answer)
        router.replace({name: 'home'})
      }
      arr.value = arr.value.concat(answer.record)
      isEnd.value = answer.is_end
      if (!metadataIsLoad.value) {
        setMetadata()
        metadataIsLoad.value = true
      }
    }).catch(() => {
      router.replace({name: 'home'})
    })
}

function setRecord(action, index, value) {
  axios.post(setPath, {token: user.token, id: id, index: index, value: value, action: action})
  .then((res) => {
    let answer = res.data
    if (answer.is_ok) {
      if (action == 'set') {
        arr.value[index] = value
      } else if (action == 'del') {
        arr.value.splice(index, 1)
      } else if (action == 'add') {
        arr.value.push(0)
      }
      setMetadata()
    }
  }).catch((err) => {
    console.log(err)
  })
}

function setMetadata() {
  axios.post(getMetadata, {token: user.token, id: id})
    .then((res) => {
      let answer = res.data
      if (answer.is_ok) {
        arrAverage.value = answer.average
        arrMaxs.value = answer.maxs
        arrMins.value = answer.mins
      }
    }).catch((err) => {
      console.log(err)
    })
}

function checkScroll(e) {
  const scrollEnd = e.target.scrollTop + e.target.clientHeight
  const procHeight = scrollEnd / e.target.scrollHeight * 100
  if (!isEnd.value && procHeight > 80) {
    getRecord()
  }
}

getRecord()
watch(step, () => {
  arr.value = []
  getRecord()
})
</script>

<template>
  <div class="wrapper">
    <div class="record" @scroll="checkScroll">
      <div class="field" v-for="(item, index) in arr">
        <input type="number" :value="item" @change="(e) => setRecord('set', index, e.target.value)" />
        <button @click="() => setRecord('del', index, 0)">🗑</button>
      </div>
      <button v-if="isEnd" @click="() => setRecord('add', 0, 0)">+</button>
    </div>
    <div class="control">
      <p>Step: <input min="1" type="number" :value="step" @change="(e) => step = Number(e.target.value)" /></p>
      <p>Average: {{ arrAverage.toFixed(2) }}</p>
      <p>Maximums: {{ arrMaxs }}</p>
      <p>Minimums: {{ arrMins }}</p>
    </div>
  </div>
</template>

<style>
.wrapper {
  display: flex;
  flex-direction: column;
  row-gap: 1vh;
}
.wrapper input {
  border: 1px solid gray;
  background: inherit;
  color: gray;
  transition: 0.3s;
  outline: none;
}
.wrapper input:focus, input:hover {
  color: var(--color-primary);
  border-color: var(--color-primary);
}
.record {
  border: 1px solid var(--color-primary);
  padding: 10px;
  width: 71vw;
  height: 80vh;
  overflow-y: scroll;
  overflow-x: hidden;
  display: grid;
  grid-template-columns: repeat(5, 13vw);
  column-gap: 1vw;
  row-gap: 1vh;
}
.field {
  display: flex;
  flex-direction: row;
}
.field input {
  width: 70%;
  text-align: center;
  font-size: 5vh;
}
button {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 30%;
  background: var(--vt-c-red-soft);
  border: none;
  cursor: pointer;
  transition: 0.3s;
  color: white;
  font-size: 5vh;
}
button:hover {
  background: var(--vt-c-red-active);
}
.record > *:last-child {
  width: 100%;
}
.control {
  display: flex;
  flex-direction: row;
  column-gap: 1vw;
  font-size: 3vh;
}
.control input {
  font-size: 3vh;
}
</style>
