<script setup lang="ts">
import { useUser } from '@/composables/useUser';
import { computed, ref } from 'vue';

defineProps<{
    totalCost: number;
    itemCount: number;
    locations: string[];
}>();

const user = await useUser();
const promptForLogin = computed(() => !!user);

const requestShipping = ref(false);
const deliveryAddress = ref("");
</script>

<template>
    <form class="row g-5 my-5">
        <h1 class="display-4 fw-bold lh-1 mb-3 text-glow">Összesítés</h1>
        <p class="m-0">Már csak pár lépés és nemsokára az asztalodon landol a rendelésed. Kérjük, hogy valós adatokat adj meg.</p>
        <hr class="my-4">
        <div class="col-9">
            <div class="mb-4">
                <label for="inputDeliveryType" class="form-label text-uppercase fw-bold mb-2">Átvétel formája</label>
                <select id="inputDeliveryType" class="form-select border-dark rounded-3" aria-describedby="deliveryTypeHelp">
                    <option v-for="location in locations" :key="location">{{ location }}</option>
                </select>
            </div>
            <div class="mb-3">
                <label for="inputAddress" class="form-label text-uppercase fw-bold mb-2">Kiszállítási cím</label>
                <input type="text" class="form-control border-dark rounded-3" id="inputAddress" aria-describedby="addressHelp">
                <div id="addressHelp" class="form-text">Budapesten belül 45, Pest megyén belül pedig 90 perc alatt garantáljuk a kiszállítást. Kérjük, hogy ne adj meg más címet, mert a rendelést törölni fogjuk.</div>
            </div>
        </div>
        <div class="col-3">
            <div class="mb-3 card rounded-4">
                <div class="card-body">
                    <p class="text-uppercase fw-bold mb-2">Fizetendő</p>
                    <div class="display-5 fw-bold m-0">{{ totalCost }} Ft</div>
                    <p class="form-text mt-2">A kalkuláció tartalmazza az adókat és szállítási díjat.</p>
                    <RouterLink :to="{ name: 'register' }" class="btn btn-dark d-block rounded-pill mt-4 fw-bold px-4 py-2">MEGRENDELEM</RouterLink>
                </div>
            </div>
        </div>
        <!-- <img :src="DeliveryAdImage" class="object-fit-cover col-10 col-sm-8 col-lg-6 d-none d-lg-block p-0 m-0 img-fluid" alt=""> -->
    </form>
</template>
