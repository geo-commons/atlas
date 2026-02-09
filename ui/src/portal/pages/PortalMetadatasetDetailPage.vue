<template>
  <div class="tw-min-h-screen tw-bg-gray-50">
    <div v-if="loading" class="tw-flex tw-justify-center tw-items-center tw-min-h-[60vh]">
      <Spinner class="spinner" :style-type="'portal'" />
    </div>
    <div v-else-if="error" class="tw-flex tw-justify-center tw-items-center tw-min-h-[60vh]">
      <div class="tw-text-center">
        <p class="tw-text-gray-600 tw-text-lg">{{ error }}</p>
      </div>
    </div>
    <div v-else>
      <header class="tw-bg-white tw-border-b tw-border-gray-200 tw-border-solid tw-border-0">
        <div class="tw-max-w-7xl tw-mx-auto tw-px-6 tw-py-12">
          <div class="tw-flex tw-items-start tw-gap-4 tw-mb-4">
            <div
              class="tw-w-16 tw-h-16 tw-bg-gray-50 tw-rounded-2xl tw-flex tw-items-center tw-justify-center tw-flex-shrink-0"
            >
              <i class="pi pi-database tw-text-2xl tw-text-gray-700" aria-hidden="true"></i>
            </div>
            <div class="tw-flex-1">
              <h1 class="tw-text-4xl tw-my-3">{{ metadataset?.title }}</h1>
              <p v-if="metadataset?.abstract" class="tw-text-gray-600 tw-text-lg tw-leading-relaxed tw-max-w-3xl">
                {{ metadataset?.abstract }}
              </p>
            </div>
          </div>
        </div>
      </header>

      <main class="tw-max-w-7xl tw-mx-auto tw-px-6 tw-py-10 tw-space-y-6">
        <section
          v-if="metadataset?.description"
          class="tw-bg-white tw-rounded-2xl tw-border tw-border-gray-200 tw-shadow-sm tw-p-6"
        >
          <h2 class="tw-text-xl tw-mb-3">
            Beschrijving
            <VisibilityIndicator visibility="Intern" />
          </h2>
          <p class="tw-m-0 tw-whitespace-pre-wrap tw-leading-relaxed tw-text-gray-700">
            {{ metadataset?.description }}
          </p>
        </section>

        <section class="tw-space-y-6">
          <div
            v-for="section in tableData"
            v-show="section.show"
            :key="section.title"
            class="tw-bg-white tw-rounded-2xl tw-border tw-border-gray-200 tw-shadow-sm tw-p-6"
          >
            <h2 class="tw-text-xl tw-mb-4">{{ section.title }}</h2>
            <table class="tw-w-full tw-border-collapse">
              <tbody class="tw-divide-y tw-divide-gray-200">
                <tr v-for="row in section.rows" v-show="row.show" :key="row.label">
                  <td class="tw-text-gray-600 tw-pr-4 tw-py-3 tw-w-[12rem] lg:tw-w-[16rem] tw-align-top">
                    <div class="tw-flex tw-items-center tw-gap-2">
                      <span>{{ row.label }}</span>
                      <VisibilityIndicator v-if="row.hasVisibilityIndicator" visibility="Intern" />
                    </div>
                  </td>
                  <td class="tw-py-3 tw-text-gray-800">
                    <!-- Keywords type -->
                    <div v-if="row.type === 'keywords' && row.value" class="tw-flex tw-flex-wrap tw-gap-2">
                      <span
                        v-for="keyword in row.value.split('\n').filter((k) => k.trim())"
                        :key="keyword"
                        class="tw-bg-gray-100 tw-text-gray-800 tw-px-2 tw-py-1 tw-rounded-lg tw-text-sm tw-border tw-border-gray-200"
                      >
                        {{ keyword.trim() }}
                      </span>
                    </div>
                    <!-- Email type -->
                    <a
                      v-else-if="row.type === 'email' && row.value"
                      class="tw-text-[var(--color-primary-organization)] tw-no-underline hover:tw-underline"
                      :href="`mailto:${row.value.toLowerCase()}`"
                    >
                      {{ row.value.toLowerCase() }}
                    </a>
                    <!-- Text type -->
                    <span v-else-if="row.value">{{ row.value }}</span>
                    <span v-else class="tw-text-gray-400">N/A</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import Spinner from "@/components/Spinner.vue";
