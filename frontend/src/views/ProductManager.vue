<template>
  <div class="p-8">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold">Quản lý Sản phẩm</h1>
      <el-button type="primary" @click="openAddProduct">+ Thêm sản phẩm</el-button>
    </div>

    <el-dialog v-model="showProductForm" :title="editing ? 'Chỉnh sửa sản phẩm' : 'Thêm sản phẩm mới'">
      <el-form :model="productForm" label-width="120px">
        <el-form-item label="Tên sản phẩm">
          <el-input v-model="productForm.name" />
        </el-form-item>
        <el-form-item label="Mã SKU">
          <el-input v-model="productForm.sku" />
        </el-form-item>
        <el-form-item label="Giá">
          <el-input v-model="productForm.price" type="number" />
        </el-form-item>
        <el-form-item label="Size">
          <el-input v-model="productForm.size" />
        </el-form-item>
        <el-form-item label="Số lượng tồn">
          <el-input v-model="productForm.stock_quantity" type="number" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showProductForm = false">Hủy</el-button>
        <el-button type="primary" @click="submitProduct">{{ editing ? 'Cập nhật' : 'Thêm' }}</el-button>
      </template>
    </el-dialog>

    <!-- Modal In mã vạch -->
    <el-dialog v-model="barcodeProduct" title="In Mã Vạch" width="400px">
      <div class="flex justify-center">
        <svg ref="barcodeSvg"></svg>
      </div>
      <template #footer>
        <el-button @click="barcodeProduct = null">Đóng</el-button>
        <el-button type="primary" @click="printBarcode">In mã vạch</el-button>
      </template>
    </el-dialog>

    <el-table :data="products" border style="width: 100%">
      <el-table-column prop="name" label="Tên sản phẩm" />
      <el-table-column prop="sku" label="Mã SKU" />
      <el-table-column prop="price" label="Giá (đ)" />
      <el-table-column prop="size" label="Size" />
      <el-table-column prop="stock_quantity" label="Tồn kho" />
      <el-table-column label="Hành động">
        <template #default="scope">
          <el-button size="small" @click="openEditProduct(scope.row)">Sửa</el-button>
          <el-button size="small" type="success" @click="openBarcode(scope.row)">Mã vạch</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import JsBarcode from 'jsbarcode'
import html2pdf from 'html2pdf.js'

const products = ref([])
const showProductForm = ref(false)
const editing = ref(false)
const editProductId = ref(null)

const barcodeProduct = ref(null)
const barcodeSvg = ref(null)

const productForm = ref({
  name: '',
  sku: '',
  price: '',
  size: '',
  stock_quantity: ''
})

const access = localStorage.getItem('access')
const config = { headers: { Authorization: `Bearer ${access}` } }

const fetchProducts = async () => {
  const res = await axios.get('http://localhost:8000/api/products/', config)
  products.value = res.data
}

onMounted(fetchProducts)

const openAddProduct = () => {
  editing.value = false
  editProductId.value = null
  productForm.value = { name: '', sku: '', price: '', size: '', stock_quantity: '' }
  showProductForm.value = true
}

const openEditProduct = (product) => {
  editing.value = true
  editProductId.value = product.id
  productForm.value = { ...product }
  showProductForm.value = true
}

const submitProduct = async () => {
  try {
    if (editing.value) {
      await axios.put(`http://localhost:8000/api/products/${editProductId.value}/`, productForm.value, config)
      ElMessage.success('Cập nhật sản phẩm thành công!')
    } else {
      await axios.post('http://localhost:8000/api/products/', productForm.value, config)
      ElMessage.success('Thêm sản phẩm thành công!')
    }
    showProductForm.value = false
    await fetchProducts()
  } catch (error) {
    console.error('Lỗi lưu sản phẩm:', error)
    ElMessage.error('Lưu sản phẩm thất bại!')
  }
}

const openBarcode = async (product) => {
  barcodeProduct.value = product
  await nextTick()
  JsBarcode(barcodeSvg.value, product.sku, { format: 'CODE128', width: 2, height: 100 })
}

const printBarcode = () => {
  html2pdf().from(barcodeSvg.value).set({ margin: 1, filename: `${barcodeProduct.value.sku}.pdf` }).save()
}
</script>
