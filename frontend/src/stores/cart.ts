import { defineStore } from 'pinia';
import { useLocalStorage } from '@vueuse/core';
import { computed } from 'vue';

export const useCartStore = defineStore('cart', () => {
    const itemIds = useLocalStorage('cart', []);
    const itemCount = computed(() => itemIds.value.length);

    return {
        itemIds,
        itemCount
    }
});
