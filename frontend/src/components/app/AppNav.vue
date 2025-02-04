<script setup lang="ts">
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
                <RouterLink :to="{ name: 'register' }" class="btn btn-light rounded-pill fw-bold text-uppercase">RENDELÉS</RouterLink>
            </div>
            </div>
        </div>
    </nav>
</template>
