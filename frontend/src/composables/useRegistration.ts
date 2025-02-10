import { API_BASE, POST_REGISTER } from "@/lib/endpoints";
import type { APIError, User } from "@/lib/models";
import { useFetch } from "@vueuse/core";
import { toValue } from "vue";

export async function useRegistration(email: string, password: string, fullName: string) {
    const { data, execute } = useFetch<User | APIError>(API_BASE + POST_REGISTER, {
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
        password,
        full_name: fullName
    }).json();

    await execute();

    return toValue(data);
}