import VisibilityIndicator from "@/components/VisibilityIndicator.vue";
import type {
  AccessConstraintsTypeId,
  OtherConstraintsTypeId,
  RoleTypeId,
  TopicCategoryId,
  UpdateMethodTypeId,
} from "@/types";
import { accessConstraintsTypeOptions } from "@/types/AccessConstraintsType";
import { IMetadataset } from "@/types/metadataset";
import { otherConstraintsTypeOptions } from "@/types/OtherConstraintsType";
import { roleTypeLabels } from "@/types/RoleType";
import { topicCategoryLabels } from "@/types/TopicCategory";
import { updateMethodTypeLabels } from "@/types/UpdateMethodType";
import { formatDateValue } from "@/utils/date-formatter";
import { computed, onMounted, ref } from "vue";
import { useRoute } from "vue-router";

interface TableRow {
  label: string;
  value: string;
  show: boolean;
  type: "text" | "keywords" | "email";
  hasVisibilityIndicator?: boolean;
}

interface TableSection {
  title: string;
  show: boolean;
  rows: TableRow[];
}

const route = useRoute();
const loading = ref<boolean>(false);
const metadataset = ref<IMetadataset | null>(null);
const error = ref<string | null>(null);

const hasSourceInfo = computed(() => {
  return !!(
    metadataset.value?.source_origin ||
    metadataset.value?.source_organization ||
    metadataset.value?.source_email_public ||
    metadataset.value?.source_role_person_responsible ||
    metadataset.value?.source_location ||
    metadataset.value?.source_email_internal ||
    metadataset.value?.source_name_internal ||
    metadataset.value?.source_name_public
  );
});

const hasConstraintsInfo = computed(() => {
  return !!(
    metadataset.value?.access_constraints ||
    metadataset.value?.other_constraints ||
    metadataset.value?.usage_constraints
  );
});

const hasMetadataResponsibleInfo = computed(() => {
  return !!(
    metadataset.value?.meta_organization ||
    metadataset.value?.meta_email_person_responsible ||
    metadataset.value?.meta_role_person_responsible ||
    metadataset.value?.meta_email_internal
  );
});

