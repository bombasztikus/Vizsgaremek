<script setup lang="ts">
import DeliveryAdImage from '@/assets/img/delivery_ad.jpg';
import StoreSection from '@/components/store/StoreSection.vue';
import { useMeals } from '@/composables/useMeals';
import WelcomeSection from '@/components/store/WelcomeSection.vue';

const meals = useMeals();
</script>

<template>
    <main class="container-lg">
        <Suspense>
            <WelcomeSection />
        </Suspense>
        <StoreSection :meals="meals.MENU" title="Menük" v-if="meals.MENU.length > 0" />
        <StoreSection :meals="meals.FOOD" title="Ételek" v-if="meals.FOOD.length > 0" />
        <section class="row flex-lg-row-reverse align-items-center justify-content-center g-5 bg-black bg-gradient text-white mt-lg-4 my-2 overflow-hidden ad">
            <div class="col-lg-6 text-lg-start text-center my-auto py-5 px-5">
                <h1 class="display-4 fw-bold lh-1 mb-3 text-glow">Gyors & precíz kiszállítás</h1>
                <p class="lead mb-0 mb-lg-3">Budapesten belül 45, Pest megyén belül pedig 90 perc alatt az asztalodon lehet a rendelésed.</p>
                <p class="lead text-white-50 fs-6 d-lg-inline-block d-none mb-0">Kép: pexels.com</p>
                <RouterLink :to="{ name: 'register' }" class="btn btn-light d-block rounded-pill mt-4 fw-bold btn-cta px-4 py-2 mx-auto mx-lg-0">REGISZTRÁLJ</RouterLink>
            </div>
            <img :src="DeliveryAdImage" class="object-fit-cover col-10 col-sm-8 col-lg-6 d-none d-lg-block p-0 m-0 img-fluid" alt="">
        </section>
        <StoreSection :meals="meals.BEVERAGE" title="Italok" v-if="meals.BEVERAGE.length > 0" />
        <StoreSection :meals="meals.DESSERT" title="Desszertek" v-if="meals.DESSERT.length > 0" />
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
