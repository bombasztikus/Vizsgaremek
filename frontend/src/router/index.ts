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
        },
        {
            path: '/cart',
            name: 'cart',
            component: () => import('../views/CartView.vue'),
            meta: {
                requiresAuth: false,
                preventAuthedEnter: false,
            }
        },
        {
            path: '/orders/:id',
            name: 'order',
            component: () => import('../views/OrderView.vue'),
            meta: {
                requiresAuth: true,
                preventAuthedEnter: false,
            }
        },
        {
            path: '/orders',
            name: 'orders',
            component: () => import('../views/MyOrdersView.vue'),
            meta: {
                requiresAuth: true,
                preventAuthedEnter: false,
            }
        },
        {
            path: '/products',
            name: 'browse',
            component: () => import("../views/ProductsView.vue"),
            meta: {
                requiresAuth: false,
                preventAuthedEnter: false,
            }
        },
        {
            path: '/products/:id',
            name: 'product',
            component: () => import("../views/ProductView.vue"),
            meta: {
                requiresAuth: false,
                preventAuthedEnter: false,
            }
        },
        {
            path: '/404',
            name: 'notFound',
            component: () => import("../views/404View.vue"),
            meta: {
                requiresAuth: false,
                preventAuthedEnter: false,
            }
        },
        {
            path: '/:catchAll(.*)',
            redirect: {
                name: 'notFound'
            }
        },
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
