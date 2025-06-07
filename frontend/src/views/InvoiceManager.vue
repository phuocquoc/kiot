<template>
  <div class="p-8">
    <h1 class="text-3xl font-bold mb-6">Quản lý Hóa Đơn</h1>

    <el-table :data="invoices" border style="width: 100%">
      <el-table-column prop="id" label="Mã HĐ" width="80" />
      <el-table-column prop="customer.name" label="Khách hàng" />
      <el-table-column prop="staff.username" label="Nhân viên" />
      <el-table-column label="Tổng tiền (đ)">
        <template #default="scope">
          {{ scope.row.total_amount.toLocaleString() }}
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="Ngày tạo" :formatter="formatDate" />
      <el-table-column label="Hành động" width="160">
        <template #default="scope">
          <el-button size="small" @click="viewDetails(scope.row)">Xem</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- Modal chi tiết hóa đơn -->
    <el-dialog v-model="selectedInvoice" title="Chi tiết Hóa Đơn" width="60%">
      <div v-if="selectedInvoice" ref="invoiceContent" class="bg-white p-4">
        <div class="text-2xl font-bold mb-4">Hóa đơn #{{ selectedInvoice.id }}</div>

        <el-table :data="selectedInvoice.items" border>
          <el-table-column prop="product.name" label="Tên sản phẩm" />
          <el-table-column prop="quantity" label="Số lượng" />
          <el-table-column label="Đơn giá (đ)">
            <template #default="scope">
              {{ scope.row.price_per_item.toLocaleString() }}
            </template>
          </el-table-column>
          <el-table-column label="Thành tiền (đ)">
            <template #default="scope">
              {{ (scope.row.quantity * scope.row.price_per_item).toLocaleString() }}
            </template>
          </el-table-column>
        </el-table>

        <div class="text-right font-bold mt-6">
          Tổng tiền: {{ selectedInvoice.total_amount.toLocaleString() }} đ
        </div>
      </div>

      <template #footer>
        <el-button @click="selectedInvoice = null">Đóng</el-button>
        <el-button type="primary" @click="printInvoice">In hóa đơn</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axiosInstance from '../axiosInstance';
import { ElMessage } from 'element-plus'
import html2pdf from 'html2pdf.js'

const invoices = ref([])
const selectedInvoice = ref(null)
const invoiceContent = ref(null)

const access = localStorage.getItem('access')
const config = { headers: { Authorization: `Bearer ${access}` } }

onMounted(async () => {
  const res = await axiosInstance.get(`/invoices/`, config)
  invoices.value = res.data
})

const formatDate = (row, column, cellValue) => {
  if (!cellValue) return ''
  const date = new Date(cellValue)
  return date.toLocaleDateString('vi-VN')
}

const viewDetails = async (invoice) => {
  try {
    const res = await axiosInstance.get(`/invoices/${invoice.id}/`, config)
    selectedInvoice.value = res.data
  } catch (error) {
    console.error('Lỗi lấy chi tiết hóa đơn:', error)
    ElMessage.error('Không thể lấy chi tiết hóa đơn!')
  }
}

const printInvoice = () => {
  if (invoiceContent.value) {
    html2pdf().from(invoiceContent.value).set({
      margin: 1,
      filename: `invoice_${selectedInvoice.value.id}.pdf`,
      html2canvas: { scale: 2 },
      jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
    }).save()
  }
}
</script>
