import { API_BASE, POST_REGISTER } from "@/lib/endpoints";
import type { APIError, User } from "@/lib/models";
import { useFetch } from "@vueuse/core";
import { computed } from "vue";

export function useRegistration(email: string, password: string, fullName: string) {
    const { data, error } = useFetch<User | APIError>(API_BASE + POST_REGISTER, {
        afterFetch(ctx) {
            if (!ctx.response.ok) {
                console.error((ctx.data as APIError).error);
            }
            return ctx;
        },
    }).post({
        email,
        password,
        full_name: fullName
    }).json();

    return computed(() => data.value ?? error.value);
}
