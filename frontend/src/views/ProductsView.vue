<script setup lang="ts">
import StoreSection from '@/components/store/StoreSection.vue';
import { useMeals } from '@/composables/useMeals';
import { useTitle } from '@vueuse/core';
import { computed } from 'vue';
import { MealType, type Meal } from '@/lib/models';
import { useRouteQuery } from '@vueuse/router';

useTitle("Termékek");

const normalizeMealType = (type: string): MealType | undefined => {
  return Object.values(MealType).find(
    (mealType) => mealType.toUpperCase() === type.toUpperCase()
  );
};

const rawCategory = useRouteQuery<string>("type", MealType.FOOD);
const category = computed<MealType>(() => normalizeMealType(rawCategory.value) ?? MealType.FOOD);

const items = useMeals();
const meals = computed(() => {
    return {
        [MealType.FOOD]: items.value.filter((item: Meal) => item.type === MealType.FOOD),
        [MealType.BEVERAGE]: items.value.filter((item: Meal) => item.type === MealType.BEVERAGE),
        [MealType.MENU]: items.value.filter((item: Meal) => item.type === MealType.MENU),
        [MealType.DESSERT]: items.value.filter((item: Meal) => item.type === MealType.DESSERT),
    }
});
</script>

<template>
    <main class="container-lg">
        <template v-if="category && meals[category].length > 0">
            <StoreSection title="Temékek" :meals="meals[category]" :is-loading="meals[category].length === 0" />
        </template>
    </main>
</template>

