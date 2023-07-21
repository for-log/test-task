import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import { useUserStore } from '../stores/user'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { requiresAuth: true }    
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/record/:id',
      name: 'record',
      component: () => import('../views/RecordView.vue'),
      meta: { requiresAuth: true }
    }
  ]
})


router.beforeEach((to) => {
  const user = useUserStore()
  if (to.meta.requiresAuth && user.id == null) return '/login'
})

export default router
