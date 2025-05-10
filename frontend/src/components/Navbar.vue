<template>
    <nav class="bg-green-500 text-white p-4 flex justify-between">
      <div class="font-bold text-xl">
        KiotViet Clone
      </div>
      <div class="flex space-x-4">
        <router-link to="/dashboard" class="hover:underline">Dashboard</router-link>
        <router-link to="/pos" class="hover:underline">POS</router-link>
        <router-link to="/products" class="hover:underline">Sản phẩm</router-link>
        <router-link to="/customers" class="hover:underline">Khách hàng</router-link>
        <router-link to="/invoices" class="hover:underline">Hóa đơn</router-link>
        <button @click="logout" class="hover:underline text-red-300">Đăng xuất</button>
      </div>
    </nav>
  </template>
  
  <script setup>
  import { useRouter } from 'vue-router'
  
  const router = useRouter()
  
  const logout = () => {
    localStorage.removeItem('access')
    router.push('/')
  }
  </script>
  