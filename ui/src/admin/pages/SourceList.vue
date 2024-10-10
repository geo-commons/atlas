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

const sources: Ref<Array<object>> = ref([]);
const loading: Ref<boolean> = ref(true);

const tableHeaders: Array<TableHeader> = [
  {
    header: "Titel",
    key: "title",
    enableLink: true,
  },
];

const initialSourceData = {
  title: "",
  url: "",
  authenticate: false,
};

const getSources = async (params?: URLSearchParams): Promise<{ results: Array<object>; count: number }> => {
  const url = new URL("/atlas/api/v1/sources/", window.location.origin);

  if (params) {
    url.search = params.toString();
  }

  const result = await fetch(url.toString(), {
    credentials: "same-origin",
    headers: { "Content-Type": "application/json" },
  });

  if (!result.ok) {
    console.error("Could not fetch sources");
  }

  const items = await result.json();

  return items;
};

const getCreateSourceSections = () => {
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
        {
          label: "Kort kenmerk",
          id: "slug",
          name: "Slug",
          type: "text",
          required: false,
          infoText: "Een uniek kort kenmerk voor de bron in Atlas.",
        },
        {
          label: "URL",
          id: "url",
          name: "Url",
          type: "url",
          required: true,
        },
      ],
    },
  };
};

const saveSource = async (
  currentValues: any,
  continueEditing = false,
  sendSaveRequest: (apiUrl: string, method: string, currentValues: object) => Response,
) => {
  const url = "/atlas/api/v1/sources/";

  try {
    const result = await sendSaveRequest(url, "POST", currentValues);

    if (result.ok) {
      childRef?.value?.toggleDialog(EDialogTypes.Create);

      if (continueEditing) {
        const response = await result.json();
        await router.push(`/sources/update/${response.id}`);
      }
    }
  } catch (e) {
    console.error("An unexpected error occurred:", e);
  }
};

// onMounted
onMounted(() => {
  Promise.all([getSources()]).then((result) => {
    sources.value = result[0].results;
    loading.value = false;
  });
});
</script>

<template>
  <AdminListView
    ref="childRef"
    :loading="loading"
    singular-name="Bron"
    plural-name="Bronnen"
    api-name="sources"
    :get-create-object-dialog-sections="getCreateSourceSections"
    :initial-create-object-dialog-data="initialSourceData"
    :save-create-object-dialog-data="saveSource"
    :get-objects="getSources"
    :table-headers="tableHeaders"
  />
</template>
