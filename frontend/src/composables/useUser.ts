import { API_BASE, GET_ME } from "@/lib/endpoints";
import type { APIError, User } from "@/lib/models";
import { useFetch } from "@vueuse/core";
import { computed, toValue } from "vue";
import { useSession } from "./useSession";

export async function useUser() {
    const { session, isAuthenticated, clearSession } = useSession();

    if (!isAuthenticated.value) {
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
                    if (errorData.error_code === 'unauthorized') {
                        clearSession();
                    }
                    return ctx;
                });
            }

            return ctx;
        },
    }).get().json();

    await execute();

    return computed(() => {
        if (isAuthenticated.value) {
            return toValue(data);
        }

        return null;
    });
}
