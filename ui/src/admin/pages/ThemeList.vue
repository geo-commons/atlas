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

const themes: Ref<Array<object>> = ref([]);
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

const getThemes = async (params?: URLSearchParams): Promise<{ results: Array<object>; count: number }> => {
  const url = new URL("/atlas/api/v1/themes/", window.location.origin);

  if (params) {
    url.search = params.toString();
  }

  const result = await fetch(url.toString(), {
    credentials: "same-origin",
    headers: { "Content-Type": "application/json" },
  });

  if (!result.ok) {
    console.error("Could not fetch themes");
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

const saveTheme = async (
  currentValues: any,
  continueEditing = false,
  sendSaveRequest: (apiUrl: string, method: string, currentValues: object) => Response,
) => {
  const url = "/atlas/api/v1/themes/";

  currentValues.datasets = [];

  try {
    const result = await sendSaveRequest(url, "POST", currentValues);

    if (result.ok) {
      childRef?.value?.toggleDialog("create-object-dialog");

      if (continueEditing) {
        const response = await result.json();
        await router.push(`/themes/update/${response.id}`);
      }
    }
  } catch (e) {
    console.error("An unexpected error occurred:", e);
  }
};

// onMounted
onMounted(() => {
  Promise.all([getThemes()]).then((result) => {
    themes.value = result[0].results;
    loading.value = false;
  });
});
</script>

<template>
  <AdminListView
    ref="childRef"
    :loading="loading"
    singular-name="Thema"
    plural-name="Thema's"
    api-name="themes"
    :get-create-object-dialog-sections="getCreateThemeSections"
    :initial-create-object-dialog-data="initialThemeData"
    :save-create-object-dialog-data="saveTheme"
    :get-objects="getThemes"
    :table-headers="tableHeaders"
  />
</template>
