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
        <header class="mb-4 pt-3">
            <h2 class="display-4 fw-bold">Kosár ({{ meals.length }} elem)</h2>
        </header>
        <section class="d-flex flex-column gap-3" v-if="meals.length > 0">
            <CartItem v-for="meal in meals" :key="meal.id" :meal="meal" />
        </section>
        <section class="card" v-else>
            <div class="card-body d-flex flex-column gap-1 justify-content-center align-items-center text-center">
                <p class="fs-4 fw-bold">A kosarad üres. Miért nem adsz hozzá valamit?</p>
                <RouterLink :to="{ name: 'home' }" class="btn btn-dark d-block rounded-pill fw-bold px-4 py-2">Mutasd a kínálatot</RouterLink>
            </div>
        </section>
        <Suspense>
            <CartSummary :item-count="meals.length" :total-cost="totalValue" :locations="['Helyben fogyasztom', 'Kiszállítást kérek']" />
        </Suspense>
    </main>
</template>
