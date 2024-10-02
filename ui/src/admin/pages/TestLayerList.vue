<script setup lang="ts">
import AdminListView, { DialogTypes } from "@/admin/components/AdminListView.vue";
import { Ref, ref } from "vue";
import { useRouter } from "vue-router";
import { TableHeader } from "@/admin/components/AdminListViewTable.vue";

const router = useRouter();

const childRef: Ref<null | {
  toggleDialog: (type: DialogTypes) => void;
}> = ref(null);

const categories = ref([]);
const initialCreateLayerData = {
  title: "",
  authenticate: false,
  metadata: { name: "", description: "", organization: "", updated: "", link: "", lineage: "", contact: "" },
};
const tableHeaders: Array<TableHeader> = [
  {
    header: "Titel",
    key: "title",
    enableLink: true,
  },
  {
    header: "Categorie",
    key: "category.title",
    enableLink: false,
  },
];

const getLayers = async (): Promise<Array<object>> => {
  const result = await fetch("/atlas/api/v1/layers/", {
    credentials: "same-origin",
    headers: { "Content-Type": "application/json" },
  });

  if (!result.ok) {
    console.error("Could not fetch layers");
  }

  const items = await result.json();

  return items;
};

const selectedItems = ref([]);

const getCategories = async () => {
  const result = await fetch("/atlas/api/v1/categories/", {
    credentials: "same-origin",
    headers: { "Content-Type": "application/json" },
  });

  if (!result.ok) {
    console.error("Could not fetch categories");
  }

  const response = await result.json();

  categories.value = response.map((category: any) => category.title);

  return response.map((category: any) => {
    return { id: category.id, label: category.title };
  });
};

const getSources = async () => {
  const result = await fetch("/atlas/api/v1/sources/", {
    credentials: "same-origin",
    headers: { "Content-Type": "application/json" },
  });

  if (!result.ok) {
    console.error("Could not fetch sources");
  }

  const response = await result.json();

  return response.map((source: any) => {
    return { id: source.id, label: source.title };
  });
};

const saveLayer = async (
  currentValues: any,
  continueEditing = false,
  sendSaveRequest: (apiUrl: string, method: string, currentValues: object) => Response,
) => {
  const url = "/atlas/api/v1/layers/";

  try {
    const result = await sendSaveRequest(url, "POST", currentValues);

    if (result.ok) {
      childRef?.value?.toggleDialog("create-object-dialog");

      if (continueEditing) {
        const response = await result.json();
        await router.push(`/layers/update/${response.id}`);
      }

      // TODO: implement this.getLayers()
      // await this.getLayers();
    }
  } catch (e) {
    console.error("An unexpected error occurred:", e);
  }
};

const getCreateLayerSections = () => {
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
          label: "Categorie",
          id: "category_id",
          name: "Category",
          type: "dropdown",
          required: false,
          placeholder: "categorie",
          options: getCategories,
        },
      ],
    },
    source: {
      label: "Bron",
      questions: [
        {
          label: "Bron",
          id: "source_id",
          name: "Source",
          type: "dropdown",
          required: true,
          placeholder: "bron",
          options: getSources,
        },
      ],
    },
  };
};
</script>

<template>
  <AdminListView
    ref="childRef"
    singular-name="Kaartlaag"
    plural-name="Kaartlagen"
    api-name="layers"
    :enable-sort="true"
    :get-create-object-dialog-sections="getCreateLayerSections"
    :initial-create-object-dialog-data="initialCreateLayerData"
    :save-create-object-dialog-data="saveLayer"
    :get-objects="getLayers"
    :selected-items="selectedItems"
    :table-headers="tableHeaders"
  />
</template>
