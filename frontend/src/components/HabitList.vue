<template>
  <section class="card">
    <div class="list-header">
      <h2>Your Habits</h2>

      <button
        v-if="showClearCompleted"
        class="button button-secondary"
        type="button"
        @click="$emit('clear-completed')"
      >
        Clear Completed
      </button>
    </div>

    <p v-if="loading">Loading habits...</p>
    <p v-else-if="error">{{ error }}</p>
    <p v-else-if="habits.length === 0">{{ emptyMessage }}</p>

    <ul v-else class="habit-list">
      <li
        v-for="habit in habits"
        :key="habit.id"
        class="habit-item"
        :class="{ 'habit-item--completed': habit.completed }"
      >
        <div class="habit-content">
          <h3 class="habit-name">{{ habit.name }}</h3>
          <p v-if="habit.description" class="habit-description">
            {{ habit.description }}
          </p>
        </div>

        <div class="habit-actions">
          <label class="checkbox-row">
            <input
              type="checkbox"
              :checked="habit.completed"
              @change="$emit('toggle', habit)"
            />
            <span>{{ habit.completed ? "Completed" : "Mark complete" }}</span>
          </label>

          <button
            class="button button-secondary"
            type="button"
            @click="$emit('delete', habit.id)"
          >
            Delete
          </button>
        </div>
      </li>
    </ul>
  </section>
</template>

<script setup lang="ts">
import type { Habit } from "../api";

defineProps<{
  habits: Habit[];
  loading: boolean;
  error: string;
  emptyMessage: string;
  showClearCompleted: boolean;
}>();

defineEmits<{
  toggle: [habit: Habit];
  delete: [habitId: number];
  "clear-completed": [];
}>();
</script>
