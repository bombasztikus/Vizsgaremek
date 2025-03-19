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
        <div class="card mt-3 sticky-top shadow-lg mx-auto rounded-pill" style="top: 5rem; width: min-content;">
            <ul class="navbar-nav d-flex flex-row gap-5 justify-content-center fs-5 fw-semibold text-uppercase leading-1 card-body px-3 py-2">
                <li class="nav-item">
                    <RouterLink :to="{ name: 'browse', query: { 'type': MealType.MENU } }" class="nav-link p-0">Menük</RouterLink>
                </li>
                <li class="nav-item">
                    <RouterLink :to="{ name: 'browse', query: { 'type': MealType.FOOD } }" class="nav-link p-0">Ételek</RouterLink>
                </li>
                <li class="nav-item">
                    <RouterLink :to="{ name: 'browse', query: { 'type': MealType.BEVERAGE } }" class="nav-link p-0">Italok</RouterLink>
                </li>
                <li class="nav-item">
                    <RouterLink :to="{ name: 'browse', query: { 'type': MealType.DESSERT } }" class="nav-link p-0">Desszertek</RouterLink>
                </li>
            </ul>
        </div>
        <template v-if="category && meals[category].length > 0">
            <StoreSection title="Temékek" :meals="meals[category]" :is-loading="meals[category].length === 0" />
        </template>
    </main>
</template>