const tableData = computed<TableSection[]>(() => {
  return [
    {
      title: "Algemene informatie",
      show: true,
      rows: [
        {
          label: "Onderwerp",
          value: getTopicCategoryLabel(metadataset.value?.topic_category as TopicCategoryId),
          show: !!metadataset.value?.topic_category,
          type: "text",
        },
        {
          label: "Trefwoorden",
          value: metadataset.value?.keyword || "",
          show: !!metadataset.value?.keyword,
          type: "keywords",
        },
        {
          label: "Doel van de vervaardiging",
          value: metadataset.value?.statement || "",
          show: !!metadataset.value?.statement,
          type: "text",
        },
        {
          label: "Laatste update",
          value: metadataset.value?.last_updated ? formatDateValue(metadataset.value.last_updated) : "",
          show: !!metadataset.value?.last_updated,
          type: "text",
        },
        {
          label: "Updatefrequentie",
          value: metadataset.value?.update_frequency || "",
          show: !!metadataset.value?.update_frequency,
          type: "text",
        },
        {
          label: "Updatemethode",
          value: getUpdateMethodLabel(metadataset.value?.update_method as UpdateMethodTypeId),
          show: !!metadataset.value?.update_method,
          type: "text",
          hasVisibilityIndicator: true,
        },
      ],
    },
    {
      title: "Broninformatie",
      show: hasSourceInfo.value,
      rows: [
        {
          label: "Oorspronkelijke bron",
          value: metadataset.value?.source_origin || "",
          show: !!metadataset.value?.source_origin,
          type: "text",
        },
        {
          label: "Verantwoordelijke organisatie",
          value: metadataset.value?.source_organization || "",
          show: !!metadataset.value?.source_organization,
          type: "text",
        },
        {
          label: "Naam contactpersoon verantwoordelijke",
          value: metadataset.value?.source_name_public || "",
          show: !!metadataset.value?.source_name_public,
          type: "text",
        },
        {
          label: "E-mailadres verantwoordelijke",
          value: metadataset.value?.source_email_public || "",
          show: !!metadataset.value?.source_email_public,
          type: "email",
        },
        {
          label: "Rol verantwoordelijke",
          value: getRoleTypeLabel(metadataset.value?.source_role_person_responsible as RoleTypeId),
          show: !!metadataset.value?.source_role_person_responsible,
          type: "text",
        },
        {
          label: "Bronlocatie",
          value: metadataset.value?.source_location || "",
          show: !!metadataset.value?.source_location,
          type: "text",
          hasVisibilityIndicator: true,
        },
        {
          label: "Naam contactpersoon aanspreekpunt",
          value: metadataset.value?.source_name_internal || "",
          show: !!metadataset.value?.source_name_internal,
          type: "text",
          hasVisibilityIndicator: true,
        },
        {
          label: "E-mailadres aanspreekpunt",
          value: metadataset.value?.source_email_internal || "",
          show: !!metadataset.value?.source_email_internal,
          type: "email",
          hasVisibilityIndicator: true,
        },
      ],
    },
    {
      title: "Beperkingen",
      show: hasConstraintsInfo.value,
      rows: [
        {
          label: "Juridische toegangsrestricties",
          value: getAccessConstraintsLabel(metadataset.value?.access_constraints as AccessConstraintsTypeId),
          show: !!metadataset.value?.access_constraints,
          type: "text",
        },
        {
          label: "Overige beperkingen",
          value: getOtherConstraintsLabel(metadataset.value?.other_constraints as OtherConstraintsTypeId),
          show: !!(
            metadataset.value?.other_constraints && metadataset.value?.access_constraints === "otherRestrictions"
          ),
          type: "text",
        },
        {
          label: "Gebruiksbeperkingen",
          value: metadataset.value?.usage_constraints || "",
          show: !!metadataset.value?.usage_constraints,
          type: "text",
        },
      ],
    },
    {
      title: "Verantwoordelijke metadata",
      show: hasMetadataResponsibleInfo.value,
      rows: [
        {
          label: "Organisatie",
          value: metadataset.value?.meta_organization || "",
          show: !!metadataset.value?.meta_organization,
          type: "text",
        },
        {
          label: "E-mailadres verantwoordelijke",
          value: metadataset.value?.meta_email_person_responsible || "",
          show: !!metadataset.value?.meta_email_person_responsible,
          type: "email",
        },
        {
          label: "Rol verantwoordelijke",
          value: getRoleTypeLabel(metadataset.value?.meta_role_person_responsible as RoleTypeId),
          show: !!metadataset.value?.meta_role_person_responsible,
          type: "text",
        },
        {
          label: "E-mailadres aanspreekpunt",
          value: metadataset.value?.meta_email_internal || "",
          show: !!metadataset.value?.meta_email_internal,
          type: "email",
          hasVisibilityIndicator: true,
        },
      ],
    },
  ];
});

const getTopicCategoryLabel = (topicId?: TopicCategoryId): string => {
  return topicId ? topicCategoryLabels[topicId] || topicId : "";
};

const getRoleTypeLabel = (roleId?: RoleTypeId): string => {
  return roleId ? roleTypeLabels[roleId] || roleId : "";
};

const getAccessConstraintsLabel = (constraintId?: AccessConstraintsTypeId): string => {
  return constraintId
    ? accessConstraintsTypeOptions.find((option) => option.id === constraintId)?.label || constraintId
    : "";
};

const getOtherConstraintsLabel = (constraintId?: OtherConstraintsTypeId): string => {
  return constraintId
    ? otherConstraintsTypeOptions.find((option) => option.id === constraintId)?.label || constraintId
    : "";
};

const getUpdateMethodLabel = (updateMethodId?: UpdateMethodTypeId): string => {
  return updateMethodId ? updateMethodTypeLabels[updateMethodId] || updateMethodId : "";
};

const getMetadataset = async (): Promise<void> => {
  loading.value = true;

  const slug = route.params.slug as string;

  if (!slug) {
    console.error("No valid slug");
    error.value = "Geen geldige metadataset gevonden.";
    loading.value = false;
    return;
  }

  try {
    const result = await fetch(`/atlas/api/v1/metadatasets/${slug}/`, {
      credentials: "same-origin",
      headers: { "Content-Type": "application/json" },
    });

    if (!result.ok) {
      console.error("Could not fetch metadataset");
      error.value = "Er is een probleem opgetreden bij het laden van de metadataset. Probeer het opnieuw.";
    } else {
      metadataset.value = await result.json();
    }
  } catch (err) {
    console.error("Error fetching metadataset:", err);
    error.value = "Er is een probleem opgetreden bij het laden van de metadataset. Probeer het opnieuw.";
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  getMetadataset();
});
</script>

<style scoped></style>
