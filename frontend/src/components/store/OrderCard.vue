<script setup lang="ts">
import type { MinifiedOrder } from '@/lib/models';
import { computed } from 'vue';

const props = defineProps<{
    order: MinifiedOrder;
}>();

const dateCreated = computed(() => {
    const date = new Date(props.order.date_created);

    return new Intl.DateTimeFormat('hu-HU', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        timeZone: 'Europe/Budapest'
    }).format(date);
})
</script>

<template>
    <RouterLink :to="{ name: 'order', params: { id: order.id } }" class="d-block text-decoration-none">
        <article class="card rounded-4 overflow-hidden">
            <div class="card-body justify-content-center">
                <p class="card-title fs-4 fw-semibold mb-1">
                    {{ dateCreated }}
                </p>
                <div class="row">
                    <div class="card-text text-muted">
                        <template v-if="order?.is_completed"><i class="bi bi-check2-circle me-1 text-success"></i>Teljesítve</template>
                        <template v-else><i class="bi bi-clock me-1 text-warning"></i>Teljesítés folyamatban</template>
                    </div>
                </div>
            </div>
        </article>
    </RouterLink>
</template>
