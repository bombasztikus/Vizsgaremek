<script setup lang="ts">
import CartItem from '@/components/store/CartItem.vue';
import { useMeals } from '@/composables/useMeals';
import { useCartStore } from '@/stores/cart';
import { useTitle } from '@vueuse/core';
import { computed, ref, watchEffect } from 'vue';
import { storeToRefs } from 'pinia';
import type { Meal } from '@/lib/models';
import CartSummary from '@/components/store/CartSummary.vue';

useTitle("Kosár");

const { items } = storeToRefs(useCartStore());
const ids = computed(() => items.value.map((i) => i.productId));

const meals = ref<Meal[]>([]);
const mealsRef = useMeals(ids.value);
const totalValue = computed(() => meals.value.reduce((a, b) => a + b.price , 0));

watchEffect(() => {
    meals.value = ids.value.length > 0 ? mealsRef.value : [];
});
</script>

<template>
    <main class="container-lg">
        <Suspense>
            <CartSummary :item-count="meals.length" :total-cost="totalValue" :locations="['Helyben fogyasztom', 'Kiszállítást kérek']">
                <section class="d-flex flex-column gap-3" v-if="meals.length > 0">
                    <CartItem v-for="meal in meals" :key="meal.id" :meal="meal" />
                </section>
            </CartSummary>
        </Suspense>
    </main>
</template>
