// src/axiosInstance.js
import axios from 'axios'

const axiosInstance = axios.create({
  baseURL: "http://localhost:8000/api",  // Lấy API_BASE_URL từ .env
  timeout: 5000,
});

export default axiosInstance;
