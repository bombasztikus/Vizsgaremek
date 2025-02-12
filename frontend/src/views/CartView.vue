<script setup lang="ts">
import CartItem from '@/components/store/CartItem.vue';
import { useMeals } from '@/composables/useMeals';
import { useCartStore } from '@/stores/cart';
import { useTitle } from '@vueuse/core';

useTitle("Kosár");

const { items, itemCount } = useCartStore();
const meals = useMeals(items.map((i) => i.productId));;
</script>

<template>
    <main class="container-lg">
        <header class="mb-4 pt-3">
            <h2 class="display-4 fw-bold">Kosár ({{ itemCount }} elem)</h2>
        </header>
        <section class="d-flex flex-col g-4">
            <CartItem :meal="meal" v-for="meal in meals" :key="meal.id" />
        </section>
    </main>
</template>
