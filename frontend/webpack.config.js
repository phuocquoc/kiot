const path = require('path')

module.exports = {
  entry: './src/index.js',  // File entry chính của frontend (ví dụ: main.js hoặc index.js)
  output: {
    path: path.resolve(__dirname, '../backend/static/js'),  // Output file cho Django
    filename: 'bundle.js',
  },
  mode: 'production',  // Production mode
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: 'babel-loader',  // Để transpile JS
      },
      {
        test: /\.vue$/,
        loader: 'vue-loader',  // Dùng vue-loader cho Vue components
      },
    ],
  },
  resolve: {
    alias: {
      vue: 'vue/dist/vue.esm-bundler.js',  // Đảm bảo sử dụng version Vue đúng
    },
  },
}
