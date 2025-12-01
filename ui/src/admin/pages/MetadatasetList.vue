<script setup lang="ts">
import AdminListView from "@/admin/components/AdminListView.vue";
import { TableFilter } from "@/admin/components/AdminListViewFilter.vue";
import { TableHeader } from "@/admin/components/AdminListViewTable.vue";
import { EDialogTypes } from "@/types/dialog";
import slugify from "slugify";
import { onMounted, ref, Ref } from "vue";
import { useRouter } from "vue-router";
import { statusTypeLabels, statusTypeOptions, topicCategoryLabels, topicCategoryOptions } from "@/types";
import { IMetadataset } from "@/types/metadataset";

const router = useRouter();

const loading: Ref<boolean> = ref(true);

const childRef: Ref<null | {
  toggleDialog: (type: EDialogTypes) => void;
}> = ref(null);

const getMetadatasets = async (params?: URLSearchParams): Promise<{ results: Array<object>; count: number }> => {
  const url = new URL("/atlas/api/v1/metadatasets/", window.location.origin);

  if (params) {
    url.search = params.toString();
  }

  const result = await fetch(url.toString(), {
    credentials: "same-origin",
    headers: { "Content-Type": "application/json" },
  });

  if (!result.ok) {
    console.error("Could not fetch metadatasets");
  }

  const items = await result.json();

  return items;
};

const saveMetadataset = async (
  currentValues: any,
  continueEditing = false,
  sendSaveRequest: (apiUrl: string, method: string, currentValues: object) => Response,
) => {
  const url = "/atlas/api/v1/metadatasets/";

  const payload: Partial<IMetadataset> = {
    ...currentValues,
    slug: slugify(currentValues.title, { lower: true, strict: true }),
  };

  try {
    const result = await sendSaveRequest(url, "POST", payload);

    if (result.ok) {
      childRef?.value?.toggleDialog(EDialogTypes.Create);

      if (continueEditing) {
        const response = await result.json();
        await router.push(`/metadatasets/update/${response.id}`);
      }
    }
  } catch (e) {
    console.error("An unexpected error occurred:", e);
  }
};

const getCreateMetadatasetSections = () => {
  return {
    general: {
      label: "Algemene gegevens",
      questions: [
        {
          label: "Titel",
          id: "title",
          name: "Title",
          type: "text",
          required: true,
          visibility: "Publiek",
        },
        {
          label: "Beschrijving",
          id: "description",
          name: "Description",
          type: "text",
          required: false,
          multiLine: true,
          visibility: "Intern",
        },
      ],
    },
  };
};

const initialCreateMetadatasetData = {
  title: "",
  status: "underDevelopment",
  last_updated: null,
  update_method: "manual",
};

const tableHeaders: Array<TableHeader> = [
  {
    header: "Titel",
    key: "title",
    enableLink: true,
  },
  {
    header: "Onderwerp",
    key: "topic_category",
    mapValues: topicCategoryLabels,
    enableLink: false,
  },
  {
    header: "Status",
    key: "status",
    enableLink: false,
    mapValues: statusTypeLabels,
  },
  {
    header: "Tonen op portal",
    key: "show_in_overview",
    enableLink: false,
  },
];

const getTableFilters = (): Array<TableFilter> => {
  return [
    {
      name: "Selecteer onderwerp",
      key: "topic_category",
      label: "label",
      dataKey: "id",
      options: topicCategoryOptions,
    },
    {
      name: "Selecteer status",
      key: "status",
      label: "label",
      dataKey: "id",
      options: statusTypeOptions,
    },
  ];
};

// onMounted
onMounted(() => {
  Promise.all([getMetadatasets()]).then(() => {
    loading.value = false;
  });
});
</script>

<template>
  <AdminListView
    ref="childRef"
    :loading="loading"
    singular-name="Metadataset"
    plural-name="Metadatasets"
    api-name="metadatasets"
    :get-create-object-dialog-sections="getCreateMetadatasetSections"
    :initial-create-object-dialog-data="initialCreateMetadatasetData"
    :save-create-object-dialog-data="saveMetadataset"
    :get-objects="getMetadatasets"
    :enable-import-export="true"
    :enable-delete-multiple="true"
    :enable-duplicate="true"
    :table-headers="tableHeaders"
    :get-table-filters="getTableFilters"
  />
</template>
