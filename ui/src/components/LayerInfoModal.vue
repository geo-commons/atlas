<template>
  <Dialog
    :visible="modelValue"
    :modal="true"
    :closable="true"
    :draggable="false"
    :header="layer.title"
    :dismissable-mask="true"
    class="tw-w-[90%] md:tw-w-[70%] tw-max-w-[900px]"
    @update:visible="(value: boolean) => emit('update:modelValue', value)"
  >
    <div v-if="layer.metadataset" class="modal-content">
      <div v-if="layer.description" class="tw-mb-6">
        <h3 class="tw-m-0">Beschrijving laag</h3>
        <div class="tw-m-0 tw-whitespace-pre-wrap tw-leading-relaxed">
          <markdown :source="layer.description" />
        </div>
      </div>

      <div v-if="layer.metadataset?.abstract" class="tw-mb-6">
        <h3 class="tw-m-0">Over deze dataset</h3>
        <p class="tw-m-0 tw-whitespace-pre-wrap tw-leading-relaxed">{{ layer.metadataset?.abstract }}</p>
      </div>

      <div v-if="layer.metadataset?.description && isLoggedIn" class="tw-mb-6">
        <h3 class="tw-m-0">Beschrijving <VisibilityIndicator visibility="Intern" /></h3>
        <p class="tw-m-0 tw-whitespace-pre-wrap tw-leading-relaxed">{{ layer.metadataset?.description }}</p>
      </div>

      <div class="tw-grid tw-grid-cols-1 lg:tw-grid-cols-12 lg:tw-gap-10">
        <div class="lg:tw-col-span-7">
          <div v-for="section in tableData" v-show="section.show" :key="section.title" class="tw-mb-8">
            <h3 class="tw-m-0">{{ section.title }}</h3>
            <table class="tw-border-collapse">
              <tbody>
                <tr v-for="row in section.rows" v-show="row.show" :key="row.label" class="">
                  <td
                    class="tw-text-gray-600 tw-pr-3 lg:tw-pr-8 tw-w-[12rem] tw-min-w-[12rem] lg:tw-w-[18rem] lg:tw-min-w-[18rem] tw-py-3 tw-px-1"
                  >
                    {{ row.label }}
                    <VisibilityIndicator v-if="row.hasVisibilityIndicator" visibility="Intern" />
                  </td>
                  <td class="tw-py-3 tw-px-1">
                    <!-- Keywords type -->
                    <div v-if="row.type === 'keywords' && row.value" class="tw-flex tw-flex-wrap tw-gap-2">
                      <span
                        v-for="keyword in row.value.split('\n').filter((k: string) => k.trim())"
                        :key="keyword"
                        class="tw-bg-gray-100 tw-text-gray-800 tw-px-2 tw-py-1 tw-rounded tw-text-sm tw-border tw-border-gray-300"
                      >
                        {{ keyword.trim() }}
                      </span>
                    </div>
                    <!-- Email type -->
                    <a
                      v-else-if="row.type === 'email' && row.value"
                      class="tw-text-blue-600 tw-no-underline hover:tw-underline"
                      :href="`mailto:${row.value.toLowerCase()}`"
                    >
                      {{ row.value.toLowerCase() }}
                    </a>
                    <!-- Text type -->
                    <span v-else-if="row.value">{{ row.value }}</span>
                    <span v-else>N/A</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </Dialog>
</template>

<script setup lang="ts">
import VisibilityIndicator from "@/components/VisibilityIndicator.vue";
import { accessConstraintsTypeOptions } from "@/types/AccessConstraintsType";
import { otherConstraintsTypeOptions } from "@/types/OtherConstraintsType";
import { roleTypeLabels, type RoleTypeId } from "@/types/RoleType";
import { topicCategoryLabels, type TopicCategoryId } from "@/types/TopicCategory";
import { updateMethodTypeLabels, type UpdateMethodTypeId } from "@/types/UpdateMethodType";
import { formatDateValue } from "@/utils/date-formatter";
import { computed } from "vue";
import type { LayerInfoLayer } from "./LayerInfo.vue";
import Markdown from "./Markdown";

interface Props {
  modelValue: boolean;
  layer: LayerInfoLayer;
  isLoggedIn?: boolean;
}

const props = defineProps<Props>();

const emit = defineEmits<{
  (e: "update:modelValue", value: boolean): void;
}>();

const getTopicCategoryLabel = (topicId?: string): string => {
  if (!topicId) return "";
  return (topicId in topicCategoryLabels ? topicCategoryLabels[topicId as TopicCategoryId] : topicId) || "";
};

const getRoleTypeLabel = (roleId?: string): string => {
  if (!roleId) return "";
  return (roleId in roleTypeLabels ? roleTypeLabels[roleId as RoleTypeId] : roleId) || "";
};

const getAccessConstraintsLabel = (constraintId?: string): string => {
  if (!constraintId) return "";
  return accessConstraintsTypeOptions.find((option) => option.id === constraintId)?.label || constraintId;
};

