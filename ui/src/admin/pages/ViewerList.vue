<script setup lang="ts">
import AdminListView, { DialogTypes } from "@/admin/components/AdminListView.vue";
import { onMounted, Ref, ref, unref } from "vue";
import { TableHeader } from "@/admin/components/AdminListViewTable.vue";
import { TableFilter } from "@/admin/components/AdminListViewFilter.vue";
import { useRouter } from "vue-router";

const router = useRouter();

const childRef: Ref<null | {
  toggleDialog: (type: DialogTypes) => void;
}> = ref(null);

const viewers: Ref<Array<object>> = ref([]);
const loading: Ref<boolean> = ref(true);

const tableHeaders: Array<TableHeader> = [
  {
    header: "Titel",
    key: "title",
    enableLink: true,
  },
];

const initialViewerData = {
  title: "",
  url: "",
  authenticate: false,
};

const getViewers = async (params?: URLSearchParams): Promise<{ results: Array<object>; count: number }> => {
  const url = new URL("/atlas/api/v1/viewers/", window.location.origin);

  if (params) {
    url.search = params.toString();
  }

  const result = await fetch(url.toString(), {
    credentials: "same-origin",
    headers: { "Content-Type": "application/json" },
  });

  if (!result.ok) {
    console.error("Could not fetch viewers");
  }

  const items = await result.json();

  return items;
};

const getCreateViewerSections = () => {
  return {
    general: {
      label: "Algemene gegevens",
      questions: [
        {
          label: "Label",
          id: "label",
          name: "Label",
          type: "text",
          required: true,
        },
      ],
    },
  };
};

const saveViewer = async (
  currentValues: any,
  continueEditing = false,
  sendSaveRequest: (apiUrl: string, method: string, currentValues: object) => Response,
) => {
  const url = "/atlas/api/v1/viewers/";

  try {
    const result = await sendSaveRequest(url, "POST", currentValues);

    if (result.ok) {
      childRef?.value?.toggleDialog("create-object-dialog");

      if (continueEditing) {
        const response = await result.json();
        await router.push(`/viewers/update/${response.id}`);
      }
    }
  } catch (e) {
    console.error("An unexpected error occurred:", e);
  }
};

// onMounted
onMounted(() => {
  Promise.all([getViewers()]).then((result) => {
    viewers.value = result[0].results;
    loading.value = false;
  });
});
</script>

<template>
  <AdminListView
    ref="childRef"
    :loading="loading"
    singular-name="Viewer"
    plural-name="Viewers"
    api-name="viewers"
    :get-create-object-dialog-sections="getCreateViewerSections"
    :initial-create-object-dialog-data="initialViewerData"
    :save-create-object-dialog-data="saveViewer"
    :get-objects="getViewers"
    :table-headers="tableHeaders"
  />
</template>
