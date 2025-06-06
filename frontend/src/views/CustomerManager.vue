<template>
  <div class="p-8">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold">Quản lý Khách Hàng</h1>
      <el-button type="primary" @click="openAddCustomer">+ Thêm khách hàng</el-button>
    </div>

    <el-dialog v-model="showCustomerForm" :title="editing ? 'Chỉnh sửa khách hàng' : 'Thêm khách hàng mới'">
      <el-form :model="customerForm" label-width="120px">
        <el-form-item label="Tên khách hàng">
          <el-input v-model="customerForm.name" />
        </el-form-item>
        <el-form-item label="Số điện thoại">
          <el-input v-model="customerForm.phone" />
        </el-form-item>
        <el-form-item label="Email">
          <el-input v-model="customerForm.email" />
        </el-form-item>
        <el-form-item label="Địa chỉ">
          <el-input v-model="customerForm.address" type="textarea" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCustomerForm = false">Hủy</el-button>
        <el-button type="primary" @click="submitCustomer">{{ editing ? 'Cập nhật' : 'Lưu' }}</el-button>
      </template>
    </el-dialog>

    <el-table :data="customers" border style="width: 100%">
      <el-table-column prop="name" label="Tên" />
      <el-table-column prop="phone" label="Số điện thoại" />
      <el-table-column prop="email" label="Email" />
      <el-table-column prop="address" label="Địa chỉ" />
      <el-table-column label="Hành động">
        <template #default="scope">
          <el-button size="small" @click="openEditCustomer(scope.row)">Sửa</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axiosInstance from '../axiosInstance';
import { ElMessage } from 'element-plus'

const customers = ref([])
const showCustomerForm = ref(false)
const editing = ref(false)
const editCustomerId = ref(null)

const customerForm = ref({
  name: '',
  phone: '',
  email: '',
  address: ''
})

const access = localStorage.getItem('access')
const config = { headers: { Authorization: `Bearer ${access}` } }

const loadCustomers = async () => {
  const res = await axiosInstance.get(`/customers/`, config)
  customers.value = res.data
}

onMounted(loadCustomers)

const openAddCustomer = () => {
  editing.value = false
  editCustomerId.value = null
  customerForm.value = { name: '', phone: '', email: '', address: '' }
  showCustomerForm.value = true
}

const openEditCustomer = (customer) => {
  editing.value = true
  editCustomerId.value = customer.id
  customerForm.value = { ...customer }
  showCustomerForm.value = true
}

const submitCustomer = async () => {
  try {
    if (editing.value) {
      await axiosInstance.put(`/customers/${editCustomerId.value}/`, customerForm.value, config)
      ElMessage.success('Cập nhật khách hàng thành công!')
    } else {
      await axiosInstance.post(`/customers/`, customerForm.value, config)
      ElMessage.success('Thêm khách hàng thành công!')
    }
    showCustomerForm.value = false
    await loadCustomers()
  } catch (error) {
    console.error('Lỗi lưu khách hàng:', error)
    ElMessage.error('Lưu khách hàng thất bại!')
  }
}
</script>
