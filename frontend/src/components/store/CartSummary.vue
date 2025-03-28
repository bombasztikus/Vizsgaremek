<script setup lang="ts">
import { useUser } from '@/composables/useUser';
import { computed, ref, watch, type InputHTMLAttributes } from 'vue';
import ImageKHSzepkartya from '@/assets/payment/kh.png';
import ImageOTPSzepkartya from '@/assets/payment/otp.png';
import ImageMBHSzepkartya from '@/assets/payment/mbh.png';
import ImageCashAccepted from '@/assets/payment/cash.png';
import { useCartStore } from '@/stores/cart';
import { storeToRefs } from 'pinia';
import { useCreateOrder } from '@/composables/useCreateOrder';
import { useRouter } from 'vue-router';
import type { APIError, Order } from '@/lib/models';
import AppAlert from '../app/AppAlert.vue';

const paymentProcessors = [ImageKHSzepkartya, ImageOTPSzepkartya, ImageMBHSzepkartya, ImageCashAccepted];

const { totalPrice, items, itemCount } = storeToRefs(useCartStore());
const user = await useUser();
const promptForLogin = computed(() => !user);
const router = useRouter();

const error = ref<APIError | null>(null);

interface BaseDeliveryMethod {
  label: string;
  id: string;
  requiresCustomInput: boolean;
}

interface DeliveryMethodWithCustomInput extends BaseDeliveryMethod {
  requiresCustomInput: true;
  customInputLabel: string;
  customInputDescription: string;
  customInputPlaceholder: string;
  customInputType: InputHTMLAttributes["type"];
}

interface DeliveryMethodWithoutCustomInput extends BaseDeliveryMethod {
  requiresCustomInput: false;
  customInputLabel?: undefined;
  customInputDescription?: undefined;
  customInputPlaceholder?: undefined;
  customInputType?: undefined;
}

type DeliveryMethod = DeliveryMethodWithCustomInput | DeliveryMethodWithoutCustomInput;

const deliveryMethods: DeliveryMethod[] = [
    {
        label: "Átvétel a pultnál",
        id: "checkout",
        requiresCustomInput: false,
    },
    {
        label: "Átvétel az asztalnál",
        id: "table",
        requiresCustomInput: true,
        customInputLabel: "Asztalszám",
        customInputDescription: "Add meg annak az asztalnak a számát, ahol ülsz. Az asztalszám az asztal közepén található.",
        customInputPlaceholder: "Asztalszám",
        customInputType: "number",
    },
    {
        label: "Kiszállítás futárral",
        id: "delivery",
        requiresCustomInput: true,
        customInputLabel: "Kiszállítási cím",
        customInputDescription: "Budapesten belül 45, Pest megyén belül pedig 90 perc alatt garantáljuk a kiszállítást. Kérjük, hogy ne adj meg más címet, mert a rendelést törölni fogjuk.",
        customInputPlaceholder: "1234 Budapest, Példa u. 1",
        customInputType: "text",
    }
];

const customInputValue = ref<string | undefined>(undefined);
const chosenDeliveryMethod = ref<DeliveryMethod>(deliveryMethods[0]);

watch(chosenDeliveryMethod, () => {
    customInputValue.value = "";
});

const clearCart = () => items.value = [];

const submit = async () => {
    if (itemCount.value === 0) {
        return;
    }

    if (!customInputValue.value) {
        if (chosenDeliveryMethod.value.requiresCustomInput) {
            return;
        }

        customInputValue.value = chosenDeliveryMethod.value.label;
    }

    if (!user?.value) {
        return;
    }

    const order = await useCreateOrder(customInputValue.value, items.value);

    if (!order) {
        return;
    } else if (order.is_error === true) {
        error.value = order as APIError;
        return;
    }

    router.push({ name: 'order', params: { id: (order as Order).id } });
    clearCart();
};
</script>

