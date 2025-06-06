<template>
  <div class="p-6">
    <h1 class="text-3xl font-bold mb-6">Bán Hàng (POS)</h1>

    <el-form label-position="top" class="mb-6">
      <!-- Chọn sản phẩm -->
      <el-form-item label="Chọn sản phẩm hoặc quét mã">
        <el-select v-model="selectedProduct" filterable placeholder="Tìm sản phẩm..." @change="addSelectedProduct"
          style="width: 100%;">
          <el-option v-for="p in products" :key="p.id" :label="`${p.name} (${p.sku})`" :value="p.id" />
        </el-select>
      </el-form-item>

      <!-- Chọn khách hàng -->
      <el-form-item label="Chọn khách hàng (Tùy chọn)">
        <el-select v-model="selectedCustomerId" filterable placeholder="Tìm khách hàng..." style="width: 100%;"
          @input="searchCustomer">
          <el-option v-for="c in filteredCustomers" :key="c.id" :label="`${c.name} (${c.phone})`" :value="c.id" />
        </el-select>

        <!-- Nút tạo mới khách hàng khi không tìm thấy kết quả -->
        <el-button v-if="filteredCustomers.length === 0 && customerSearch.length > 0" @click="showCreateDialog = true"
          class="mt-2" type="primary">
          Thêm khách hàng
        </el-button>
      </el-form-item>

      <!-- Popup thêm khách hàng -->
      <el-dialog :visible.sync="showCreateDialog" title="Tạo khách hàng mới">
        <el-form :model="newCustomer" label-width="100px">
          <el-form-item label="Tên khách hàng">
            <el-input v-model="newCustomer.name" placeholder="Nhập tên khách hàng" />
          </el-form-item>
          <el-form-item label="Số điện thoại">
            <el-input v-model="newCustomer.phone" placeholder="Nhập số điện thoại" />
          </el-form-item>
          <el-form-item label="Email">
            <el-input v-model="newCustomer.email" placeholder="Nhập email" />
          </el-form-item>
        </el-form>

        <template #footer>
          <el-button @click="showCreateDialog = false">Hủy</el-button>
          <el-button type="primary" @click="createCustomer">Lưu</el-button>
        </template>
      </el-dialog>
    </el-form>

    <!-- Giỏ hàng -->
    <el-table :data="cart" border>
      <el-table-column prop="name" label="Tên sản phẩm" />
      <el-table-column prop="size" label="Size" />
      <el-table-column label="Số lượng">
        <template #default="scope">
          <el-input-number v-model="scope.row.quantity" :min="1" />
        </template>
      </el-table-column>
      <el-table-column label="Thành tiền (đ)">
        <template #default="scope">
          {{ (scope.row.price * scope.row.quantity).toLocaleString() }}
        </template>
      </el-table-column>
    </el-table>

    <div class="mt-6 text-right font-bold text-xl">
      Tổng cộng: {{ totalAmount.toLocaleString() }} đ
    </div>

    <div class="mt-6 text-center">
      <el-button type="success" @click="checkout">Thanh Toán</el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axiosInstance from '../axiosInstance'
import { ElMessage } from 'element-plus'

const products = ref([])
const customers = ref([])
const filteredCustomers = ref([])  // Lọc khách hàng
const cart = ref([])

const selectedProduct = ref(null)
const selectedCustomerId = ref(null)
const customerSearch = ref('')  // Tìm kiếm khách hàng
const newCustomer = ref({ name: '', phone: '', email: '', address: '' })
const showCreateDialog = ref(false)

const access = localStorage.getItem('access')
const config = { headers: { Authorization: `Bearer ${access}` } }

// Fetch danh sách sản phẩm
const fetchProducts = async () => {
  const res = await axiosInstance.get(`/products/`, config)
  products.value = res.data
}

// Fetch danh sách khách hàng
const fetchCustomers = async () => {
  try {
    const res = await axiosInstance.get(`/customers/`)
    customers.value = res.data
    filteredCustomers.value = res.data // Lọc khách hàng mặc định khi chưa tìm kiếm
  } catch (error) {
    console.error('Lỗi khi lấy danh sách khách hàng:', error)
  }
}

onMounted(() => {
  fetchProducts()
  fetchCustomers()
})

// Hàm tìm kiếm khách hàng từ danh sách đã fetch
const searchCustomer = () => {
  if (customerSearch.value.trim()) {
    // Lọc khách hàng theo tên hoặc số điện thoại
    filteredCustomers.value = customers.value.filter((customer) =>
      customer.name.toLowerCase().includes(customerSearch.value.toLowerCase()) ||
      customer.phone.includes(customerSearch.value)
    )
  } else {
    filteredCustomers.value = customers.value // Nếu không tìm kiếm, hiển thị tất cả
  }
}

// Thêm sản phẩm vào giỏ hàng
const addSelectedProduct = (productId) => {
  const found = products.value.find(p => p.id === productId)
  if (found) {
    const exist = cart.value.find(p => p.id === found.id)
    if (exist) {
      exist.quantity += 1
    } else {
      cart.value.push({ ...found, quantity: 1 })
    }
    selectedProduct.value = null
  }
}

// Tính tổng giá trị giỏ hàng
const totalAmount = computed(() => {
  return cart.value.reduce((sum, p) => sum + p.price * p.quantity, 0)
})

// Hàm tạo khách hàng mới
const createCustomer = async () => {
  try {
    // Gửi yêu cầu tạo khách hàng mới
    const response = await axiosInstance.post('/customers', newCustomer.value)
    
    // Thêm khách hàng mới vào danh sách (nếu cần)
    filteredCustomers.value.push(response.data)

    // Đóng dialog và reset form
    showCreateDialog.value = false
    newCustomer.value = { name: '', phone: '', email: '' }

    // Chọn khách hàng vừa tạo
    selectedCustomerId.value = response.data.id

    // Hiển thị thông báo thành công
    ElMessage.success('Khách hàng đã được tạo thành công')
  } catch (error) {
    console.error('Lỗi khi tạo khách hàng:', error)
    ElMessage.error('Tạo khách hàng thất bại')
  }
}

// Hàm thanh toán
const checkout = async () => {
  if (cart.value.length === 0) {
    ElMessage.error('Chưa có sản phẩm trong giỏ hàng!')
    return
  }

  try {
    const invoiceData = {
      customer: selectedCustomerId.value,
      total_amount: totalAmount.value,
      items: cart.value.map(item => ({
        product: item.id,
        quantity: item.quantity,
        price_per_item: item.price
      }))
    }
    await axiosInstance.post(`/invoices/`, invoiceData, config)
    ElMessage.success('Thanh toán thành công!')
    cart.value = []
    selectedCustomerId.value = null
  } catch (error) {
    console.error(error)
    ElMessage.error('Thanh toán thất bại!')
  }
}
</script>
