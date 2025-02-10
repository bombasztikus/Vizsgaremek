import { useSession } from '@/composables/useSession';
import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            component: () => import('../views/HomeView.vue'),
            meta: {
                requiresAuth: false,
                preventAuthedEnter: false,
            }
        },
        {
            path: '/login',
            name: 'login',
            component: () => import('../views/LoginView.vue'),
            meta: {
                requiresAuth: false,
                preventAuthedEnter: true,
            }
        },
        {
            path: '/register',
            name: 'register',
            component: () => import('../views/RegisterView.vue'),
            meta: {
                requiresAuth: false,
                preventAuthedEnter: true,
            }
        }
    ],
});

const { isAuthenticated } = useSession();
router.beforeEach((to, from) => {
    if (isAuthenticated.value && to.meta.preventAuthedEnter && to.name !== 'home') {
        return { name: 'home' };
    }

    if (!isAuthenticated.value && to.meta.requiresAuth && to.name !== 'login') {
        return { name: 'login' };
    }
});

export default router;
