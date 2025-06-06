<template>
  <div class="min-h-screen flex items-center justify-center bg-green-100">
    <el-card class="w-96">
      <h1 class="text-2xl font-bold mb-6 text-center">Đăng nhập</h1>
      <el-form @submit.prevent="login" label-position="top">
        <el-form-item label="Tên đăng nhập">
          <el-input v-model="username" placeholder="Nhập username" />
        </el-form-item>
        <el-form-item label="Mật khẩu">
          <el-input v-model="password" type="password" placeholder="Nhập mật khẩu" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="login" class="w-full">Đăng nhập</el-button>
        </el-form-item>
      </el-form>
      <el-alert v-if="error" type="error" :title="error" show-icon class="mt-4" />
    </el-card>
  </div>
</template>

<script setup>

import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axiosInstance from '../axiosInstance';
import { ElMessage } from 'element-plus'

const router = useRouter()
const username = ref('')
const password = ref('')
const error = ref('')

const login = async () => {
  try {
    const response = await axiosInstance.post('/token/', {
      username: username.value,
      password: password.value
    })
    localStorage.setItem('access', response.data.access)
    ElMessage.success('Đăng nhập thành công!')
    router.push('/dashboard')
  } catch (err) {
    error.value = 'Sai tài khoản hoặc mật khẩu!'
    ElMessage.error(error.value)
  }
}
</script>
