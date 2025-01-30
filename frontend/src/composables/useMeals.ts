import { API_BASE, GET_ALL_MEALS } from '@/lib/endpoints';
import { MealType, type APIError, type Meal, type MealsResponse } from '@/lib/models';
import { useFetch } from '@vueuse/core';
import { computed, ref, watch } from 'vue';

type ComposableType = {
    [MealType.FOOD]: Meal[];
    [MealType.BEVERAGE]: Meal[];
    [MealType.MENU]: Meal[];
    [MealType.DESSERT]: Meal[];
};

export function useMeals() {
    const meals = ref<Meal[]>([]);

    const { data, error } = useFetch<MealsResponse | APIError>(API_BASE + GET_ALL_MEALS).json();

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

    return computed<ComposableType>(() => ({
        [MealType.FOOD]: meals.value.filter((meal) => meal.type === MealType.FOOD),
        [MealType.BEVERAGE]: meals.value.filter((meal) => meal.type === MealType.BEVERAGE),
        [MealType.MENU]: meals.value.filter((meal) => meal.type === MealType.MENU),
        [MealType.DESSERT]: meals.value.filter((meal) => meal.type === MealType.DESSERT),
    }));
}
