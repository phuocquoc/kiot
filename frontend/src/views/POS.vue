<template>
  <div class="p-6">
    <h1 class="text-3xl font-bold mb-6">Bán Hàng (POS)</h1>

    <el-form label-position="top" class="mb-6">
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

      <el-form-item label="Chọn khách hàng (Tùy chọn)">
        <el-select
          v-model="selectedCustomerId"
          filterable
          placeholder="Tìm khách hàng..."
          style="width: 100%;"
        >
          <el-option
            v-for="c in customers"
            :key="c.id"
            :label="`${c.name} (${c.phone})`"
            :value="c.id"
          />
        </el-select>
      </el-form-item>
    </el-form>

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
import axios from 'axios'
import { ElMessage } from 'element-plus'

const products = ref([])
const customers = ref([])
const cart = ref([])

const selectedProduct = ref(null)
const selectedCustomerId = ref(null)

const access = localStorage.getItem('access')
const config = { headers: { Authorization: `Bearer ${access}` } }

const fetchProducts = async () => {
  const res = await axios.get('http://localhost:8000/api/products/', config)
  products.value = res.data
}

const fetchCustomers = async () => {
  const res = await axios.get('http://localhost:8000/api/customers/', config)
  customers.value = res.data
}

onMounted(() => {
  fetchProducts()
  fetchCustomers()
})

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

const totalAmount = computed(() => {
  return cart.value.reduce((sum, p) => sum + p.price * p.quantity, 0)
})

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
    await axios.post('http://localhost:8000/api/invoices/', invoiceData, config)
    ElMessage.success('Thanh toán thành công!')
    cart.value = []
    selectedCustomerId.value = null
  } catch (error) {
    console.error(error)
    ElMessage.error('Thanh toán thất bại!')
  }
}
</script>
