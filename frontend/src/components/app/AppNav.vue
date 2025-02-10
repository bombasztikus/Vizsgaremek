<script setup lang="ts">
import { useSession } from '@/composables/useSession';
import { useRouter } from 'vue-router';

const { clearSession, isAuthenticated } = useSession();
const router = useRouter();

const signOut = () => {
    clearSession();
    router.push({ name: 'home' });
}
</script>

<template>
    <nav class="navbar navbar-expand-lg bg-black">
        <div class="container-lg">
            <RouterLink :to="{ name: 'home' }" class="navbar-brand" href="#">
                <img src="/logo.png" width="40" height="40" class="img-fluid" />
            </RouterLink>
            <button class="navbar-toggler border-white ms-auto" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
                <i class="bi bi-list text-white p-2 fs-3"></i>
            </button>
            <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
            <div class="navbar-nav gap-3 ms-auto fw-semibold">
                <RouterLink :to="{ name: 'home' }" class="nav-link text-white">Főoldal</RouterLink>
                <button @click="signOut" class="btn btn-outline-light rounded-pill fw-bold text-uppercase" v-if="isAuthenticated">KIJELENTKEZÉS</button>
                <RouterLink :to="{ name: 'register' }" class="btn btn-light rounded-pill fw-bold text-uppercase" v-else>REGISZTRÁCIÓ</RouterLink>
            </div>
            </div>
        </div>
    </nav>
</template>
