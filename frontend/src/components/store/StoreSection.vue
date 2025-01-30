<script setup lang="ts">
import type { Meal } from '@/lib/models';
import MealCard from './MealCard.vue';

defineProps<{
    title: string;
    meals: Meal[];
}>();
</script>

<template>
    <section class="mb-5">
        <header class="mb-4 pt-3">
            <h2 class="display-4 fw-bold">{{ title }}</h2>
        </header>
        <div class="row g-3 row-cols-sm-2 row-cols-md-3 row-cols-lg-4">
            <div class="col" v-for="meal in meals" :key="meal.id">
                <MealCard :meal="meal" />
            </div>
        </div>
    </section>
</template>
