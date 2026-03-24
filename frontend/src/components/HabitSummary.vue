<template>
  <section class="summary-grid">
    <article class="summary-card">
      <p class="summary-label">Total Habits</p>
      <p class="summary-value">{{ total }}</p>
    </article>

    <article class="summary-card">
      <p class="summary-label">Completed</p>
      <p class="summary-value">{{ completed }}</p>
    </article>

    <article class="summary-card">
      <p class="summary-label">Active</p>
      <p class="summary-value">{{ active }}</p>
    </article>
  </section>
</template>

<script setup lang="ts">
defineProps<{
  total: number
  completed: number
  active: number
}>()
</script>