const getOtherConstraintsLabel = (constraintId?: string): string => {
  if (!constraintId) return "";
  return otherConstraintsTypeOptions.find((option) => option.id === constraintId)?.label || constraintId;
};

const getUpdateMethodLabel = (updateMethodId?: string): string => {
  if (!updateMethodId) return "";
  return (
    (updateMethodId in updateMethodTypeLabels
      ? updateMethodTypeLabels[updateMethodId as UpdateMethodTypeId]
      : updateMethodId) || ""
  );
};

const hasSourceInfo = computed(() => {
  const md = props.layer.metadataset;
  return !!(
    md?.source_origin ||
    md?.source_organization ||
    md?.source_email_public ||
    md?.source_role_person_responsible ||
    md?.source_location ||
    md?.source_email_internal ||
    md?.source_name_internal ||
    md?.source_name_public
  );
});

const hasConstraintsInfo = computed(() => {
  const md = props.layer.metadataset;
  return !!(md?.access_constraints || md?.other_constraints || md?.usage_constraints);
});

const hasMetadataResponsibleInfo = computed(() => {
  const md = props.layer.metadataset;
  return !!(
    md?.meta_organization ||
    md?.meta_email_person_responsible ||
    md?.meta_role_person_responsible ||
    md?.meta_email_internal
  );
});

const tableData = computed(() => {
  const md = props.layer.metadataset;
  return [
    {
      title: "Algemene informatie",
      show: true,
      rows: [
        {
          label: "Onderwerp",
          value: getTopicCategoryLabel(md?.topic_category),
          show: !!md?.topic_category,
          type: "text",
        },
        {
          label: "Trefwoorden",
          value: md?.keyword || "",
          show: !!md?.keyword,
          type: "keywords",
        },
        {
          label: "Doel van de vervaardiging",
          value: md?.statement || "",
          show: !!md?.statement,
          type: "text",
        },
        {
          label: "Laatste update",
          value: md?.last_updated ? formatDateValue(md.last_updated) : "",
          show: !!md?.last_updated,
          type: "text",
        },
        {
          label: "Updatefrequentie",
          value: md?.update_frequency || "",
          show: !!md?.update_frequency,
          type: "text",
        },
        {
          label: "Updatemethode",
          value: getUpdateMethodLabel(md?.update_method),
          show: !!md?.update_method,
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
          value: md?.source_origin || "",
          show: !!md?.source_origin,
          type: "text",
        },
        {
          label: "Verantwoordelijke organisatie",
          value: md?.source_organization || "",
          show: !!md?.source_organization,
          type: "text",
        },
        {
          label: "Naam contactpersoon verantwoordelijke",
          value: md?.source_name_public || "",
          show: !!md?.source_name_public,
          type: "text",
        },
        {
          label: "E-mailadres verantwoordelijke",
          value: md?.source_email_public || "",
          show: !!md?.source_email_public,
          type: "email",
        },
        {
          label: "Rol verantwoordelijke",
          value: getRoleTypeLabel(md?.source_role_person_responsible),
          show: !!md?.source_role_person_responsible,
          type: "text",
        },
        {
          label: "Bronlocatie",
          value: md?.source_location || "",
          show: !!md?.source_location,
          type: "text",
          hasVisibilityIndicator: true,
        },
        {
          label: "Naam contactpersoon aanspreekpunt",
          value: md?.source_name_internal || "",
          show: !!md?.source_name_internal,
          type: "text",
          hasVisibilityIndicator: true,
        },
        {
          label: "E-mailadres aanspreekpunt",
          value: md?.source_email_internal || "",
          show: !!md?.source_email_internal,
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
          value: getAccessConstraintsLabel(md?.access_constraints),
          show: !!md?.access_constraints,
          type: "text",
        },
        {
          label: "Overige beperkingen",
          value: getOtherConstraintsLabel(md?.other_constraints),
          show: !!(md?.other_constraints && md?.access_constraints === "otherRestrictions"),
          type: "text",
        },
        {
          label: "Gebruiksbeperkingen",
          value: md?.usage_constraints || "",
          show: !!md?.usage_constraints,
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
          value: md?.meta_organization || "",
          show: !!md?.meta_organization,
          type: "text",
        },
        {
          label: "E-mailadres verantwoordelijke",
          value: md?.meta_email_person_responsible || "",
          show: !!md?.meta_email_person_responsible,
          type: "email",
        },
        {
          label: "Rol verantwoordelijke",
          value: getRoleTypeLabel(md?.meta_role_person_responsible),
          show: !!md?.meta_role_person_responsible,
          type: "text",
        },
        {
          label: "E-mailadres aanspreekpunt",
          value: md?.meta_email_internal || "",
          show: !!md?.meta_email_internal,
          type: "email",
          hasVisibilityIndicator: true,
        },
      ],
    },
  ];
});
</script>

<style scoped>
.modal-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

table tbody tr:not(:last-child) td {
  border-bottom: 1px solid;
  @apply tw-border-gray-300;
}
</style>
