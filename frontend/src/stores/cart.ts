import { defineStore } from 'pinia';
import { useLocalStorage } from '@vueuse/core';
import { computed } from 'vue';
import type { CartItem } from '@/lib/cart';

export const useCartStore = defineStore('cart', () => {
    const items = useLocalStorage<CartItem[]>('cart', []);
    const itemCount = computed(() => items.value.length);

    return {
        items,
        itemCount
    }
});
