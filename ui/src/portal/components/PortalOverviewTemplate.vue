<template>
  <div class="tw-min-h-screen tw-bg-gray-50">
    <!-- Page Header -->
    <header class="tw-bg-white tw-border-b tw-border-gray-200 tw-border-solid tw-border-0">
      <div class="tw-max-w-7xl tw-mx-auto tw-px-6 tw-py-12">
        <div class="tw-flex tw-items-start tw-gap-4 tw-mb-4">
          <div
            class="tw-w-16 tw-h-16 tw-bg-gray-50 tw-rounded-2xl tw-flex tw-items-center tw-justify-center tw-flex-shrink-0"
          >
            <i :class="headerIcon" class="tw-text-3xl tw-text-gray-700" aria-hidden="true"></i>
          </div>
          <div class="tw-flex-1">
            <h1 class="tw-text-4xl tw-my-3">{{ title }}</h1>
            <p class="tw-text-[var(--color-text-organization)] tw-text-lg tw-leading-relaxed tw-max-w-3xl">
              {{ subtitle }}
            </p>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main id="main-content" class="tw-max-w-7xl tw-mx-auto tw-px-6 tw-py-12">
      <!-- Search -->
      <div class="tw-bg-white tw-rounded-2xl tw-border tw-border-gray-200 tw-shadow-sm tw-p-8 tw-mb-6">
        <div class="tw-relative">
          <i
            class="pi pi-search tw-absolute tw-left-4 tw-top-1/2 -tw-translate-y-1/2 tw-text-lg tw-text-gray-400"
            aria-hidden="true"
          ></i>
          <input
            type="search"
            :value="searchQuery"
            class="tw-w-full tw-pl-12 tw-pr-4 tw-py-3.5 !tw-border !tw-border-solid !tw-border-gray-300 tw-rounded-xl focus:tw-outline-none focus:tw-ring-2 focus:tw-ring-[var(--color-primary-organization)] focus:!tw-border-[var(--color-primary-organization)] tw-text-base tw-bg-white"
            :placeholder="searchPlaceholder"
            @input="(e) => $emit('update:searchQuery', (e.target as HTMLInputElement).value)"
            @keydown.enter="$emit('search')"
          />
        </div>
      </div>

      <!-- Filters -->
      <div
        v-if="$slots.filters"
        class="tw-bg-white tw-rounded-2xl tw-border tw-border-gray-200 tw-shadow-sm tw-p-8 tw-mb-10"
      >
        <h3 class="tw-text-lg tw-font-medium tw-mb-4 tw-mt-0">Filters</h3>
        <slot name="filters" />
      </div>

      <!-- Results count and controls -->
      <div class="tw-flex tw-items-center tw-justify-between tw-mb-6">
        <p class="tw-text-[var(--color-text-organization)]">
          <span class="tw-font-medium tw-text-[var(--color-text-organization)]">{{ totalRecords }}</span>
          {{ totalRecords === 1 ? "resultaat" : "resultaten" }} gevonden
        </p>
        <div class="tw-flex tw-items-center tw-gap-4">
          <div class="tw-flex tw-items-center tw-gap-2">
            <label class="tw-text-sm tw-text-[var(--color-text-organization)]" :for="itemsPerPageInputId">Toon:</label>
            <Dropdown
              :model-value="itemsPerPage"
              :options="itemsPerPageOptions"
              option-label="label"
              option-value="value"
              :input-id="itemsPerPageInputId"
              :pt="{ input: { class: 'tw-text-sm' }, panel: { class: 'tw-text-sm' } }"
              @update:model-value="$emit('update:itemsPerPage', $event)"
            />
          </div>
          <div class="tw-flex tw-items-center tw-gap-2">
            <label class="tw-text-sm tw-text-[var(--color-text-organization)]" :for="viewModeInputId">Weergave:</label>
            <Dropdown
              :model-value="viewMode"
              :options="viewModeOptions"
              option-label="label"
              option-value="value"
              :input-id="viewModeInputId"
              :pt="{ input: { class: 'tw-text-sm' }, panel: { class: 'tw-text-sm' } }"
              @update:model-value="$emit('update:viewMode', $event)"
            />
          </div>
        </div>
      </div>

      <Spinner v-if="loading" class="spinner" :style-type="'portal'" />

      <!-- Error State -->
      <div
        v-else-if="error"
        class="tw-bg-white tw-rounded-2xl tw-border tw-border-gray-200 tw-shadow-sm tw-p-16 tw-text-center"
      >
        <i
          class="pi pi-exclamation-triangle tw-w-16 tw-h-16 tw-text-amber-500 tw-mx-auto tw-mb-4"
          aria-hidden="true"
        ></i>
        <h3 class="tw-text-xl tw-text-[var(--color-text-organization)] tw-mb-2 tw-font-medium">Laden mislukt</h3>
        <p class="tw-text-[var(--color-text-organization)] tw-max-w-md tw-mx-auto">
          {{ error }}
        </p>
      </div>

      <!-- Results -->
      <template v-else-if="hasResults">
        <slot />

        <!-- Pagination -->
        <div class="tw-flex tw-flex-row tw-items-start tw-py-8">
          <Paginator
            class="tw-mx-auto"
            :first="(page - 1) * itemsPerPage"
            :rows="itemsPerPage"
            :total-records="totalRecords"
            :pt="{
              root: { class: '!tw-bg-transparent' },
              page: ({ context }) => ({
                class: context?.active
                  ? '!tw-bg-[var(--color-primary-organization)] !tw-text-white'
                  : 'hover:!tw-text-[var(--color-primary-organization)]',
              }),
              first: { class: 'hover:!tw-text-[var(--color-primary-organization)]' },
              prev: { class: 'hover:!tw-text-[var(--color-primary-organization)]' },
              next: { class: 'hover:!tw-text-[var(--color-primary-organization)]' },
              last: { class: 'hover:!tw-text-[var(--color-primary-organization)]' },
            }"
            @page="$emit('page', $event)"
          />
        </div>
      </template>

      <!-- Empty State -->
      <div
        v-else-if="!loading"
        class="tw-bg-white tw-rounded-2xl tw-border tw-border-gray-200 tw-shadow-sm tw-p-16 tw-text-center"
      >
        <i :class="emptyIcon" class="tw-w-16 tw-h-16 tw-text-gray-300 tw-mx-auto tw-mb-4" aria-hidden="true"></i>
        <h3 class="tw-text-xl tw-text-[var(--color-text-organization)] tw-mb-2 tw-font-medium">{{ emptyTitle }}</h3>
        <p class="tw-text-[var(--color-text-organization)] tw-max-w-md tw-mx-auto">
          {{ emptyMessage }}
        </p>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import Spinner from "@/components/Spinner.vue";
