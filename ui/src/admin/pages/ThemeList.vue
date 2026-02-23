<script setup lang="ts">
import AdminListView from "@/admin/components/AdminListView.vue";
import { Ref, ref } from "vue";
import { TableHeader } from "@/admin/components/AdminListViewTable.vue";
import { useRouter } from "vue-router";
import { EDialogTypes } from "@/types/dialog";

const router = useRouter();

const childRef: Ref<null | {
  toggleDialog: (type: EDialogTypes) => void;
}> = ref(null);

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
      childRef?.value?.toggleDialog(EDialogTypes.Create);

      if (continueEditing) {
        const response = await result.json();
        await router.push(`/themes/update/${response.id}`);
      }
    }
  } catch (e) {
    console.error("An unexpected error occurred:", e);
  }
};
</script>

<template>
  <AdminListView
    ref="childRef"
    :loading="loading"
    singular-name="Thema"
    plural-name="Thema's"
    api-name="themes"
    :get-create-object-dialog-sections="getCreateThemeSections"
    :enable-import-export="true"
    :enable-delete-multiple="true"
    :initial-create-object-dialog-data="initialThemeData"
    :save-create-object-dialog-data="saveTheme"
    :table-headers="tableHeaders"
  />
</template>
