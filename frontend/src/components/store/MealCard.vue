<script setup lang="ts">
import type { Meal } from '@/lib/models';
import { useCartStore } from '@/stores/cart';
import { computed } from 'vue';

const props = defineProps<{
    meal: Meal;
}>();

const { items: cart } = useCartStore();
const inCartAlready = computed(() => cart.some((i) => i.productId === props.meal.id));

const addToCart = () => {
    const idx = cart.findIndex((i) => i.productId === props.meal.id);

    if (idx === -1) {
        cart.push({
            productId: props.meal.id,
            quantity: 1,
            price: props.meal.price,
        });
    } else {
        if (cart[idx].quantity < 100) {
            cart[idx].quantity++;
        }
    }
};
</script>

<template>
    <article class="card h-100 rounded-4 overflow-hidden" style="min-height: 400;">
        <RouterLink :to="{ name: 'product', params: { id: meal.id } }" class="text-decoration-none text-dark h-100">
            <img :src="meal.has_image_url ? meal.image_url : meal.fallback_image_url" class="card-img-top h-10 p-2" :alt="`${meal.name} illusztrációja`" :class="[$style.grow]">
            <div class="card-body d-flex flex-column pb-0">
                <h5 class="card-title fw-bolder fs-4 text-truncate lh-base">{{ meal.name }}</h5>
                <p class="card-subtitle">
                    <i class="bi bi-star-fill text-warning me-1" v-for="star in meal.stars" :key="star"></i>
                    <i class="bi bi-star text-warning me-1" v-for="star in (5 - meal.stars)" :key="star"></i>
                    <span class="text-body-secondary">({{ meal.stars }})</span>
                </p>
                <p class="card-text text-body-secondary mt-2 meal-description">
                    {{ meal.description ?? "Ennek az ételnek vagy italnak nincs leírása, de biztosan nagyon finom." }}
                </p>
            </div>
        </RouterLink>
        <div class="card-body">
            <button @click="addToCart" class="btn btn-outline-dark fw-bold w-100 mt-auto rounded-pill text-uppercase">
                <template v-if="inCartAlready"><i class="bi bi-cart-check me-1"></i>Kosárban (</template>
                <template v-if="meal.is_free">
                    <i class="bi bi-gift me-1" v-if="!inCartAlready"></i>INGYEN
                </template>
                <template v-else>
                    <i class="bi bi-cart-plus me-1" v-if="!inCartAlready"></i>{{ meal.display_price }}
                </template>
                <template v-if="inCartAlready">)</template>
            </button>
        </div>
    </article>
</template>

<style module>
.grow {
    transition: all .1s;
}

article:hover > .grow {
    transform: scale(1.15) rotate(3deg);
}
</style>
