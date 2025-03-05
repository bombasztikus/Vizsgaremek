<script setup lang="ts">
import PlaceholderImage from '@/assets/fallback/image.jpg';
</script>

<template>
    <article class="card h-100 rounded-4 overflow-hidden" style="min-height: 400;" aria-hidden="true">
        <div class="placeholder-glow h-10 p-2">
            <img :src="PlaceholderImage" class="placeholder card-img-top" alt="">
        </div>
        <div class="card-body d-flex flex-column">
            <h5 class="card-title fs-4 placeholder-glow">
                <span class="placeholder col-8"></span>
            </h5>
            <p class="card-subtitle placeholder-glow">
                <span class="placeholder col-5"></span>
            </p>
            <p class="card-text mt-2 placeholder-glow">
                <span class="placeholder col-12"></span>
                <span class="placeholder col-12"></span>
                <span class="placeholder col-12"></span>
            </p>
            <div class="placeholder-glow">
                <a class="btn btn-dark w-100 mt-auto rounded-pill disabled placeholder" aria-disabled="true"></a>
            </div>
        </div>
    </article>
</template>
