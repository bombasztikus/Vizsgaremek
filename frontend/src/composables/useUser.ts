import { API_BASE, GET_ME, GET_USER } from "@/lib/endpoints";
import type { APIError, User } from "@/lib/models";
import { useFetch, useLocalStorage } from "@vueuse/core";
import { toValue } from "vue";

export async function useUser(): Promise<User | null> {
    const session = useLocalStorage<string | null>("session", null);

    if (!session.value) {
        return null;
    }

    const { data, execute } = useFetch<User | APIError>(API_BASE + GET_ME, {
        immediate: false,
        beforeFetch({ options }) {
            options.headers!.Authorization = `Bearer ${session.value}`;
            return { options };
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
