<script setup lang="ts">
import AdminListView from "@/admin/components/AdminListView.vue";
import { onMounted, ref, Ref } from "vue";
import { TableHeader } from "@/admin/components/AdminListViewTable.vue";
import { useRouter } from "vue-router";
import { EDialogTypes } from "@/types/dialog";
import { getAllObjects } from "@/utils/api-helpers";

const router = useRouter();

const loading: Ref<boolean> = ref(true);

const childRef: Ref<null | {
  toggleDialog: (type: EDialogTypes) => void;
}> = ref(null);

const sources: Ref<Array<object>> = ref([]);

const getTables = async (params?: URLSearchParams): Promise<{ results: Array<object>; count: number }> => {
  const url = new URL("/atlas/api/v1/tables/", window.location.origin);

  if (params) {
    url.search = params.toString();
  }

  const result = await fetch(url.toString(), {
    credentials: "same-origin",
    headers: { "Content-Type": "application/json" },
  });

  if (!result.ok) {
    console.error("Could not fetch tables");
  }

  const items = await result.json();

  return items;
};

const getSources = async () => {
  const url = getAllObjects("/atlas/api/v1/sources/");
  const result = await fetch(url, {
    credentials: "same-origin",
    headers: { "Content-Type": "application/json" },
  });

  if (!result.ok) {
    console.error("Could not fetch sources");
  }

  const response = await result.json();

  return response.results.map((source: any) => {
    return { id: source.id, label: source.title };
  });
};

const saveTable = async (
  currentValues: any,
  continueEditing = false,
  sendSaveRequest: (apiUrl: string, method: string, currentValues: object) => Response,
) => {
  const url = "/atlas/api/v1/tables/";

  currentValues.method = "GET";
  currentValues.endpoint = "/";

  try {
    const result = await sendSaveRequest(url, "POST", currentValues);

    if (result.ok) {
      childRef?.value?.toggleDialog(EDialogTypes.Create);

      if (continueEditing) {
        const response = await result.json();
        await router.push(`/tables/update/${response.id}`);
      }
    }
  } catch (e) {
    console.error("An unexpected error occurred:", e);
  }
};

const getCreateTableSections = () => {
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
          required: true,
        },
        {
          label: "Bron",
          id: "source",
          name: "Source",
          type: "dropdown",
          required: true,
          placeholder: "bron",
          options: sources,
        },
      ],
    },
  };
};

const initialCreateTableData = {
  title: "",
  authenticate: false,
  layers: [],
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
  Promise.all([getTables(), getSources()]).then((result) => {
    loading.value = false;
    sources.value = result[1];
  });
});
</script>

<template>
  <AdminListView
    ref="childRef"
    :loading="loading"
    singular-name="Tabel"
    plural-name="Tabellen"
    api-name="tables"
    :get-create-object-dialog-sections="getCreateTableSections"
    :initial-create-object-dialog-data="initialCreateTableData"
    :save-create-object-dialog-data="saveTable"
    :get-objects="getTables"
    :table-headers="tableHeaders"
  />
</template>
