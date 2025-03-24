<script setup lang="ts">
import { useTitle } from '@vueuse/core';

useTitle("Az oldal nem található (404)")
</script>

<template>
    <main class="container d-flex h-100 m-auto justify-content-center justify-items-center text-center text-md-start">
        <div>
            <p class="display-6 mb-5 text-secondary">404</p>
            <h1 class="display-2 fw-bold mb-1 p-0">Az oldal nem található...</h1>
            <p class="fs-5 text-secondary mb-5">Ellenőrizd az oldal címét.</p>
            <RouterLink :to="{ name: 'browse' }" class="btn btn-dark rounded-pill fw-bold px-4 py-2">Nem vagy éhes?</RouterLink>
        </div>
    </main>
</template>
