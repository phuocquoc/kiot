const fs = require('fs');
const path = require('path');

// Cấu hình các đường dẫn
const distDir = path.resolve(__dirname, 'dist');
const backendStaticDir = path.resolve(__dirname, '../backend/static/assets');
const backendTemplateDir = path.resolve(__dirname, '../backend/templates');

// Đảm bảo folder static/assets tồn tại
if (!fs.existsSync(backendStaticDir)) {
  fs.mkdirSync(backendStaticDir, { recursive: true });
}

// Xóa toàn bộ assets cũ (nếu có)
fs.rmSync(backendStaticDir, { recursive: true, force: true });
fs.mkdirSync(backendStaticDir, { recursive: true });

// Copy tất cả assets/
const assetsSrc = path.join(distDir, 'assets');
const assetsDest = backendStaticDir;

fs.cpSync(assetsSrc, assetsDest, { recursive: true });
console.log('✅ Đã copy assets/ thành công.');

// Copy và chỉnh sửa index.html
const indexSrcPath = path.join(distDir, 'index.html');
const indexDestPath = path.join(backendTemplateDir, 'index.html');

let indexContent = fs.readFileSync(indexSrcPath, 'utf-8');

// Thêm {% load static %} vào đầu file
indexContent = `{% load static %}\n` + indexContent;

// Replace link tới assets thành Django static
indexContent = indexContent.replace(/(href|src)="\/assets\//g, '$1="{% static \'assets/');

// Replace kết thúc link
indexContent = indexContent.replace(/\.css"/g, `.css' %}"`);
indexContent = indexContent.replace(/\.js"/g, `.js' %}"`);

fs.writeFileSync(indexDestPath, indexContent);
console.log('✅ Đã copy và sửa index.html thành công.');
