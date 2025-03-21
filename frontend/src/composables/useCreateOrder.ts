import { API_BASE, POST_ORDER } from "@/lib/endpoints";
import type { APIError, CartItem, Order, OrderCreationItem } from "@/lib/models";
import { toValue, useFetch } from "@vueuse/core";
import { useSession } from "./useSession";

export async function useCreateOrder(address: string, items: CartItem[]): Promise<Order | APIError | null> {
    const { session, isAuthenticated } = useSession();

    if (!isAuthenticated.value) {
        return null;
    }

    const iems = items.map((item: CartItem): OrderCreationItem => ({
        id: item.productId,
        quantity: item.quantity
    }));

    const { data, execute } = useFetch<Order | APIError>(API_BASE + POST_ORDER, {
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
    }).post({
        address,
        items: iems
    }).json();

    await execute();

    return toValue(data);
}
