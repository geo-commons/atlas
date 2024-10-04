<script setup lang="ts">
import AdminListView, { DialogTypes } from "@/admin/components/AdminListView.vue";
import { onMounted, ref, Ref } from "vue";
import { TableHeader } from "@/admin/components/AdminListViewTable.vue";
import slugify from "slugify";
import { useRouter } from "vue-router";

const router = useRouter();

const loading: Ref<boolean> = ref(true);

const childRef: Ref<null | {
  toggleDialog: (type: DialogTypes) => void;
}> = ref(null);

const getDatasets = async (params?: URLSearchParams): Promise<{ results: Array<object>; count: number }> => {
  const url = new URL("/atlas/api/v1/datasets/", window.location.origin);

  if (params) {
    url.search = params.toString();
  }

  const result = await fetch(url.toString(), {
    credentials: "same-origin",
    headers: { "Content-Type": "application/json" },
  });

  if (!result.ok) {
    console.error("Could not fetch datasets");
  }

  const items = await result.json();

  return items;
};

const saveDataset = async (
  currentValues: any,
  continueEditing = false,
  sendSaveRequest: (apiUrl: string, method: string, currentValues: object) => Response,
) => {
  const url = "/atlas/api/v1/datasets/";

  currentValues.themes = [];
  currentValues.slug = slugify(currentValues.title);

  try {
    const result = await sendSaveRequest(url, "POST", currentValues);

    if (result.ok) {
      childRef?.value?.toggleDialog("create-object-dialog");

      if (continueEditing) {
        const response = await result.json();
        await router.push(`/datasets/update/${response.id}`);
      }
    }
  } catch (e) {
    console.error("An unexpected error occurred:", e);
  }
};

const getCreateDatasetSections = () => {
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
        },
      ],
    },
  };
};

const initialCreateDatasetData = {
  title: "",
};

const tableHeaders: Array<TableHeader> = [
  {
    header: "Titel",
    key: "title",
    enableLink: true,
  },
];

// onMounted
onMounted(() => {
  Promise.all([getDatasets()]).then((result) => {
    loading.value = false;
  });
});
</script>

<template>
  <AdminListView
    ref="childRef"
    :loading="loading"
    singular-name="Dataset"
    plural-name="Datasets"
    api-name="datasets"
    :get-create-object-dialog-sections="getCreateDatasetSections"
    :initial-create-object-dialog-data="initialCreateDatasetData"
    :save-create-object-dialog-data="saveDataset"
    :get-objects="getDatasets"
    :table-headers="tableHeaders"
  />
</template>
