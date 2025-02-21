<script setup lang="ts">
import type { Meal } from '@/lib/models';
import { useCartStore } from '@/stores/cart';
import { storeToRefs } from 'pinia';
import { computed } from 'vue';

const props = defineProps<{
    meal: Meal;
}>();

const { items: cart } = storeToRefs(useCartStore());

const idx = computed(() => cart.value.findIndex((i) => i.productId === props.meal.id));
const quantity = computed(() => idx.value !== -1 ? cart.value[idx.value].quantity : 0);

const incrementQuantity = () => {
    if (idx.value !== -1) {
        cart.value[idx.value].quantity++;
    }
};

const decrementQuantity = () => {
    if (idx.value !== -1) {
        cart.value[idx.value].quantity--;

        if (cart.value[idx.value].quantity === 0) {
            cart.value = cart.value.filter((i) => i.productId !== props.meal.id);
        }
    }
};

const totalPriceForThisItem = computed(() => cart.value.reduce((acc, item) => {
    if (item.productId === props.meal.id) {
        return acc + item.price * item.quantity;
    }

    return acc;
}, 0));
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
                                    <i class="bi bi-cart me-2"></i>{{ totalPriceForThisItem.toLocaleString("hu") }} Ft
                                </template>
                            </div>
                            <div class="fs-6 text-body-tertiary my-auto fw-light">({{ meal.price.toLocaleString("hu") }} Ft/db)</div>
                        </div>
                        <div class="col-6 me-0 d-flex gap-3 align-items-center justify-content-end">
                            <button type="button" class="btn btn-outline-dark rounded-3" @click="decrementQuantity">
                                <i class="bi bi-dash fs-5 h-100"></i>
                            </button>
                            <p class="fs-5 fw-bold my-auto h-100 pb-1 align-middle d-flex align-items-center">{{ quantity }}</p>
                            <button type="button" class="btn btn-outline-dark rounded-3" @click="incrementQuantity">
                                <i class="bi bi-plus fs-5 h-100"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </article>
</template>
