<script setup lang="ts">
import { useRegistration } from '@/composables/useRegistration';
import type { APIError } from '@/lib/models';
import router from '@/router';
import { computed, ref, watch, watchEffect } from 'vue';
import { RouterLink } from 'vue-router';

const email = ref<string>("");
const password = ref<string>("");
const fullName = ref<string>("");
const error = ref<APIError | null>(null);
const errorClass = computed(() => error.value?.css_class ? `alert-${error.value.css_class}` : "");

const submit = () => {
    const response = useRegistration(email.value, password.value, fullName.value);

    watchEffect(() => {
        if (!response.value) return;

        if ((response.value as APIError).is_error) {
            error.value = response.value as APIError;
        } else {
            error.value = null;
            // router.push({ name: 'login' }); // Uncomment when ready
        }
    });
};
</script>

<template>
    <div class="justify-content-center align-items-center d-flex flex-grow-1" :class="[$style.bg]">
        <div class="card rounded-4 overflow-hidden shadow-lg" style="min-width: 400px;">
                <div class="card-body bg-black bg-gradient border-5 border border-white border-bottom-0 rounded-4 text-white d-flex flex-column justify-content-center align-items-center gap-3">
                    <i class="bi bi-patch-check display-4"></i>
                    <h1 class="display-6" :class="[$style.title]">Regisztráció</h1>
                </div>
                <form class="card-body p-3" @submit.prevent="submit">
                    <div class="alert" :class="[errorClass]" role="alert" v-if="error">
                        {{ error.error }}
                    </div>
                    <div class="mb-3">
                        <label for="fullNameHelp" class="form-label text-uppercase fw-bold">Teljes név</label>
                        <input type="text" class="form-control border-dark rounded-3" id="inputEmail" aria-describedby="fullNameHelp" v-model="fullName" placeholder="Példa Pista">
                        <div id="fullNameHelp" class="form-text">A rendelések beazonosításához szükséges</div>
                    </div>
                    <div class="mb-3">
                        <label for="inputEmail" class="form-label text-uppercase fw-bold">Email cím</label>
                        <input type="email" class="form-control border-dark rounded-3" id="inputEmail" aria-describedby="emailHelp" v-model="email" placeholder="valaki@pelda.hu">
                        <div id="emailHelp" class="form-text">Kérjük, adj meg egy érvényes címet</div>
                    </div>
                    <div class="mb-3">
                        <label for="inputPassword" class="form-label text-uppercase fw-bold">Jelszó</label>
                        <input type="password" class="form-control border-dark rounded-3" id="inputPassword" aria-describedby="passwordHelp" v-model="password" placeholder="Jelszó">
                        <div id="passwordHelp" class="form-text">Legalább 6 karakter hosszú kell legyen</div>
                    </div>
                    <div class="mb-3">
                        <button type="submit" class="btn btn-dark fw-bold w-100 rounded-pill text-uppercase">Regisztrálok</button>
                    </div>
                    <RouterLink class="btn btn-outline-dark fw-bold w-100 rounded-pill text-uppercase" :to="{ name: 'login' }">Bejelentkezek</RouterLink>
                </form>
            </div>
    </div>
</template>

<style module>
.bg {
    background-image: url("/bg/auth.jpg");
    background-repeat: no-repeat;
    background-size: cover;
    background-position: center;
}

@media only screen and (max-width: 768px) {
    .bg {
        background: none;
    }
}

.title {
    font-size: 1.8rem;
}
</style>
