<script setup lang="ts">
import CartItem from '@/components/store/CartItem.vue';
import { useMeals } from '@/composables/useMeals';
import { useCartStore } from '@/stores/cart';
import { useTitle } from '@vueuse/core';
import { computed, ref } from 'vue';
import { storeToRefs } from 'pinia';

useTitle("Kosár");

const { items, itemCount } = storeToRefs(useCartStore());
const ids = computed(() => items.value.map((i) => i.productId));
const meals = computed(() => ids.value.length == 0 ? [] : useMeals(ids.value).value);
</script>

<template>
    <main class="container-lg">
        <header class="mb-4 pt-3">
            <h2 class="display-4 fw-bold">Kosár ({{ itemCount }} elem)</h2>
        </header>
        <section class="d-flex flex-column gap-4">
            <CartItem :meal="meal" v-for="meal in meals" :key="meal.id" />
        </section>
    </main>
</template>
