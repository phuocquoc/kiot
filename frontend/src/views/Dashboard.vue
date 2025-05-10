<template>
  <div class="p-6">
    <h1 class="text-3xl font-bold mb-6">Dashboard</h1>
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card class="text-center">
          <h2 class="text-xl font-bold mb-2">Tổng sản phẩm</h2>
          <div class="text-3xl">{{ productCount }}</div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="text-center">
          <h2 class="text-xl font-bold mb-2">Tổng khách hàng</h2>
          <div class="text-3xl">{{ customerCount }}</div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="text-center">
          <h2 class="text-xl font-bold mb-2">Tổng doanh thu</h2>
          <div class="text-3xl">{{ totalRevenue.toLocaleString() }} đ</div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const productCount = ref(0)
const customerCount = ref(0)
const totalRevenue = ref(0)

const access = localStorage.getItem('access')
const config = { headers: { Authorization: `Bearer ${access}` } }

onMounted(async () => {
  const products = await axios.get('http://localhost:8000/api/products/', config)
  productCount.value = products.data.length

  const customers = await axios.get('http://localhost:8000/api/customers/', config)
  customerCount.value = customers.data.length

  const invoices = await axios.get('http://localhost:8000/api/invoices/', config)
  totalRevenue.value = invoices.data.reduce((sum, item) => sum + parseFloat(item.total_amount), 0)
})
</script>
