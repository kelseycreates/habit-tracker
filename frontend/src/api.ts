const API_BASE_URL = "http://127.0.0.1:8000";

export interface Habit {
  id: number;
  name: string;
  description: string | null;
  completed: boolean;
  created_at: string;
}

export interface CreateHabitPayload {
  name: string;
  description: string | null;
}

export async function getHabits(): Promise<Habit[]> {
  const response = await fetch(`${API_BASE_URL}/habits`);

  if (!response.ok) {
    throw new Error("Failed to fetch habits");
  }

  return response.json();
}

export async function createHabit(payload: CreateHabitPayload): Promise<Habit> {
  const response = await fetch(`${API_BASE_URL}/habits`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error("Failed to create habit");
  }

  return response.json();
}

export interface UpdateHabitPayload {
  completed: boolean;
}

export async function updateHabit(
  habitId: number,
  payload: UpdateHabitPayload,
): Promise<Habit> {
  const response = await fetch(`${API_BASE_URL}/habits/${habitId}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error("Failed to update habit");
  }

  return response.json();
}

export async function deleteHabit(habitId: number): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/habits/${habitId}`, {
    method: "DELETE",
  });

  if (!response.ok) {
    throw new Error("Failed to delete habit");
  }
}

export async function clearCompletedHabits(habits: Habit[]): Promise<void> {
  const completedHabits = habits.filter((habit) => habit.completed);

  await Promise.all(completedHabits.map((habit) => deleteHabit(habit.id)));
}
