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
    <div class="fw-semibold alert" :class="[alertClass]" role="alert">
        <i class="bi bi-info-circle-fill me-2"></i>{{ text }}
    </div>
</template>
