<script setup lang="ts">
import AdminListView from "@/admin/components/AdminListView.vue";
import { onMounted, Ref, ref } from "vue";
import { TableHeader } from "@/admin/components/AdminListViewTable.vue";
import { useRouter } from "vue-router";
import { EDialogTypes } from "@/types/dialog";
import { getAllObjects } from "@/utils/api-helpers";

const router = useRouter();

const childRef: Ref<null | {
  toggleDialog: (type: EDialogTypes) => void;
}> = ref(null);

const loading: Ref<boolean> = ref(true);
const categories: Ref<Array<{ id: number; label: string }>> = ref([]);

const tableHeaders: Array<TableHeader> = [
  {
    header: "Titel",
    key: "title",
    enableLink: true,
  },
  {
    header: "Hoofdcategorie",
    key: "parent.title",
    enableLink: false,
  },
];

const initialCategoryData = {
  title: "",
  authenticate: false,
  slug: "",
  parent_id: null,
};

const getCategories = async (): Promise<Array<{ id: number; label: string }>> => {
  const result = await fetch(getAllObjects("/atlas/api/v1/categories/"), {
    credentials: "same-origin",
    headers: { "Content-Type": "application/json" },
  });

  if (!result.ok) {
    console.error("Could not fetch categories");
  }

  const response = await result.json();

  return response.results
    .filter((category: any) => !category.parent)
    .map((category: any) => ({ id: category.id, label: category.title }));
};

const getCreateCategorySections = () => {
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
          infoText: "Een uniek kort kenmerk voor de categorie in Atlas.",
        },
        {
          label: "Hoofdcategorie",
          id: "parent_id",
          name: "ParentId",
          type: "dropdown",
          required: false,
          placeholder: "hoofdcategorie",
          options: categories,
          infoText: "Laat leeg voor een hoofdcategorie. Kies een hoofdcategorie om een subcategorie aan te maken.",
        },
      ],
    },
  };
};

onMounted(async () => {
  categories.value = await getCategories();
  loading.value = false;
});

const saveCategory = async (
  currentValues: any,
  continueEditing = false,
  sendSaveRequest: (apiUrl: string, method: string, currentValues: object) => Response,
) => {
  const url = "/atlas/api/v1/categories/";

  try {
    const result = await sendSaveRequest(url, "POST", currentValues);

    if (result.ok) {
      childRef?.value?.toggleDialog(EDialogTypes.Create);

      if (continueEditing) {
        const response = await result.json();
        await router.push(`/categories/update/${response.id}`);
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
    singular-name="Categorie"
    plural-name="Categorieën"
    api-name="categories"
    :enable-duplicate="true"
    :enable-import-export="true"
    :enable-delete-multiple="true"
    :get-create-object-dialog-sections="getCreateCategorySections"
    :initial-create-object-dialog-data="initialCategoryData"
    :save-create-object-dialog-data="saveCategory"
    :table-headers="tableHeaders"
  />
</template>
