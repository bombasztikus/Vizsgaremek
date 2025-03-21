<script setup lang="ts">
import MealCardSkeletonized from '@/components/store/MealCardSkeletonized.vue';
import MealCard from '@/components/store/MealCard.vue';
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
        <section class="mb-4">
            <header class="mb-4 d-flex sticky-top card mx-auto rounded-pill border-dark" style="top: 4.8rem;">
                <div class="card-body fs-5 fw-semibold leading-1 p-2 d-flex justify-content-between align-items-center">
                    <h2 class="fw-bold p-0 m-0 lh-sm ps-3">Termékek</h2>
                    <div class="ms-auto text-uppercase">
                        <ul class="navbar-nav d-flex flex-row justify-content-center gap-2">
                            <li class="nav-item p-0 m-0">
                                <RouterLink :to="{ name: 'browse', query: { 'type': MealType.MENU } }" class="nav-link px-3 py-2 rounded-pill" :class="{ 'active': category === MealType.MENU }">
                                    <font-awesome-icon :icon="['fas', 'utensils']" class="me-md-2 fs-6 align-baseline" /><span class="d-none d-md-inline-block">Menük</span>
                                </RouterLink>
                            </li>
                            <li class="nav-item">
                                <RouterLink :to="{ name: 'browse', query: { 'type': MealType.FOOD } }" class="nav-link px-3 py-2 rounded-pill" :class="{ 'active': category === MealType.FOOD }">
                                    <font-awesome-icon :icon="['fas', 'pizza-slice']" class="me-md-2 fs-6 align-baseline" /><span class="d-none d-md-inline-block">Ételek</span>
                                </RouterLink>
                            </li>
                            <li class="nav-item">
                                <RouterLink :to="{ name: 'browse', query: { 'type': MealType.BEVERAGE } }" class="nav-link px-3 py-2 rounded-pill" :class="{ 'active': category === MealType.BEVERAGE }">
                                    <font-awesome-icon :icon="['fas', 'martini-glass-citrus']" class="me-md-2 fs-6 align-baseline" /><span class="d-none d-md-inline-block">Italok</span>
                                </RouterLink>
                            </li>
                            <li class="nav-item">
                                <RouterLink :to="{ name: 'browse', query: { 'type': MealType.DESSERT } }" class="nav-link px-3 py-2 rounded-pill" :class="{ 'active': category === MealType.DESSERT }">
                                    <font-awesome-icon :icon="['fas', 'ice-cream']"  class="me-md-2 fs-6 align-baseline" /><span class="d-none d-md-inline-block">Desszertek</span>
                                </RouterLink>
                            </li>
                        </ul>
                    </div>
                </div>
            </header>
            <div class="row g-3 row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4">
                <template v-if="meals[category].length === 0">
                    <div class="col" v-for="i in 4" :key="i">
                        <MealCardSkeletonized />
                    </div>
                </template>
                <template v-else>
                    <div class="col" v-for="meal in meals[category]" :key="meal.id">
                        <MealCard :meal="meal" />
                    </div>
                </template>
            </div>
        </section>
    </main>
</template>

<style scoped>
.active {
    /* backdrop-filter: brightness(.95); */
    background-color: black;
    color: white !important;
    font-weight: bold;
    transition: .15s all ease-in-out;
}
</style>