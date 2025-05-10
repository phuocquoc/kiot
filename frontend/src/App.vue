<template>
  <router-view />
</template>

<script setup>
// App.vue bây giờ chỉ cần render đúng <router-view />,
// vì layout (sidebar, header, content) đã tự động handled trong router (Layout.vue)
</script>

<style>
/* Nếu cần CSS global thì thêm vào đây */
body {
  background-color: #f3f4f6; /* Tailwind gray-100 */
}
</style>
