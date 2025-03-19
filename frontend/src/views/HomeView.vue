<script setup lang="ts">
import DeliveryAdImage from '@/assets/img/delivery_ad.jpg';
import StoreSection from '@/components/store/StoreSection.vue';
import { useMeals } from '@/composables/useMeals';
import WelcomeSection from '@/components/store/WelcomeSection.vue';
import { useTitle } from '@vueuse/core';
import { computed, onBeforeMount, ref } from 'vue';
import { MealType, type APIError, type Meal, type User } from '@/lib/models';
import { useUser } from '@/composables/useUser';

useTitle("Főoldal");

const items = useMeals([], 3);
const meals = computed(() => {
    return {
        [MealType.FOOD]: items.value.filter((item: Meal) => item.type === MealType.FOOD),
        [MealType.BEVERAGE]: items.value.filter((item: Meal) => item.type === MealType.BEVERAGE),
        [MealType.MENU]: items.value.filter((item: Meal) => item.type === MealType.MENU),
        [MealType.DESSERT]: items.value.filter((item: Meal) => item.type === MealType.DESSERT),
    }
});

const user = ref<User>();

onBeforeMount(async () => {
    const o = await useUser();

    if (!o) {
        console.error('Failed to fetch logged in user (user is likely not logged in)');
        return;
    } else if ((o as unknown as APIError).is_error === true) {
        console.error('Failed to fetch user:', (o as unknown as APIError).error);
        return;
    }

    user.value = o.value;
});
</script>

<template>
    <main class="container-lg">
        <Suspense>
            <WelcomeSection />
        </Suspense>
        <StoreSection :meals="meals.MENU" title="Menük" :is-loading="meals.MENU.length === 0" :show-continue-card="true" />
        <StoreSection :meals="meals.FOOD" title="Ételek" :is-loading="meals.FOOD.length === 0" :show-continue-card="true" />
        <section class="row flex-lg-row-reverse align-items-center justify-content-center g-5 bg-black bg-gradient text-white mt-lg-4 my-2 overflow-hidden ad" v-if="!user">
            <div class="col-lg-6 text-lg-start text-center my-auto py-5 px-5">
                <h1 class="display-4 fw-bold lh-1 mb-3 text-glow">Gyors & precíz kiszállítás</h1>
                <p class="lead mb-0 mb-lg-3">Budapesten belül 45, Pest megyén belül pedig 90 perc alatt az asztalodon lehet a rendelésed.</p>
                <p class="lead text-white-50 fs-6 d-lg-inline-block d-none mb-0">Kép: pexels.com</p>
                <RouterLink :to="{ name: 'register' }" class="btn btn-light d-block rounded-pill mt-4 fw-bold btn-cta px-4 py-2 mx-auto mx-lg-0">REGISZTRÁLJ</RouterLink>
            </div>
            <img :src="DeliveryAdImage" class="object-fit-cover col-10 col-sm-8 col-lg-6 d-none d-lg-block p-0 m-0 img-fluid" alt="">
        </section>
        <StoreSection :meals="meals.BEVERAGE" title="Italok" :is-loading="meals.BEVERAGE.length === 0" :show-continue-card="true" />
        <StoreSection :meals="meals.DESSERT" title="Desszertek" :is-loading="meals.DESSERT.length === 0" :show-continue-card="true" />
    </main>
</template>

<style>
  .ad {
    border-radius: 2rem;
  }

  .btn-cta {
    width: fit-content;
    font-size: 1.1rem;
  }

  @media (max-width: 992px) {
    .ad {
      border-radius: 0;
    }
  }
</style>
