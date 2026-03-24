<template>
  <main class="app">
    <section class="container">
      <header class="header">
        <p class="eyebrow">Full Stack Project</p>
        <h1 class="title">Habit Tracker</h1>
        <p class="subtitle">
          Track daily habits, mark progress, and stay consistent.
        </p>
      </header>

      <AppToast
        :message="toastMessage"
        :type="toastType"
      />

      <HabitSummary
        :total="totalHabits"
        :completed="completedHabits"
        :active="activeHabits"
      />

      <HabitForm
        :submitting="submitting"
        @submit="handleCreateHabit"
      />

      <section class="card">
        <div class="filter-bar">
          <h2 class="filter-title">Filter Habits</h2>

          <div class="filter-buttons">
            <button
              class="filter-button"
              :class="{ 'filter-button--active': filter === 'all' }"
              type="button"
              @click="filter = 'all'"
            >
              All
            </button>

            <button
              class="filter-button"
              :class="{ 'filter-button--active': filter === 'active' }"
              type="button"
              @click="filter = 'active'"
            >
              Active
            </button>

            <button
              class="filter-button"
              :class="{ 'filter-button--active': filter === 'completed' }"
              type="button"
              @click="filter = 'completed'"
            >
              Completed
            </button>
          </div>
        </div>
      </section>

      <HabitList
        :habits="filteredHabits"
        :loading="loading"
        :error="error"
        :empty-message="emptyMessage"
        :show-clear-completed="completedHabits > 0"
        @toggle="handleToggleHabit"
        @delete="handleDeleteHabit"
        @clear-completed="handleClearCompleted"
      />
    </section>
  </main>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import HabitForm from './components/HabitForm.vue'
import HabitList from './components/HabitList.vue'
import HabitSummary from './components/HabitSummary.vue'
import AppToast from './components/AppToast.vue'
import {
  clearCompletedHabits,
  createHabit,
  deleteHabit,
  getHabits,
  updateHabit,
  type Habit,
} from './api'

type HabitFilter = 'all' | 'active' | 'completed'
type ToastType = 'success' | 'error'

const habits = ref<Habit[]>([])
const loading = ref(true)
const error = ref('')
const submitting = ref(false)
const filter = ref<HabitFilter>('all')

const toastMessage = ref('')
const toastType = ref<ToastType>('success')
let toastTimeout: number | undefined

const totalHabits = computed(() => habits.value.length)
const completedHabits = computed(
  () => habits.value.filter((habit) => habit.completed).length,
)
const activeHabits = computed(
  () => habits.value.filter((habit) => !habit.completed).length,
)

const filteredHabits = computed(() => {
  if (filter.value === 'active') {
    return habits.value.filter((habit) => !habit.completed)
  }

  if (filter.value === 'completed') {
    return habits.value.filter((habit) => habit.completed)
  }

  return habits.value
})

const emptyMessage = computed(() => {
  if (filter.value === 'active') {
    return 'No active habits found.'
  }

  if (filter.value === 'completed') {
    return 'No completed habits found.'
  }

  return 'No habits yet.'
})

function showToast(message: string, type: ToastType) {
  toastMessage.value = message
  toastType.value = type

  if (toastTimeout) {
    window.clearTimeout(toastTimeout)
  }

  toastTimeout = window.setTimeout(() => {
    toastMessage.value = ''
  }, 2500)
}

async function loadHabits() {
  try {
    loading.value = true
    error.value = ''
    habits.value = await getHabits()
  } catch (err) {
    console.error(err)
    error.value = 'Unable to load habits.'
    showToast('Unable to load habits.', 'error')
  } finally {
    loading.value = false
  }
}

async function handleCreateHabit(payload: {
  name: string
  description: string | null
}) {
  try {
    submitting.value = true
    error.value = ''

    const newHabit = await createHabit(payload)
    habits.value = [newHabit, ...habits.value]
    showToast('Habit created.', 'success')
  } catch (err) {
    console.error(err)
    error.value = 'Unable to create habit.'
    showToast('Unable to create habit.', 'error')
  } finally {
    submitting.value = false
  }
}

async function handleToggleHabit(habit: Habit) {
  try {
    error.value = ''

    const updatedHabit = await updateHabit(habit.id, {
      completed: !habit.completed,
    })

    habits.value = habits.value.map((item) =>
      item.id === updatedHabit.id ? updatedHabit : item,
    )

    showToast(
      updatedHabit.completed ? 'Habit marked complete.' : 'Habit marked active.',
      'success',
    )
  } catch (err) {
    console.error(err)
    error.value = 'Unable to update habit.'
    showToast('Unable to update habit.', 'error')
  }
}

async function handleDeleteHabit(habitId: number) {
  try {
    error.value = ''
    await deleteHabit(habitId)
    habits.value = habits.value.filter((habit) => habit.id !== habitId)
    showToast('Habit deleted.', 'success')
  } catch (err) {
    console.error(err)
    error.value = 'Unable to delete habit.'
    showToast('Unable to delete habit.', 'error')
  }
}

async function handleClearCompleted() {
  try {
    error.value = ''
    await clearCompletedHabits(habits.value)
    habits.value = habits.value.filter((habit) => !habit.completed)
    showToast('Completed habits cleared.', 'success')
  } catch (err) {
    console.error(err)
    error.value = 'Unable to clear completed habits.'
    showToast('Unable to clear completed habits.', 'error')
  }
}

onMounted(() => {
  loadHabits()
})
</script>