<script setup lang="ts">
import AdminListView from "@/admin/components/AdminListView.vue";
import { ref, Ref } from "vue";
import { TableHeader } from "@/admin/components/AdminListViewTable.vue";
import { useRouter } from "vue-router";
import { EDialogTypes } from "@/types/dialog";

const router = useRouter();

const loading: Ref<boolean> = ref(true);

const childRef: Ref<null | {
  toggleDialog: (type: EDialogTypes) => void;
}> = ref(null);

const saveGroup = async (
  currentValues: any,
  continueEditing = false,
  sendSaveRequest: (apiUrl: string, method: string, currentValues: object) => Response,
) => {
  const url = "/atlas/api/v1/groups/";

  try {
    const result = await sendSaveRequest(url, "POST", currentValues);

    if (result.ok) {
      childRef?.value?.toggleDialog(EDialogTypes.Create);

      if (continueEditing) {
        const response = await result.json();
        await router.push(`/groups/update/${response.id}`);
      }
    }
  } catch (e) {
    console.error("An unexpected error occurred:", e);
  }
};

const getCreateGroupSections = () => {
  return {
    general: {
      label: "Algemene gegevens",
      questions: [
        {
          label: "Groep",
          id: "name",
          name: "Name",
          type: "text",
          required: true,
        },
      ],
    },
  };
};

const initialCreateGroupData = {
  title: "",
  authenticate: false,
};

const tableHeaders: Array<TableHeader> = [
  {
    header: "Groep",
    key: "name",
    enableLink: true,
  },
];
</script>

<template>
  <AdminListView
    ref="childRef"
    :loading="loading"
    singular-name="Groep"
    plural-name="Groepen"
    api-name="groups"
    :get-create-object-dialog-sections="getCreateGroupSections"
    :initial-create-object-dialog-data="initialCreateGroupData"
    :save-create-object-dialog-data="saveGroup"
    :table-headers="tableHeaders"
  />
</template>
