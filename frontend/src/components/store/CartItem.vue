<script setup lang="ts">
import type { Meal } from '@/lib/models';

defineProps<{
    meal: Meal;
}>();
</script>

<template>
    <article class="card w-full rounded-4 overflow-hidden">
        <div class="row g-2">
            <div class="col-md-8">
                <div class="card-body">
                    <p class="card-title">{{ meal.name }}</p>
                    <p class="card-text">{{ meal.description ?? "Ennek az ételnek vagy italnak nincs leírása, de biztosan nagyon finom." }}</p>
                </div>
            </div>
            <div class="col-md-4">
                <img :src="meal.has_image_url ? meal.image_url : meal.fallback_image_url" class="card-img-top h-10 p-2" :alt="`${meal.name} illusztrációja`">
            </div>
        </div>
    </article>
</template>
