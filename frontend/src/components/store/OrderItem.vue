<script setup lang="ts">
import type { Meal } from '@/lib/models';
import { useCartStore } from '@/stores/cart';
import { storeToRefs } from 'pinia';
import { computed } from 'vue';

const props = defineProps<{
    meal: Meal;
    quantity: number;
}>();

const price = computed(() => props.meal.price * props.quantity);
</script>

<template>
    <article class="card rounded-4 overflow-hidden">
        <div class="row">
            <div class="d-none d-md-flex col-md-2 align-items-center p-0">
                <img :src="meal.has_image_url ? meal.image_url : meal.fallback_image_url" class="img-fluid d-block ps-5" :alt="`${meal.name} illusztrációja`">
            </div>
            <div class="col col-md-10">
                <div class="card-body justify-content-center">
                    <p class="card-title fs-4 fw-semibold mb-1">{{ meal.name }}</p>
                    <p class="card-text text-muted">{{ meal.description ?? "Ennek az ételnek vagy italnak nincs leírása, de biztosan nagyon finom." }}</p>
                    <div class="row">
                        <div class="col-6 d-flex flex-column flex-md-row">
                            <div class="fw-bold ms-0 fs-5 d-flex align-items-center">
                                <template v-if="meal.is_free">
                                    <i class="bi bi-gift me-1"></i>INGYEN
                                </template>
                                <template v-else>
                                    {{ price.toLocaleString("hu") }} Ft
                                </template>
                            </div>
                            <div class="fs-6 text-body-tertiary ms-md-2 my-md-auto fw-light" v-if="quantity > 1">({{ meal.price.toLocaleString("hu") }} Ft/db)</div>
                        </div>
                        <div class="col-6 me-0 d-flex gap-3 align-items-center justify-content-end">
                            <p class="fs-5 fw-bold my-auto h-100 align-middle d-flex align-items-center">{{ quantity }} db</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </article>
</template>
