<script setup lang="ts">
import { apiFetch } from "@/utils/api-helpers";
import { formatDateValue } from "@/utils/date-formatter";
import { getAuditActionIndicator, getAuditDetails, getAuditValueDisplay } from "@/admin/utils/audit-event";
import { computed, ref, watch } from "vue";
import Drawer from "primevue/drawer";
import Button from "primevue/button";
import Card from "primevue/card";
import Tag from "primevue/tag";

interface IAuditLogEntry {
  id: string;
  date: string;
  action: string;
  action_id: string;
  actor: string;
  details: string;
  summary: string;
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
      <li v-for="entry in entries" :key="entry.id" class="history-entry">
        <div class="history-meta">
          <Tag
            :value="getAuditActionIndicator(entry.action_id).label"
            :severity="getAuditActionIndicator(entry.action_id).severity"
            :icon="getAuditActionIndicator(entry.action_id).icon"
          />
          <span>{{ formatDateValue(entry.date) }} · {{ entry.actor }}</span>
        </div>
        <p class="history-summary">{{ entry.summary }}</p>
        <div class="history-changes">
          <Card
            v-for="(detail, index) in getAuditDetails(entry.details)"
            :key="index"
            :pt="{
              root: {
                class:
                  '!tw-border !tw-border-solid !tw-border-[var(--color-grey-20)] !tw-bg-[#fafafa] !tw-text-black !tw-shadow-none',
              },
              body: { class: '!tw-p-3' },
              content: { class: '!tw-p-0' },
            }"
          >
            <template #content>
              <p v-if="detail.context" class="history-change-context">{{ detail.context }}</p>
              <p v-if="detail.field" class="history-change-field">{{ detail.field }}</p>
              <div
                v-if="
                  detail.oldValue !== undefined &&
                  (getAuditValueDisplay(detail.oldValue).isJson ||
                    getAuditValueDisplay(detail.newValue ?? String()).isJson)
                "
                class="tw-mt-1 tw-grid tw-grid-cols-[minmax(0,1fr)_auto_minmax(0,1fr)] tw-items-center tw-gap-2"
              >
                <div class="tw-min-w-0">
                  <pre
                    class="history-change-old tw-m-0 tw-overflow-x-auto tw-rounded tw-bg-[var(--color-grey-20)] tw-px-2 tw-py-1 tw-font-mono tw-text-sm tw-whitespace-pre-wrap"
                  ><code>{{ getAuditValueDisplay(detail.oldValue).value }}</code></pre>
                </div>
                <span class="history-change-arrow tw-m-0">→</span>
                <div class="tw-min-w-0">
                  <pre
                    class="tw-m-0 tw-overflow-x-auto tw-rounded tw-bg-[var(--color-grey-20)] tw-px-2 tw-py-1 tw-font-mono tw-text-sm tw-whitespace-pre-wrap"
                  ><code>{{ getAuditValueDisplay(detail.newValue ?? String()).value }}</code></pre>
                </div>
              </div>
              <p v-else-if="detail.oldValue !== undefined" class="history-change-values">
                <span class="history-change-old">{{ detail.oldValue }}</span>
                <span class="history-change-arrow">→</span>
                <span>{{ detail.newValue }}</span>
              </p>
              <p v-else class="history-change-value">{{ detail.value }}</p>
            </template>
          </Card>
        </div>
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

.history-entry {
  padding: 1rem 0;
  border-bottom: 1px solid var(--color-grey-60);
}

.history-summary {
  margin: 0.75rem 0;
  font-weight: 600;
}

.history-changes {
  display: grid;
  gap: 0.5rem;
}

.history-change-context,
.history-change-field,
.history-change-values,
.history-change-value {
  margin: 0;
}

.history-change-context {
  color: var(--color-text-grey);
  font-size: 0.875rem;
}

.history-change-field {
  margin-top: 0.25rem;
  font-weight: 600;
}

.history-change-values,
.history-change-value {
  margin-top: 0.25rem;
}

.history-change-old {
  color: var(--color-text-grey);
}

.history-change-arrow {
  margin: 0 0.5rem;
  color: var(--color-text-grey);
}
</style>