import Dropdown from "primevue/dropdown";
import Paginator from "primevue/paginator";
import { LayoutMode } from "@/portal/components/shared/portalCardShared";

export interface ItemsPerPageOption {
  label: string;
  value: number;
}

withDefaults(
  defineProps<{
    title: string;
    subtitle: string;
    headerIcon: string;
    searchPlaceholder: string;
    searchQuery: string;
    totalRecords: number;
    itemsPerPage: number;
    itemsPerPageOptions?: ItemsPerPageOption[];
    viewMode?: LayoutMode;
    page: number;
    hasResults: boolean;
    loading?: boolean;
    error?: string | null;
    emptyIcon?: string;
    emptyTitle?: string;
    emptyMessage?: string;
  }>(),
  {
    itemsPerPageOptions: () => [
      { label: "12", value: 12 },
      { label: "24", value: 24 },
      { label: "36", value: 36 },
      { label: "48", value: 48 },
    ],
    viewMode: LayoutMode.Grid,
    loading: false,
    error: null,
    emptyIcon: "pi pi-inbox",
    emptyTitle: "Geen resultaten gevonden",
    emptyMessage: "Probeer andere zoektermen of filters om resultaten te vinden.",
  },
);

const viewModeOptions = [
  { label: "Grid", value: LayoutMode.Grid },
  { label: "Lijst", value: LayoutMode.List },
];

const itemsPerPageInputId = "portal-items-per-page";
const viewModeInputId = "portal-view-mode";
defineEmits<{
  (e: "update:searchQuery", value: string): void;
  (e: "search"): void;
  (e: "update:itemsPerPage", value: number): void;
  (e: "update:viewMode", value: LayoutMode): void;
  (e: "page", value: import("primevue/paginator").PageState): void;
}>();
</script>
