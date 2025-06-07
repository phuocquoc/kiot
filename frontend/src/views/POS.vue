<template>
  <div class="p-6">
    <h1 class="text-3xl font-bold mb-6">Bán Hàng (POS)</h1>

    <el-form label-position="top" class="mb-6">
      <!-- Chọn sản phẩm -->
      <el-form-item label="Chọn sản phẩm hoặc quét mã">
        <el-select
          v-model="selectedProduct"
          filterable
          placeholder="Tìm sản phẩm..."
          @change="addSelectedProduct"
          style="width: 100%;"
        >
          <el-option
            v-for="p in products"
            :key="p.id"
            :label="`${p.name} (${p.sku})`"
            :value="p.id"
          />
        </el-select>
      </el-form-item>

      <!-- Chọn khách hàng -->
      <el-form-item label="Chọn khách hàng (Tùy chọn)">
        <div style="display: flex; gap: 12px; width: 100%;">
          <el-select
            v-model="selectedCustomerId"
            filterable
            clearable
            remote
            :remote-method="searchCustomer"
            :loading="isSearching"
            placeholder="Tìm khách hàng..."
            style="flex: 1"
            popper-class="custom-customer-dropdown"
          >
            <el-option
              v-for="c in filteredCustomers"
              :key="c.id"
              :label="`${c.name} (${c.phone})`"
              :value="c.id"
            />
          </el-select>

          <el-button
            type="primary"
            @click="showCreateDialog = true"
            style="white-space: nowrap;"
          >
            + Thêm
          </el-button>
        </div>
      </el-form-item>

      <!-- Popup tạo khách hàng -->
      <el-dialog v-model="showCreateDialog" title="Tạo khách hàng mới" width="500px">
        <el-form :model="newCustomer" label-width="130px">
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
          <el-input-number
            v-model="scope.row.quantity"
            :min="1"
            :max="scope.row.stock_quantity"
          />
        </template>
      </el-table-column>

      <el-table-column prop="stock_quantity" label="Tồn kho" />

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
import { ref, computed, onMounted, watch } from 'vue'
import axiosInstance from '../axiosInstance'
import { ElMessage } from 'element-plus'

const products = ref([])
const customers = ref([])
const filteredCustomers = ref([])
const cart = ref([])

const selectedProduct = ref(null)
const selectedCustomerId = ref(null)
const customerSearch = ref('')
const isSearching = ref(false)

const newCustomer = ref({ name: '', phone: '', email: '', address: '' })
const showCreateDialog = ref(false)

const access = localStorage.getItem('access')
const config = { headers: { Authorization: `Bearer ${access}` } }

const fetchProducts = async () => {
  const res = await axiosInstance.get(`/products/`, config)
  products.value = res.data
}

const fetchCustomers = async () => {
  try {
    const res = await axiosInstance.get(`/customers/`, config)
    customers.value = res.data
    filteredCustomers.value = res.data
  } catch (error) {
    console.error('Lỗi khi lấy danh sách khách hàng:', error)
  }
}

onMounted(() => {
  fetchProducts()
  fetchCustomers()
})

const searchCustomer = (query) => {
  customerSearch.value = query

  if (!query) {
    filteredCustomers.value = customers.value
    return
  }

  isSearching.value = true

  filteredCustomers.value = customers.value.filter(customer =>
    customer.name.toLowerCase().includes(query.toLowerCase()) ||
    customer.phone.includes(query)
  )

  isSearching.value = false
}

const addSelectedProduct = (productId) => {
  const found = products.value.find(p => p.id === productId)
  if (found) {
    const exist = cart.value.find(p => p.id === found.id)
    if (exist) {
      exist.quantity += 1
      // Giới hạn tăng không vượt tồn kho
      if (exist.quantity > exist.stock_quantity) {
        exist.quantity = exist.stock_quantity
        ElMessage.warning(`Sản phẩm "${exist.name}" đạt tối đa tồn kho.`)
      }
    } else {
      cart.value.push({ ...found, quantity: 1 })
    }
    selectedProduct.value = null
  }
}

const totalAmount = computed(() =>
  cart.value.reduce((sum, p) => sum + p.price * p.quantity, 0)
)

const createCustomer = async () => {
  try {
    const response = await axiosInstance.post('/customers/', newCustomer.value, config)
    filteredCustomers.value.push(response.data)
    customers.value.push(response.data)

    selectedCustomerId.value = response.data.id
    showCreateDialog.value = false
    newCustomer.value = { name: '', phone: '', email: '', address: '' }

    ElMessage.success('Khách hàng đã được tạo thành công')
  } catch (error) {
    console.error('Lỗi khi tạo khách hàng:', error)
    ElMessage.error('Tạo khách hàng thất bại')
  }
}

// Watch cart để check nếu số lượng vượt tồn kho, điều chỉnh và cảnh báo
watch(cart, (newCart) => {
  newCart.forEach(item => {
    if (item.quantity > item.stock_quantity) {
      item.quantity = item.stock_quantity
      ElMessage.warning(`Sản phẩm "${item.name}" vượt quá tồn kho. Đã điều chỉnh lại.`)
    }
    if(item.quantity < 1) {
      item.quantity = 1
    }
  })
}, { deep: true })

const checkout = async () => {
  if (cart.value.length === 0) {
    ElMessage.error('Chưa có sản phẩm trong giỏ hàng!')
    return
  }

  // Kiểm tra lại tồn kho trước khi gửi thanh toán (phòng trường hợp tồn kho thay đổi)
  for (const item of cart.value) {
    if (item.quantity > item.stock_quantity) {
      ElMessage.error(`Sản phẩm "${item.name}" vượt quá tồn kho, vui lòng điều chỉnh lại.`)
      return
    }
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

<style>
/* Dropdown custom để không che nút thêm */
.custom-customer-dropdown {
  max-height: 250px;
  overflow-y: auto;
  z-index: 1000;
}
</style>
