import { API_BASE, GET_ORDER } from "@/lib/endpoints";
import type { APIError, Order } from "@/lib/models";
import { toValue, useFetch } from "@vueuse/core";
import { useSession } from "./useSession";

export async function useOrder(id: number) {
    const { session, isAuthenticated } = useSession();

    if (!isAuthenticated.value) {
        return null;
    }

    const { data, execute, } = useFetch<Order | APIError>(API_BASE + GET_ORDER(id), {
        immediate: false,
        beforeFetch({ options, cancel }) {
            if (!session.value) {
                cancel();
                return;
            }

            options.headers = {
                ...options.headers,
                Authorization: `Bearer ${session.value}`,
              }

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
