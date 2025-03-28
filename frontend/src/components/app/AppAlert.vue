<script setup lang="ts">
import { computed } from 'vue';

const props = withDefaults(defineProps<{
    text: string;
    type?: string;
}>(), {
    type: "info"
});

const alertClass = computed(() => `alert-${props.type}`);
</script>

<template>
    <div class="fw-semibold alert text-center" :class="[alertClass]" role="alert">
        <i class="bi bi-exclamation-diamond-fill me-1 accordion" v-if="type === 'warning'"></i>
        <i class="bi bi-exclamation-triangle-fill me-1" v-else-if="type === 'danger'"></i>
        <i class="bi bi-info-circle-fill me-1" v-else></i>
        {{ text }}
    </div>
</template>
