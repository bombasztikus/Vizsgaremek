<script setup lang="ts">
import type { Meal } from '@/lib/models';
import MealCard from './MealCard.vue';
import MealCardSkeletonized from './MealCardSkeletonized.vue';

withDefaults(defineProps<{
    title?: string;
    meals?: Meal[];
    isLoading: boolean;
}>(), {
    title: undefined,
});
</script>

<template>
    <section class="mb-5 pt-3">
        <header class="mb-4" v-if="title">
            <h2 class="display-4 fw-bold">{{ title }}</h2>
        </header>
        <div class="row g-3 row-cols-sm-2 row-cols-md-3 row-cols-lg-4">
            <template v-if="isLoading">
                <div class="col" v-for="i in 8" :key="i">
                    <MealCardSkeletonized />
                </div>
            </template>
            <template v-else>
                <div class="col" v-for="meal in meals" :key="meal.id">
                    <MealCard :meal="meal" />
                </div>
            </template>
        </div>
    </section>
</template>
