<script setup lang="ts">
import AppAlert from '@/components/app/AppAlert.vue';
import { useRegistration } from '@/composables/useRegistration';
import type { APIError } from '@/lib/models';
import { useLocalStorage, useTitle } from '@vueuse/core';
import { ref, watch } from 'vue';
import { RouterLink, useRouter } from 'vue-router';

useTitle("Regisztráció");

const session = useLocalStorage<string | null>("session", null);
const router = useRouter();

const email = ref<string>("");
const password = ref<string>("");
const fullName = ref<string>("");
const error = ref<APIError | null>(null);

const reset = () => {
    email.value = "";
    password.value = "";
    fullName.value = "";
    error.value = null;
}

const submit = async () => {
    try {
        const response = await useRegistration(email.value, password.value, fullName.value);

        if (response?.is_error) {
            error.value = response;
        } else {
            reset();
            router.push({ name: "login" });
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
                <i class="bi bi-emoji-heart-eyes display-4"></i>
                <h1 class="display-6" :class="[$style.title]">Regisztráció</h1>
            </div>
            <form class="card-body p-3" @submit.prevent="submit">
                    <AppAlert :text="error.error" :type="error?.css_class" v-if="error" />
                    <div class="mb-3">
                        <label for="inputFullName" class="form-label text-uppercase fw-bold">Teljes név</label>
                        <input type="text" class="form-control rounded-3" id="inputFullName" aria-describedby="fullNameHelp" v-model.trim="fullName" placeholder="Példa Pista" :class="{
                            'border-dark': fullName.trim().length > 0,
                            'is-invalid': fullName.trim().length === 0,
                        }">
                        <div id="fullNameHelp" class="form-text" :class="{
                            'valid-feedback': fullName.trim().length > 0,
                            'invalid-feedback': fullName.trim().length === 0,
                        }">A rendelések beazonosításához szükséges</div>
                    </div>
                    <div class="mb-3">
                        <label for="inputEmail" class="form-label text-uppercase fw-bold">Email cím</label>
                        <input type="email" class="form-control rounded-3" id="inputEmail" aria-describedby="emailHelp" v-model.trim="email" placeholder="valaki@pelda.hu" :class="{
                            'border-dark': email.trim().length > 0,
                            'is-invalid': email.trim().length === 0,
                        }">
                        <div id="emailHelp" class="form-text" :class="{
                            'valid-feedback': email.trim().length > 0,
                            'invalid-feedback': email.trim().length === 0,
                        }">Kérjük, adj meg egy érvényes címet</div>
                    </div>
                    <div class="mb-3">
                        <label for="inputPassword" class="form-label text-uppercase fw-bold">Jelszó</label>
                        <input type="password" class="form-control rounded-3" id="inputPassword" aria-describedby="passwordHelp" v-model.trim="password" placeholder="Jelszó" :class="{
                            'border-dark': password.trim().length > 0,
                            'is-invalid': password.trim().length === 0,
                        }">
                        <div id="passwordHelp" class="form-text" :class="{
                            'valid-feedback': password.trim().length > 0,
                            'invalid-feedback': password.trim().length === 0,
                        }">Legalább 6 karakter hosszú kell legyen</div>
                    </div>
                    <div class="mb-3">
                        <button type="submit" class="btn btn-dark fw-bold w-100 rounded-pill text-uppercase" :disabled="email.length === 0 || password.length === 0 || fullName.length == 0">Regisztrálok</button>
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
