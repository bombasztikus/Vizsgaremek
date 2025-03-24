<script setup lang="ts">
import CartItem from '@/components/store/CartItem.vue';
import { useMeals } from '@/composables/useMeals';
import { useCartStore } from '@/stores/cart';
import { useTitle } from '@vueuse/core';
import { computed } from 'vue';
import { storeToRefs } from 'pinia';
import CartSummary from '@/components/store/CartSummary.vue';

useTitle("Kosár");

const { items } = storeToRefs(useCartStore());
const ids = computed(() => items.value.map((i) => i.productId));
const mealsRef = useMeals(ids.value);

const getMealById = (id: number) => mealsRef.value.find((m) => m.id === id);
</script>

<template>
    <main class="container-lg">
        <Suspense>
            <CartSummary :item-count="items.length">
                <section class="d-flex flex-column gap-3" v-if="items.length > 0">
                    <template v-for="item in items" :key="item.productId">
                        <CartItem :meal="getMealById(item.productId)!" v-if="getMealById(item.productId)" />
                    </template>
                </section>
            </CartSummary>
        </Suspense>
    </main>
</template>
