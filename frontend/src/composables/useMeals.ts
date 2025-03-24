import { computed, shallowRef, watch } from 'vue';
import { useFetch } from '@vueuse/core';
import { API_BASE, GET_ALL_MEALS } from '@/lib/endpoints';
import { type APIError, type Meal, type MealsResponse } from '@/lib/models';

export function useMeals(filter_ids?: number[], per_category: number = -1) {
    const meals = shallowRef<Meal[]>([]);


    // Use computed to prevent unnecessary reactivity
    const fetchUrl = computed(() => {
        const url = new URL(API_BASE + GET_ALL_MEALS);
        if (Array.isArray(filter_ids) && filter_ids.length > 0) {
            url.searchParams.set("ids", filter_ids.join(","));
        }
        if (per_category && per_category > 0) {
            url.searchParams.set("per_category", per_category.toString());
        }
        return url.toString();
    });

    const { data, error } = useFetch<MealsResponse | APIError>(fetchUrl).json();

    watch(
        [data, error],
        () => {
            if (error.value) {
                console.error(error.value);
            } else if ((data.value as APIError)?.is_error) {
                console.error((data.value as APIError).error_code);
            } else if ((data.value as MealsResponse)?.items) {
                meals.value = (data.value as MealsResponse).items;
            }
        },
        { immediate: true },
    );

    return meals;
}
