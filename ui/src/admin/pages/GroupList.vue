<script setup lang="ts">
import AdminListView, { DialogTypes } from "@/admin/components/AdminListView.vue";
import { onMounted, ref, Ref } from "vue";
import { TableHeader } from "@/admin/components/AdminListViewTable.vue";
import { useRouter } from "vue-router";

const router = useRouter();

const loading: Ref<boolean> = ref(true);

const childRef: Ref<null | {
  toggleDialog: (type: DialogTypes) => void;
}> = ref(null);

const getGroups = async (params?: URLSearchParams): Promise<{ results: Array<object>; count: number }> => {
  const url = new URL("/atlas/api/v1/groups/", window.location.origin);

  if (params) {
    url.search = params.toString();
  }

  const result = await fetch(url.toString(), {
    credentials: "same-origin",
    headers: { "Content-Type": "application/json" },
  });

  if (!result.ok) {
    console.error("Could not fetch groups");
  }

  const items = await result.json();

  return items;
};

const saveGroup = async (
  currentValues: any,
  continueEditing = false,
  sendSaveRequest: (apiUrl: string, method: string, currentValues: object) => Response,
) => {
  const url = "/atlas/api/v1/groups/";

  try {
    const result = await sendSaveRequest(url, "POST", currentValues);

    if (result.ok) {
      childRef?.value?.toggleDialog("create-object-dialog");

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

// onMounted
onMounted(() => {
  Promise.all([getGroups()]).then((result) => {
    loading.value = false;
  });
});
</script>

<template>
  <AdminListView
    ref="childRef"
    :loading="loading"
    singular-name="Groep"
    plural-name="Groepen"
    api-name="groups"
    :enable-import-export="false"
    :get-create-object-dialog-sections="getCreateGroupSections"
    :initial-create-object-dialog-data="initialCreateGroupData"
    :save-create-object-dialog-data="saveGroup"
    :get-objects="getGroups"
    :table-headers="tableHeaders"
  />
</template>
