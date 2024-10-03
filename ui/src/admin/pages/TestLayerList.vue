<script setup lang="ts">
import AdminListView, { DialogTypes } from "@/admin/components/AdminListView.vue";
import { onMounted, Ref, ref, unref } from "vue";
import { useRouter } from "vue-router";
import { TableHeader } from "@/admin/components/AdminListViewTable.vue";
import { TableFilter } from "@/admin/components/AdminListViewFilter.vue";

const router = useRouter();

const childRef: Ref<null | {
  toggleDialog: (type: DialogTypes) => void;
}> = ref(null);

const categories: Ref<Array<object>> = ref([]);
const layers: Ref<Array<object>> = ref([]);
const loading: Ref<boolean> = ref(true);
const sources: Ref<Array<object>> = ref([]);

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
    overrideKeyForFilter: "category",
    enableLink: false,
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
];

const getLayers = async (params?: URLSearchParams): Promise<Array<object>> => {
  const url = new URL("/atlas/api/v1/layers/", window.location.origin);

  // If params are provided, append them to the URL
  if (params) {
    url.search = params.toString(); // Automatically adds the query string
  }

  const result = await fetch(url.toString(), {
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

const getCategories = async (): Promise<Array<object>> => {
  const result = await fetch("/atlas/api/v1/categories/", {
    credentials: "same-origin",
    headers: { "Content-Type": "application/json" },
  });

  if (!result.ok) {
    console.error("Could not fetch categories");
  }

  const response = await result.json();

  return response.map((category: any) => {
    return { id: category.id, label: category.title };
  });
};

const getSources = async (): Promise<Array<object>> => {
  const result = await fetch("/atlas/api/v1/sources/", {
    credentials: "same-origin",
    headers: { "Content-Type": "application/json" },
  });

  if (!result.ok) {
    console.error("Could not fetch sources");
  }

  const response = await result.json();

  const sources = response.map((source: any) => {
    return { id: source.id, label: source.title };
  });

  return sources;
};

// onMounted
onMounted(() => {
  Promise.all([getSources(), getLayers(), getCategories()]).then((result) => {
    sources.value = result[0];
    layers.value = result[1];
    categories.value = result[2];
    loading.value = false;
  });
});

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
          options: categories,
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
          options: sources,
        },
      ],
    },
  };
};

const getTableFilters = (): Array<TableFilter> => {
  return [
    { options: unref(sources), name: "Bronnen", key: "layer_source", label: "label", dataKey: "id" },
    { options: unref(categories), name: "Categorie", key: "layer_type", label: "label", dataKey: "id" },
    {
      options: [
        { label: "Gepubliceerd", id: "True" },
        { label: "Concept", id: "False" },
      ],
      name: "Status",
      key: "published",
      label: "label",
      dataKey: "id",
    },
  ];
};
</script>

<template>
  <AdminListView
    ref="childRef"
    :loading="loading"
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
    :get-table-filters="getTableFilters"
  />
</template>
