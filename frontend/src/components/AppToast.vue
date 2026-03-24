<template>
  <transition name="toast-fade">
    <div
      v-if="message"
      class="toast"
      :class="toastClass"
      role="status"
      aria-live="polite"
    >
      {{ message }}
    </div>
  </transition>
</template>

<script setup lang="ts">
import { computed } from "vue";

const props = defineProps<{
  message: string;
  type: "success" | "error";
}>();

const toastClass = computed(() => {
  return props.type === "success" ? "toast--success" : "toast--error";
});
</script>
