<script setup lang="ts">
import { apiFetch } from "@/utils/api-helpers";
import { formatDateValue } from "@/utils/date-formatter";
import { getAuditActionIndicator } from "@/admin/utils/audit-event";
import { computed, ref, watch } from "vue";
import Drawer from "primevue/drawer";
import Button from "primevue/button";
import Tag from "primevue/tag";

interface IAuditLogEntry {
  id: string;
  date: string;
  action: string;
  action_id: string;
  actor: string;
  details: string;
}

interface IAuditLogResponse {
  next: string | null;
  results: IAuditLogEntry[];
}

const props = defineProps<{
  modelLabel: string;
  objectId: string | number;
}>();

const isOpen = ref(false);
const isLoading = ref(false);
const entries = ref<IAuditLogEntry[]>([]);
const nextUrl = ref<string | null>(null);

const historyUrl = computed(() => {
  const query = new URLSearchParams({ model: props.modelLabel, object_id: String(props.objectId), page_size: "10" });
  return `/atlas/api/v1/audit-logs/?${query.toString()}`;
});

const loadHistory = async (url = historyUrl.value, append = false): Promise<void> => {
  isLoading.value = true;
  try {
    const response = await apiFetch(url);
    if (!response.ok) {
      return;
    }

    const data: IAuditLogResponse = await response.json();
    entries.value = append ? [...entries.value, ...data.results] : data.results;
    nextUrl.value = data.next;
  } finally {
    isLoading.value = false;
  }
};

const openHistory = async (): Promise<void> => {
  isOpen.value = true;
  await loadHistory();
};

watch(
  () => [props.modelLabel, props.objectId],
  async () => {
    entries.value = [];
    nextUrl.value = null;
    if (isOpen.value) {
      await loadHistory();
    }
  },
);
</script>

<template>
  <Button label="Historie" icon="pi pi-history" severity="secondary" outlined type="button" @click="openHistory" />

  <Drawer v-model:visible="isOpen" position="right" header="Wijzigingsgeschiedenis" :style="{ width: '480px' }">
    <p v-if="isLoading && !entries.length">Historie laden…</p>
    <p v-else-if="!entries.length">Er zijn nog geen wijzigingen geregistreerd.</p>
    <ol v-else class="history-list">
      <li v-for="entry in entries" :key="entry.id">
        <div class="history-meta">
          <Tag
            :value="getAuditActionIndicator(entry.action_id).label"
            :severity="getAuditActionIndicator(entry.action_id).severity"
            :icon="getAuditActionIndicator(entry.action_id).icon"
          />
          <span>{{ formatDateValue(entry.date) }} · {{ entry.actor }}</span>
        </div>
        <div class="history-details">{{ entry.details }}</div>
      </li>
    </ol>
    <button
      v-if="nextUrl"
      class="button __tertiary tw-mt-4"
      type="button"
      :disabled="isLoading"
      @click="loadHistory(nextUrl, true)"
    >
      Meer laden
    </button>
  </Drawer>
</template>

<style scoped>
.history-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: var(--color-text-grey);
}

.history-list {
  margin: 0;
  padding: 0;
  list-style: none;
}

.history-list li {
  padding: 1rem 0;
  border-bottom: 1px solid var(--color-grey-60);
}

.history-details {
  margin-top: 0.5rem;
  white-space: pre-line;
}
</style>
