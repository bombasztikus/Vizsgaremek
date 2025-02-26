<script setup lang="ts">
import type { APIError, MinifiedOrder, OrdersResponse } from '@/lib/models';
import { useOrders } from '@/composables/useOrders';
import OrderCard from '@/components/store/OrderCard.vue';
import { onBeforeMount, ref } from 'vue';

const orders = ref<MinifiedOrder[]>([]);

onBeforeMount(async () => {
    const o = await useOrders();

    if (!o) {
        console.error('Failed to fetch orders (user is likely not logged in)');
        return;
    } else if ((o as APIError).is_error === true) {
        console.error('Failed to fetch orders:', (o as APIError).error);
        return;
    }

    orders.value = (o as OrdersResponse).items.reverse();
});
</script>

<template>
    <main class="container-lg my-4">
        <h1 class="display-4 fw-bold lh-1 mb-md-3 mb-2  m-0 text-glow">Rendeléseim</h1>
        <hr class="my-4">
        <div class="card rounded-4" v-if="orders.length === 0">
            <div class="card-body d-flex flex-column gap-1 justify-content-center align-items-center text-center">
                <p class="fs-4 fw-bold">Még nem rendeltél. Nem vagy éhes?</p>
                <RouterLink :to="{ name: 'home' }" class="btn btn-dark d-block rounded-pill fw-bold px-4 py-2">Mutasd a kínálatot</RouterLink>
            </div>
        </div>
        <section class="d-flex flex-column gap-3" v-else>
            <template v-for="order in orders" :key="order.id">
                <OrderCard :order="order" />
            </template>
        </section>
    </main>
</template>

<style module>
@media (min-width: 768px) {
    .sidebar {
        top: calc(var(--bs-navbar-height, 3rem) + 2.5rem);
    }
}
</style>
