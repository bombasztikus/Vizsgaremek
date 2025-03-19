<script setup lang="ts">
import { useOrder } from '@/composables/useOrder';
import type { Meal, Order, OrderItem } from '@/lib/models';
import { useRouteParams } from '@vueuse/router';
import { computed, onBeforeMount, ref, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useMeals } from '@/composables/useMeals';
import OrderItemElem from '@/components/store/OrderItem.vue';

const orderId = useRouteParams('id', undefined, { transform: Number });
const router = useRouter();
const order = ref<Order | undefined>(undefined);

type Entry = {
    meta: OrderItem;
    data: Meal;
}

const ids = computed(() => order.value?.items.map((i) => i.meal_id));
const mealsRef = useMeals(ids.value);
const entries = ref<Entry[]>([]);

onBeforeMount(async () => {
    if ((orderId.value === undefined || isNaN(orderId.value) || orderId.value < 1)) {
        await router.push({ name: 'home' });
        return;
    }

    order.value = await useOrder(orderId.value);

    if (!order.value) {
        await router.push({ name: 'home' });
    }
});

watch([mealsRef, order], () => {
    order.value?.items.map((item) => {
        const meal = mealsRef.value.find((m) => m.id === item.meal_id);
        if (meal) {
            entries.value.push({ meta: item, data: meal });
        }
    });
})

const totalPrice = computed(() => entries.value.reduce((acc, item) => acc + (item.data.price * item.meta.quantity), 0));
</script>

<template>
    <main class="container-lg">
        <form class="row my-4">
            <div class="col-md-9 col-auto">
                <h1 class="display-4 fw-bold lh-1 mb-md-3 mb-2  m-0 text-glow">Rendelés állapota</h1>
                <div class="mb-1 badge text-bg-light fs-4">#{{ order?.id ?? 'n/a' }}</div>
                <hr class="my-4">
                <div class="card rounded-4" v-if="!order">
                    <div class="card-body text-center">
                        <p class="fs-4 fw-bold m-0">A rendelés betöltése közben hibába ütköztünk.</p>
                    </div>
                </div>
                <section class="d-flex flex-column gap-3" v-else>
                    <OrderItemElem :meal="data" :quantity="meta.quantity" v-for="{ data, meta } in entries" :key="data.id" />
                </section>
            </div>
            <div class="col-md-3 col mt-4 mt-md-4 sticky-top h-100">
                <div class="card rounded-4 bg-md-background" :class="[$style.sidebar]">
                    <div class="card-body">
                        <p class="text-uppercase fw-bold mb-1">
                            <template v-if="order?.is_completed"><i class="bi bi-check2-circle me-2 text-success"></i>KIFIZETVE</template>
                            <template v-else><i class="bi bi-clock me-2 text-warning"></i>KIFIZETÉSRE VÁR</template>
                        </p>
                        <div class="display-5 fw-bold m-0">{{ totalPrice?.toLocaleString('hu') }} Ft</div>
                        <p class="form-text mt-2">A kalkuláció <b>nem tartalmazza</b> az adókat és szállítási díjat. Fizetni a rendelés átvételekor a futárnál, kasszánál vagy pincérnél tudsz.</p>
                        <hr class="my-4">
                        <div class="mb-3">
                            <p class="form-label text-uppercase fw-bold mb-2">Átvétel HELYE</p>
                            <p class="badge text-bg-light m-0">{{ order?.address ?? 'n/a' }}</p>
                            <div class="form-text mt-2">Az átvétel helye utólag nem módosítható.</div>
                        </div>
                        <div>
                            <p class="form-label text-uppercase fw-bold mb-2">RENDELÉS ÁLLAPOTA</p>
                            <p class="badge text-bg-light m-0">
                                <template v-if="order?.is_completed"><i class="bi bi-check2-circle me-1 text-success"></i>Befejezve</template>
                                <template v-else><i class="bi bi-clock me-1 text-warning"></i>Teljesítés folyamatban</template>
                            </p>
                            <div class="form-text mt-2">
                                <template v-if="order?.is_completed">Probléma esetén keresd ügyfélszolgálatunkat.</template>
                                <template v-else>Frissítsd az oldalt a frissítéshez.</template>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </form>
    </main>
</template>

<style module>
@media (min-width: 768px) {
    .sidebar {
        top: calc(var(--bs-navbar-height, 3rem) + 2.5rem);
    }
}
</style>
