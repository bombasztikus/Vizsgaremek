import { defineStore } from 'pinia';
import { useLocalStorage } from '@vueuse/core';
import { computed } from 'vue';
import type { CartItem } from '@/lib/models';

export const useCartStore = defineStore('cart', () => {
    const items = useLocalStorage<CartItem[]>('cart', []);
    const itemCount = computed(() => items.value.length);
    const totalPrice = computed(() => items.value.reduce((acc, item) => acc + (item.price * item.quantity), 0));

    return {
        items,
        itemCount,
        totalPrice,
    }
});
