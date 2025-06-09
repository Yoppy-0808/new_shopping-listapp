// src/api.js
import axios from 'axios'

const apiClient = axios.create({
  baseURL: 'http://localhost:5000', // FlaskのサーバーURL
  headers: {
    'Content-Type': 'application/json'
  }
})

export default {
  getItems: () => apiClient.get('/items'),
  addItem: (item) => apiClient.post('/items', item),
  deleteItem: (id) => apiClient.delete(`/items/${id}`),
  // 他の関数はあとで追加
}
