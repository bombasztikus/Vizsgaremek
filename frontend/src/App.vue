<script setup lang="ts">
import { RouterView } from 'vue-router';
import AppNav from './components/app/AppNav.vue';
</script>

<template>
    <AppNav />
    <RouterView />
</template>

<style>
body,
html,
#app {
  min-height: 100vh;
}

#app {
    display: flex;
    flex-direction: column;
}

.alert {
    border: none;
    padding: .7rem;
}
</style>
