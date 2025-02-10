import { API_BASE, POST_LOGIN } from "@/lib/endpoints";
import type { APIError, User } from "@/lib/models";
import { useFetch } from "@vueuse/core";
import { toValue } from "vue";

export async function useLogin(email: string, password: string) {
    const { data, execute } = useFetch<User | APIError>(API_BASE + POST_LOGIN, {
        immediate: false,
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
        email,
        password
    }).json();

    await execute();

    return toValue(data);
}
