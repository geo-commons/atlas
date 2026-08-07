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
  {
    header: "Status",
    key: "published",
    enableLink: false,
    mapValues: {
      true: "Gepubliceerd",
      false: "Concept",
    },
  },
  {
    header: "Tonen op portal",
    key: "show_in_overview",
    enableLink: false,
  },
];

const initialMapData = {
  title: "",
  authenticate: false,
  layers: [],
  categories: [],
};

const getCreateMapSections = () => {
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
          infoText: "Een uniek kort kenmerk voor de kaart in Atlas.",
        },
      ],
    },
  };
};

const saveMap = async (
  currentValues: any,
  continueEditing = false,
  sendSaveRequest: (apiUrl: string, method: string, currentValues: object) => Response,
) => {
  const url = "/atlas/api/v1/maps/";

  try {
    const result = await sendSaveRequest(url, "POST", currentValues);

    if (result.ok) {
      childRef?.value?.toggleDialog(EDialogTypes.Create);

      if (continueEditing) {
        const response = await result.json();
        await router.push(`/maps/update/${response.id}`);
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
    singular-name="Kaart"
    plural-name="Kaarten"
    api-name="maps"
    :get-create-object-dialog-sections="getCreateMapSections"
    :initial-create-object-dialog-data="initialMapData"
    :save-create-object-dialog-data="saveMap"
    :enable-duplicate="true"
    :enable-import-export="true"
    :enable-delete-multiple="true"
    :table-headers="tableHeaders"
    :fixed-query-params="{ is_main: 'False' }"
    :view-base-url="'/atlas/maps'"
  />
</template>
