<template>
  <el-container style="min-height: 100vh;">
    <el-aside width="220px" class="bg-green-700 text-white">
      <div class="text-2xl font-bold p-4 text-center border-b border-green-600">
        POS Admin
      </div>
      <el-menu
        :default-active="activeMenu"
        router
        class="bg-green-700 text-white"
        text-color="#ffffff"
        active-text-color="#ffd04b"
        background-color="#2d6a4f"
      >
        <el-menu-item index="/dashboard">
          <span>Dashboard</span>
        </el-menu-item>
        <el-menu-item index="/pos">
          <span>Bán Hàng (POS)</span>
        </el-menu-item>
        <el-menu-item index="/products">
          <span>Sản Phẩm</span>
        </el-menu-item>
        <el-menu-item index="/customers">
          <span>Khách Hàng</span>
        </el-menu-item>
        <el-menu-item index="/invoices">
          <span>Hóa Đơn</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header class="flex items-center justify-between bg-white shadow px-4">
        <div class="text-lg font-bold">Hệ thống quản lý</div>
        <el-button type="danger" size="small" @click="logout">Đăng xuất</el-button>
      </el-header>

      <el-main class="p-6 bg-gray-100">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router'
import { computed } from 'vue'

const route = useRoute()
const router = useRouter()

const activeMenu = computed(() => {
  return route.path
})

const logout = () => {
  localStorage.removeItem('access')
  router.push('/')
}
</script>

<style scoped>
.el-menu-item {
  margin: 5px 10px;
  border-radius: 8px;
}
</style>
