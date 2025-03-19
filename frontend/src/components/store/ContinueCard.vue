<script setup lang="ts">
import type { RouteLocationRaw } from 'vue-router';

defineProps<{
    to: RouteLocationRaw;
}>();
</script>

<template>
    <RouterLink :to="to" class="d-block text-decoration-none h-100">
        <div class="card h-100 rounded-4 overflow-hidden text-body-secondary" style="min-height: 400;">
            <div class="card-body d-flex flex-column gap-4 justify-content-center align-items-center">
                <i class="bi bi-arrow-right-circle-fill display-1"></i>
                <h5 class="card-title fs-4 lh-base m-0 fw-semibold">Továbbiak</h5>
            </div>
        </div>
    </RouterLink>
</template>

<style module>
.grow {
    transition: all .1s;
}

article:hover > .grow {
    transform: scale(1.15) rotate(3deg);
}
</style>
