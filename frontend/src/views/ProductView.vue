<script setup lang="ts">
import { useMeals } from '@/composables/useMeals';
import { useRouteParams } from '@vueuse/router';
import { computed, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useCartStore } from '@/stores/cart';

const router = useRouter();

const productId = useRouteParams<number>('id');
const rawMeals = useMeals([productId.value]);
const meal = computed(() => rawMeals.value.find((meal) => meal.id == productId.value));

const image = computed(() => meal.value?.has_image_url ? meal.value.image_url : meal.value?.fallback_image_url);

watch([rawMeals, productId], async () => {
    if (!productId.value || isNaN(productId.value) || productId.value < 0 || rawMeals.value.length === 0) {
        console.warn('Product ID invalid');
        await router.push({ name: 'notFound' });
        return;
    }
});


const { items: cart } = useCartStore();
const inCartAlready = computed(() => cart.some((i) => i.productId === meal.value?.id));

const addToCart = () => {
    if (!meal.value) {
        return;
    }

    const idx = cart.findIndex((i) => i.productId === meal.value?.id);

    if (idx === -1) {
        cart.push({
            productId: meal.value.id,
            quantity: 1,
            price: meal.value.price,
        });
    } else {
        cart[idx].quantity++;
    }
};
</script>

<template>
    <main class="container-lg my-5 py-5">
        <div class="row row-cols-1 row-cols-md-2">
            <div class="col">
                <img :src="image" :alt="meal?.name" class="img-fluid" />
            </div>
            <div class="col">
                <h1 class="display-4 fw-bold mb-1">{{ meal?.name }}</h1>
                <p class="lead fs-4">{{ meal?.calories }} kcal<span class="mx-2 text-secondary">&bullet;</span>{{ meal?.stars }} <i class="bi bi-star-fill text-warning ms-1"></i></p>
                <hr>
                <p class="fs-5 mb-4">{{ meal?.description ?? 'Ehhez a termékhez nem tartozik leírás.' }}</p>
                <button @click="addToCart" class="btn btn-dark fw-bold fs-6 px-4 py-2 mt-auto rounded-pill text-uppercase">
                    <template v-if="inCartAlready"><i class="bi bi-cart-check me-2"></i>Kosárban (</template>
                    <template v-if="meal?.is_free">
                        <i class="bi bi-gift me-2" v-if="!inCartAlready"></i>INGYEN
                    </template>
                    <template v-else>
                        <i class="bi bi-cart-plus me-2" v-if="!inCartAlready"></i>{{ meal?.display_price }}
                    </template>
                    <template v-if="inCartAlready">)</template>
                </button>
            </div>
        </div>
    </main>
</template>
