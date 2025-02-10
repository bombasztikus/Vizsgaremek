<script setup lang="ts">
import AppAlert from '@/components/app/AppAlert.vue';
import { useLogin } from '@/composables/useLogin';
import type { APIError } from '@/lib/models';
import { useLocalStorage, useTitle } from '@vueuse/core';
import { onBeforeMount, ref, watch } from 'vue';
import { RouterLink, useRouter } from 'vue-router';

useTitle("Bejelentkezés");

const session = useLocalStorage<string | null>("session", null);
const router = useRouter();

const email = ref<string>("");
const password = ref<string>("");
const error = ref<APIError | null>(null);

const reset = () => {
    email.value = "";
    password.value = "";
    error.value = null;
}

const submit = async () => {
    try {
        const response = await useLogin(email.value, password.value);

        if (response?.is_error) {
            error.value = response;
        } else {
            reset();
            session.value = response.access_token;
        }
    } catch (e) {
        console.error(e);
    }
};

const onSessionPreset = () => {
    if (session.value) {
        console.warn("Already logged in, redirecting...")
        router.push({ name: "home" });
    }
}

watch([session], onSessionPreset);
// onBeforeMount(onSessionPreset);
</script>

<template>
    <div class="justify-content-center align-items-center d-flex flex-grow-1" :class="[$style.bg]">
        <div class="card rounded-4 overflow-hidden shadow-lg border-0" style="min-width: 400px;">
                <div class="card-body bg-black bg-gradient text-white d-flex flex-column justify-content-center align-items-center gap-2">
                    <i class="bi bi-emoji-sunglasses display-4"></i>
                    <h1 class="display-6" :class="[$style.title]">Bejelentkezés</h1>
                </div>
                <form class="card-body p-3" @submit.prevent="submit">
                    <AppAlert :text="error.error" :type="error?.css_class" v-if="error" />
                    <div class="mb-3">
                        <label for="inputEmail" class="form-label text-uppercase fw-bold">Email cím</label>
                        <input type="email" class="form-control border-dark rounded-3" id="inputEmail" v-model="email" placeholder="valaki@pelda.hu">
                    </div>
                    <div class="mb-3">
                        <label for="inputPassword" class="form-label text-uppercase fw-bold">Jelszó</label>
                        <input type="password" class="form-control border-dark rounded-3" id="inputPassword" v-model="password" placeholder="Jelszó">
                    </div>
                    <div class="mb-3">
                        <button type="submit" class="btn btn-dark fw-bold w-100 rounded-pill text-uppercase">Bejelentkezek</button>
                    </div>
                    <RouterLink class="btn btn-outline-dark fw-bold w-100 rounded-pill text-uppercase" :to="{ name: 'register' }">Regisztrálok</RouterLink>
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
