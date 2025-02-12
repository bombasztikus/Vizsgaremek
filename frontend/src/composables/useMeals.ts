import { API_BASE, GET_ALL_MEALS } from '@/lib/endpoints';
import { MealType, type APIError, type Meal, type MealsResponse } from '@/lib/models';
import { useFetch } from '@vueuse/core';
import { computed, ref, watch } from 'vue';

export function useMeals(filter_ids?: number[]) {
    const meals = ref<Meal[]>([]);

    const url = new URL(API_BASE + GET_ALL_MEALS);
    if (Array.isArray(filter_ids) && filter_ids.length > 0) {
        url.searchParams.set("ids", filter_ids.join(","));
    }

    const { data, error } = useFetch<MealsResponse | APIError>(url.toString()).json();

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
        {
            immediate: true,
        },
    );

    return meals;
}
