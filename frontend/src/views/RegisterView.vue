<script setup lang="ts">
import { useRegistration } from '@/composables/useRegistration';
import type { APIError } from '@/lib/models';
import router from '@/router';
import { computed, ref, watch, watchEffect } from 'vue';

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
    <div class="mt-5 row g-3 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 justify-content-center">
        <div class="card h-100 rounded-4 overflow-hidden col" style="max-width: 400px;">
            <form class="card-body d-flex flex-column" @submit.prevent="submit">
                <div class="alert" :class="[errorClass]" role="alert" v-if="error">
                    {{ error.error }}
                </div>
                <div class="mb-3">
                    <label for="fullNameHelp" class="form-label">Teljes név</label>
                    <input type="text" class="form-control" id="inputEmail" aria-describedby="fullNameHelp" v-model="fullName">
                    <div id="fullNameHelp" class="form-text">Így tudjuk majd, hogy kinek kell kiszállítani</div>
                </div>
                <div class="mb-3">
                    <label for="inputEmail" class="form-label">Email cím</label>
                    <input type="email" class="form-control" id="inputEmail" aria-describedby="emailHelp" v-model="email">
                    <div id="emailHelp" class="form-text">Érvényes címet adj meg</div>
                </div>
                <div class="mb-3">
                    <label for="inputPassword" class="form-label">Jelszó</label>
                    <input type="password" class="form-control" id="inputPassword" aria-describedby="passwordHelp" v-model="password">
                    <div id="passwordHelp" class="form-text">Legalább 6 karakter hosszú kell legyen</div>
                </div>
                <button type="submit" class="btn btn-primary">Regisztrálok</button>
            </form>
        </div>
    </div>
</template>
