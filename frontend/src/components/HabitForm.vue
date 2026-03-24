<template>
  <section class="card">
    <h2>Add Habit</h2>

    <form class="habit-form" @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="name" class="label">Habit name</label>
        <input
          id="name"
          v-model="name"
          class="input"
          type="text"
          placeholder="Enter a habit name"
          required
        />
      </div>

      <div class="form-group">
        <label for="description" class="label">Description</label>
        <textarea
          id="description"
          v-model="description"
          class="textarea"
          placeholder="Optional description"
          rows="3"
        />
      </div>

      <button class="button" type="submit" :disabled="submitting">
        {{ submitting ? 'Saving...' : 'Add Habit' }}
      </button>
    </form>
  </section>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'

const DRAFT_NAME_KEY = 'habit-tracker-draft-name'
const DRAFT_DESCRIPTION_KEY = 'habit-tracker-draft-description'

defineProps<{
  submitting: boolean
}>()

const emit = defineEmits<{
  submit: [payload: { name: string; description: string | null }]
}>()

const name = ref('')
const description = ref('')

function handleSubmit() {
  emit('submit', {
    name: name.value.trim(),
    description: description.value.trim() || null,
  })

  name.value = ''
  description.value = ''
  localStorage.removeItem(DRAFT_NAME_KEY)
  localStorage.removeItem(DRAFT_DESCRIPTION_KEY)
}

onMounted(() => {
  name.value = localStorage.getItem(DRAFT_NAME_KEY) ?? ''
  description.value = localStorage.getItem(DRAFT_DESCRIPTION_KEY) ?? ''
})

watch(name, (value) => {
  localStorage.setItem(DRAFT_NAME_KEY, value)
})

watch(description, (value) => {
  localStorage.setItem(DRAFT_DESCRIPTION_KEY, value)
})
</script>