<script setup lang="ts">
import type { Meal } from '@/lib/models';

defineProps<{
    meal: Meal;
}>();
</script>

<template>
    <article class="card h-100 rounded-4 overflow-hidden">
        <img :src="meal.image_url ?? undefined" class="card-img-top h-10 p-2" :alt="`${meal.name} illusztrációja`">
        <div class="card-body d-flex flex-column">
            <h5 class="card-title fw-bolder fs-4 text-truncate lh-base">{{ meal.name }}</h5>
            <p class="card-subtitle">
                <i class="bi bi-star-fill text-warning me-1" v-for="star in meal.stars" :key="star"></i>
                <i class="bi bi-star text-warning me-1" v-for="star in (5 - meal.stars)" :key="star"></i>
                <span class="text-body-secondary">({{ meal.stars }})</span>
            </p>
            <p class="card-text text-body-secondary mt-2 meal-description">
                {{ meal.description ?? "Ennek az ételnek vagy italnak nincs leírása, de biztosan nagyon finom." }}
            </p>
            <a href="#" class="btn btn-outline-dark fw-bold w-100 mt-auto rounded-pill text-uppercase">
                <template v-if="meal.is_free">
                    <i class="bi bi-gift"></i> INGYEN
                </template>
                <template v-else>
                    <i class="bi bi-cart-plus"></i> {{ meal.display_price }}
                </template>
            </a>
        </div>
    </article>
</template>
