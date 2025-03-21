<script setup lang="ts">
import type { Meal } from '@/lib/models';
import MealCard from './MealCard.vue';
import MealCardSkeletonized from './MealCardSkeletonized.vue';
import ContinueCard from './ContinueCard.vue';

withDefaults(defineProps<{
    title?: string;
    meals?: Meal[];
    isLoading: boolean;
    showContinueCard?: boolean;
}>(), {
    title: undefined,
    showContinueCard: false,
});
</script>

<template>
    <section class="mb-5 pt-3">
        <header class="mb-4" v-if="title">
            <h2 class="display-4 fw-bold">{{ title }}</h2>
        </header>
        <div class="row g-3 row-cols-2 row-cols-md-3 row-cols-lg-4">
            <template v-if="isLoading">
                <div class="col" v-for="i in 4" :key="i">
                    <MealCardSkeletonized />
                </div>
            </template>
            <template v-else>
                <div class="col" v-for="meal in meals" :key="meal.id">
                    <MealCard :meal="meal" />
                </div>
                <div class="col" v-if="showContinueCard">
                    <ContinueCard :to="{ name: 'browse', query: { type: meals ? meals[0].type : '' } }" />
                </div>
            </template>
        </div>
    </section>
</template>
