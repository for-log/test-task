import { defineStore } from 'pinia'


export const useUserStore = defineStore('user', {
  state: () => ({ 
    token: localStorage.getItem("user-token"), 
    id: localStorage.getItem("user-id"),
    records: []
  }),
  actions: {
    setToken(value) {
      this.token = value
    },
    setId(value) {
      this.id = value
    },
    setRecords(value) {
      this.records = value
    },
    addRecord(record) {
      this.records.push(record)
    },
    dropRecord(index) {
      this.records.splice(index, 1)
    },
    clear() {
      localStorage.removeItem("user-token")
      localStorage.removeItem("user-id")
      this.token = ""
      this.id = null
      this.records = []
    }
  },
})

