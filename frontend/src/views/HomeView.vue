<script setup lang="ts">
import HeroImage from '@/assets/img/hero.png';
import StoreSection from '@/components/store/StoreSection.vue';
import { useMeals } from '@/composables/useMeals';

const meals = useMeals();
</script>

<template>
    <main class="container-lg">
        <section class="row flex-lg-row-reverse align-items-center g-5 py-4 px-5 bg-black bg-gradient text-white rounded-5 mt-md-4 mb-2 shadow-lg">
            <div class="col-10 col-sm-8 col-lg-6 mx-auto d-none d-lg-flex">
                <img :src="HeroImage" class="d-block mx-lg-auto img-fluid" alt="" width="500" height="500">
            </div>
            <div class="col-lg-6 text-lg-start text-center">
                <h1 class="display-4 fw-bold lh-1 mb-3 text-glow">Rendelj kényelmesen</h1>
                <p class="lead">Éhes vagy? Megoldjuk! Csupán annyit kell tenned, hogy megrendeled a kedvenc ételed az
                    alábbi katalógusból.</p>
                <p class="lead text-white-50 fs-6">Kép: pngtree.com</p>
            </div>
        </section>
        <StoreSection :meals="meals.MENU" title="Menük" v-if="meals.MENU.length > 0" />
        <StoreSection :meals="meals.FOOD" title="Ételek" v-if="meals.FOOD.length > 0" />
        <StoreSection :meals="meals.BEVERAGE" title="Italok" v-if="meals.BEVERAGE.length > 0" />
        <StoreSection :meals="meals.DESSERT" title="Desszertek" v-if="meals.DESSERT.length > 0" />
    </main>
</template>
