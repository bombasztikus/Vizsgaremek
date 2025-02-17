<script setup lang="ts">
import { useUser } from '@/composables/useUser';
import { computed, ref, watch, type InputHTMLAttributes } from 'vue';
import ImageKHSzepkartya from '@/assets/payment/kh.png';
import ImageOTPSzepkartya from '@/assets/payment/otp.png';
import ImageMBHSzepkartya from '@/assets/payment/mbh.png';
import ImageCashAccepted from '@/assets/payment/cash.png';

const paymentProcessors = [ImageKHSzepkartya, ImageOTPSzepkartya, ImageMBHSzepkartya, ImageCashAccepted];

defineProps<{
    totalCost: number;
    itemCount: number;
    locations: string[];
}>();

const user = await useUser();
const promptForLogin = computed(() => !!user);

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
</script>

<template>
    <form class="row my-5">
        <h1 class="display-4 fw-bold lh-1 mb-md-3 mb-2  m-0 text-glow">Összesítés</h1>
        <p class="m-0">Már csak pár lépés és nemsokára az asztalodon landol a rendelésed. Kérjük, hogy valós adatokat adj meg.</p>
        <hr class="my-4 my-md-5">
        <div class="col-sm-auto col-md-9">
            <div class="mb-4">
                <label for="inputDeliveryType" class="form-label text-uppercase fw-bold mb-2">Átvétel formája</label>
                <select id="inputDeliveryType" class="form-select border-dark rounded-3" aria-describedby="deliveryTypeHelp" v-model="chosenDeliveryMethod">
                    <option v-for="method in deliveryMethods" :key="method.id" :value="method">{{ method.label }}</option>
                </select>
            </div>
            <div class="mb-3" v-if="chosenDeliveryMethod.requiresCustomInput">
                <label for="inputAddress" class="form-label text-uppercase fw-bold mb-2">{{ chosenDeliveryMethod.customInputLabel }}</label>
                <input :type="chosenDeliveryMethod.customInputType" class="form-control border-dark rounded-3" id="inputAddress" aria-describedby="addressHelp" v-model="customInputValue" :placeholder="chosenDeliveryMethod.customInputPlaceholder">
                <div id="addressHelp" class="form-text">{{ chosenDeliveryMethod.customInputDescription }}</div>
            </div>
        </div>
        <div class="col-sm-auto col-md-3">
            <div class="mb-3 card rounded-4">
                <div class="card-body">
                    <p class="text-uppercase fw-bold mb-1">Fizetendő</p>
                    <div class="display-5 fw-bold m-0">{{ totalCost }} Ft</div>
                    <p class="form-text mt-2">A kalkuláció <b>nem tartalmazza</b> az adókat és szállítási díjat. Fizetni a
                        <b v-if="chosenDeliveryMethod.id === 'checkout'">kasszánál</b>
                        <b v-else-if="chosenDeliveryMethod.id === 'table'">pincérnél</b>
                        <b v-else-if="chosenDeliveryMethod.id === 'delivery'">futárnál</b>
                        tudsz majd.</p>
                        <hr>
                        <RouterLink :to="{ name: 'register' }" class="btn btn-dark d-block rounded-pill mt-4 fw-bold px-4 py-2">MEGRENDELEM</RouterLink>
                    <div class="row gap-2 justify-content-center mt-4">
                        <img :src="processor" alt="" width="40" height="26" class="col-auto" v-for="processor in paymentProcessors" :key="processor">
                    </div>
                    <p class="form-text text-center mt-3 mb-0">Szépkártya, hitelkártya, bankkártya, készpénz elfogadóhely</p>
                </div>
            </div>
        </div>
        <!-- <img :src="DeliveryAdImage" class="object-fit-cover col-10 col-sm-8 col-lg-6 d-none d-lg-block p-0 m-0 img-fluid" alt=""> -->
    </form>
</template>
