import { API_BASE, GET_ALL_ORDERS } from "@/lib/endpoints";
import type { APIError, OrdersResponse } from "@/lib/models";
import { toValue, useFetch } from "@vueuse/core";
import { useSession } from "./useSession";

export async function useOrders(): Promise<OrdersResponse | APIError | null> {
    const { session, isAuthenticated } = useSession();

    if (!isAuthenticated.value) {
        return null;
    }

    const { data, execute } = useFetch<OrdersResponse | APIError>(API_BASE + GET_ALL_ORDERS, {
        immediate: false,
        beforeFetch({ options }) {
            options.headers!.Authorization = `Bearer ${session.value}`;
            return { options };
        },
        afterFetch(ctx) {
            return ctx;
        },
        onFetchError(ctx) {
            if (ctx.response) {
                return ctx.response.json().then((errorData: APIError) => {
                    data.value = errorData;
                    return ctx;
                });
            }

            return ctx;
        },
    }).get().json();

    await execute();

    return toValue(data);
}
