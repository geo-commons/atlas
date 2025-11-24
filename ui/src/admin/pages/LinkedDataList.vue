<script setup lang="ts">
import AdminListView from "@/admin/components/AdminListView.vue";
import { onMounted, Ref, ref } from "vue";
import { TableHeader } from "@/admin/components/AdminListViewTable.vue";
import { useRouter } from "vue-router";
import { EDialogTypes } from "@/types/dialog";

const router = useRouter();

const childRef: Ref<null | {
  toggleDialog: (type: EDialogTypes) => void;
}> = ref(null);

const linkedData: Ref<Array<object>> = ref([]);
const loading: Ref<boolean> = ref(true);

const tableHeaders: Array<TableHeader> = [
  {
    header: "Titel",
    key: "title",
    enableLink: true,
  },
];

const initialThemeData = {
  title: "",
  authenticate: false,
};

const getLinkedData = async (params?: URLSearchParams): Promise<{ results: Array<object>; count: number }> => {
  const url = new URL("/atlas/api/v1/linked-data/", window.location.origin);

  if (params) {
    url.search = params.toString();
  }

  const result = await fetch(url.toString(), {
    credentials: "same-origin",
    headers: { "Content-Type": "application/json" },
  });

  if (!result.ok) {
    console.error("Could not fetch linked data");
  }

  const items = await result.json();

  return items;
};

const getCreateThemeSections = () => {
  return {
    general: {
      label: "Algemene gegevens",
      questions: [
        {
          label: "Naam",
          id: "title",
          name: "Title",
          type: "text",
          required: true,
        },
      ],
    },
  };
};

const saveLinkedData = async (
  currentValues: any,
  continueEditing = false,
  sendSaveRequest: (apiUrl: string, method: string, currentValues: object) => Response,
) => {
  const url = "/atlas/api/v1/linked-data/";

  currentValues.datasets = [];

  try {
    const result = await sendSaveRequest(url, "POST", currentValues);

    if (result.ok) {
      childRef?.value?.toggleDialog(EDialogTypes.Create);

      if (continueEditing) {
        const response = await result.json();
        await router.push(`/linked-data/update/${response.id}`);
      }
    }
  } catch (e) {
    console.error("An unexpected error occurred:", e);
  }
};

// onMounted
onMounted(() => {
  Promise.all([getLinkedData()]).then((result) => {
    linkedData.value = result[0].results;
    loading.value = false;
  });
});
</script>

<template>
  <AdminListView
    ref="childRef"
    :loading="loading"
    singular-name="Gerelateerde data"
    plural-name="Gerelateerde data"
    api-name="linked-data"
    :get-create-object-dialog-sections="getCreateThemeSections"
    :enable-import-export="true"
    :enable-delete-multiple="true"
    :initial-create-object-dialog-data="initialThemeData"
    :save-create-object-dialog-data="saveLinkedData"
    :get-objects="getLinkedData"
    :table-headers="tableHeaders"
  />
</template>
