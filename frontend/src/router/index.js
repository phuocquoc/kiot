import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import POS from '../views/POS.vue'
import ProductManager from '../views/ProductManager.vue'
import CustomerManager from '../views/CustomerManager.vue'
import InvoiceManager from '../views/InvoiceManager.vue'
import Layout from '../layouts/Layout.vue'

const routes = [
  {
    path: '/',
    name: 'Login',
    component: Login
  },
  {
    path: '/',
    component: Layout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '/dashboard',
        name: 'Dashboard',
        component: Dashboard
      },
      {
        path: '/pos',
        name: 'POS',
        component: POS
      },
      {
        path: '/products',
        name: 'Products',
        component: ProductManager
      },
      {
        path: '/customers',
        name: 'Customers',
        component: CustomerManager
      },
      {
        path: '/invoices',
        name: 'Invoices',
        component: InvoiceManager
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Kiểm tra login
router.beforeEach((to, from, next) => {
  const access = localStorage.getItem('access')
  if (to.meta.requiresAuth && !access) {
    next('/')
  } else if (to.path === '/' && access) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router
