<script setup lang="ts">
import HeroImage from '@/assets/img/hero.png';
import { useUser } from '@/composables/useUser';
import { computed } from 'vue';

const user = await useUser();
const greeting = computed(() => user ? `Szia ${user.full_name}!` : "Rendelj kényelmesen");
</script>

<template>
    <section class="row flex-lg-row-reverse align-items-center g-5 py-5 px-5 bg-black bg-gradient text-white mt-lg-4 mb-2 ad">
        <div class="col-10 col-sm-8 col-lg-6 mx-auto d-none d-lg-flex my-auto">
            <img :src="HeroImage" class="d-block mx-lg-auto img-fluid" alt="" width="500" height="500">
        </div>
        <div class="col-lg-6 text-lg-start text-center">
            <h1 class="display-4 fw-bold lh-1 mb-3 text-glow leading-1">{{ greeting }}</h1>
            <p class="lead mb-0 mb-lg-3">Éhes vagy? Megoldjuk! Csupán annyit kell tenned, hogy megrendeled a kedvenc ételed az alábbi katalógusból.</p>
            <p class="lead text-white-50 fs-6 d-lg-inline-block d-none">Kép: pngtree.com</p>
        </div>
    </section>
</template>