<template>
    <form class="row my-4" @submit.prevent="submit">
        <div class="col-md-9 col-auto">
            <h1 class="display-4 fw-bold lh-1 mb-md-3 mb-2  m-0 text-glow">Összesítés</h1>
            <p class="mb-3">Már csak pár lépés és nemsokára az asztalodon landol a rendelésed. Kérjük, hogy valós adatokat adj meg.</p>
            <hr class="my-4">
            <slot>
                <div class="card rounded-4">
                    <div class="card-body d-flex flex-column gap-1 justify-content-center align-items-center text-center">
                        <p class="fs-4 fw-bold">A kosarad üres. Miért nem adsz hozzá valamit?</p>
                        <RouterLink :to="{ name: 'home' }" class="btn btn-dark d-block rounded-pill fw-bold px-4 py-2">Mutasd a kínálatot</RouterLink>
                    </div>
                </div>
            </slot>
            <button type="button" @click="clearCart" class="btn btn-outline-dark d-block rounded-pill fw-semibold px-4 mx-auto mt-4 fs-6" v-if="itemCount > 0">Kosár kiürítése</button>
        </div>
        <div class="col-md-3 col mt-4 mt-md-4 sticky-top h-100">
            <div class="card rounded-4 bg-md-background" :class="[$style.sidebar]">
                <div class="card-body" v-if="promptForLogin">
                    <p class="text-uppercase fw-bold mb-3 text-center">REGISZTRÁLJ<br>VAGY JELENTKEZZ BE</p>
                    <p class="form-text text-center mt-3 mb-3">A rendelés beazonosításához szükségünk lesz néhány adatodra.</p>
                    <div class="d-flex flex-column gap-2">
                        <RouterLink class="btn btn-dark fw-bold w-100 rounded-pill text-uppercase" :to="{ name: 'register' }">Regisztrálok</RouterLink>
                        <RouterLink type="submit" class="btn btn-outline-dark fw-bold w-100 rounded-pill text-uppercase" :to="{ name: 'login' }">Bejelentkezek</RouterLink>
                    </div>
                </div>
                <div class="card-body" v-else>
                    <p class="text-uppercase fw-bold mb-1">Fizetendő</p>
                    <div class="display-5 fw-bold m-0">{{ totalPrice.toLocaleString("hu") }} Ft</div>
                    <p class="form-text mt-2">A kalkuláció <b>nem tartalmazza</b> az adókat és szállítási díjat. Fizetni a
                        <b v-if="chosenDeliveryMethod.id === 'checkout'">kasszánál</b>
                        <b v-else-if="chosenDeliveryMethod.id === 'table'">pincérnél</b>
                        <b v-else-if="chosenDeliveryMethod.id === 'delivery'">futárnál</b>
                        tudsz majd.</p>
                        <div class="mb-4">
                            <label for="inputDeliveryType" class="form-label text-uppercase fw-bold mb-2">Átvétel formája</label>
                            <select id="inputDeliveryType" class="form-select border-dark rounded-3" v-model="chosenDeliveryMethod" aria-describedby="deliveryMethodHelp" :disabled="itemCount === 0">
                                <option v-for="method in deliveryMethods" :key="method.id" :value="method">{{ method.label }}</option>
                            </select>
                            <div id="deliveryMethodHelp" class="form-text mt-2">Válaszd ki, hogyan szeretnéd átvenni a rendelésed.</div>
                        </div>
                        <div class="mb-3" v-if="chosenDeliveryMethod.requiresCustomInput">
                            <label for="inputAddress" class="form-label text-uppercase fw-bold mb-2">{{ chosenDeliveryMethod.customInputLabel }}</label>
                            <input :type="chosenDeliveryMethod.customInputType" class="form-control border-dark rounded-3" id="inputAddress" aria-describedby="addressHelp" required v-model="customInputValue" :placeholder="chosenDeliveryMethod.customInputPlaceholder">
                            <div id="addressHelp" class="form-text mt-2">{{ chosenDeliveryMethod.customInputDescription }}</div>
                        </div>
                        <hr>
                        <button type="submit" class="btn btn-dark d-block rounded-pill my-4 fw-bold px-4 py-2 w-100" :class="{ 'disabled': itemCount === 0 }">MEGRENDELEM</button>
                        <AppAlert :text="error.error" :type="error?.css_class" v-if="error" />
                    <div class="row gap-2 justify-content-center mt-4">
                        <img :src="processor" alt="" width="40" height="26" class="col-auto" v-for="processor in paymentProcessors" :key="processor">
                    </div>
                    <p class="form-text text-center mt-3 mb-0">Szépkártya, hitelkártya, bankkártya, készpénz elfogadóhely</p>
                </div>
            </div>
        </div>
    </form>
</template>

<style module>
@media (min-width: 768px) {
    .sidebar {
        top: calc(var(--bs-navbar-height, 3rem) + 2.5rem);
    }
}
</style>
