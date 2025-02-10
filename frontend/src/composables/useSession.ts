import { useLocalStorage } from "@vueuse/core";
import { computed } from "vue";

type T = string | null;

const session = useLocalStorage<T>("session", null);

export function useSession() {

    const setSession = (value: T) => {
        session.value = value;
    }

    const clearSession = () => {
        session.value = null;
    };

    const isAuthenticated = computed(() => session.value !== null);

    return {
        session,
        setSession,
        clearSession,
        isAuthenticated
    };
};
