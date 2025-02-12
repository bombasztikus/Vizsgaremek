<script setup lang="ts">
import type { Meal } from '@/lib/models';
import { useCartStore } from '@/stores/cart';
import { storeToRefs } from 'pinia';

const props = defineProps<{
    meal: Meal;
}>();

const { items: cart } = storeToRefs(useCartStore());
const removeFromCart = () => {
    cart.value = cart.value.filter((i) => i.productId !== props.meal.id);
};
</script>

<template>
    <article class="card rounded-4 overflow-hidden" @click="removeFromCart">
        <div class="row">
            <div class="col-10">
                <div class="card-body justify-content-center">
                    <p class="card-title fs-4 fw-semibold mb-1">{{ meal.name }}</p>
                    <p class="card-text text-muted">{{ meal.description ?? "Ennek az ételnek vagy italnak nincs leírása, de biztosan nagyon finom." }}</p>
                    <p class="fw-bold w-100 m-0 rounded-pill text-uppercase">
                        <template v-if="meal.is_free">
                            <i class="bi bi-gift me-1"></i>INGYEN
                        </template>
                        <template v-else>
                            <i class="bi bi-cart me-2"></i>{{ meal.display_price }}
                        </template>
                    </p>
                </div>
            </div>
            <div class="col-2">
                <img :src="meal.has_image_url ? meal.image_url : meal.fallback_image_url" class="img-fluid d-block py-3" :alt="`${meal.name} illusztrációja`">
            </div>
        </div>
    </article>
</template>
