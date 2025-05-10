module.exports = {
  devServer: {
    host: '0.0.0.0', // Cho phép truy cập từ mọi máy trong LAN
    allowedHosts: 'all', // Cho phép tất cả các IP kết nối vào
    port: 3000,  // Cổng muốn chạy
    open: true,   // Mở trình duyệt khi chạy
    hot: true,    // Hỗ trợ HMR (Hot Module Replacement)
    client: {
      overlay: true // Hiển thị lỗi trong trình duyệt
    }
  },
  // Các config khác...
}
