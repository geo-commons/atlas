<script setup lang="ts">
import AdminListView from "@/admin/components/AdminListView.vue";
import { onMounted, Ref, ref } from "vue";
import { TableHeader } from "@/admin/components/AdminListViewTable.vue";
import { useRouter } from "vue-router";
import { EDialogTypes } from "@/types/dialog";

const childRef: Ref<null | {
  toggleDialog: (type: EDialogTypes) => void;
}> = ref(null);

const authorizations: Ref<Array<object>> = ref([]);
const sources: Ref<Array<object>> = ref([]);
const loading: Ref<boolean> = ref(true);

const router = useRouter();

const newAuthorizationData = {
  source: "",
  resource: "",
};

const tableHeaders: Array<TableHeader> = [
  {
    header: "Resource",
    key: "resource",
    enableLink: true,
  },
];

const getAuthorizations = async (params?: URLSearchParams): Promise<{ results: Array<object>; count: number }> => {
  const url = new URL("/atlas/api/v1/authorizations/", window.location.origin);

  if (params) {
    url.search = params.toString();
  }

  const result = await fetch(url.toString(), {
    credentials: "same-origin",
    headers: { "Content-Type": "application/json" },
  });

  if (!result.ok) {
    console.error("Could not fetch authorizations");
  }

  const items = await result.json();

  return items;
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
    return { id: source.id, label: source.title, url: source.url, type: source.source_type };
  });
};

const saveAuthorization = async (
  currentValues: any,
  continueEditing = false,
  sendSaveRequest: (apiUrl: string, method: string, currentValues: object) => Response,
) => {
  const url = "/atlas/api/v1/authorizations/";

  try {
    const result = await sendSaveRequest(url, "POST", currentValues);

    if (result.ok) {
      childRef?.value?.toggleDialog(EDialogTypes.Create);

      if (continueEditing) {
        const response = await result.json();
        await router.push(`/authorizations/update/${response.id}`);
      }
    }
  } catch (e) {
    console.error("An unexpected error occurred:", e);
  }
};
const getCreateAuthorizationSections = () => {
  return {
    general: {
      label: "Algemene gegevens",
      questions: [
        {
          label: "Bron",
          id: "source",
          name: "Source",
          type: "dropdown",
          required: true,
          placeholder: "bron",
          options: sources,
        },
        {
          label: "Resource",
          id: "resource",
          name: "Resource",
          type: "text",
          required: true,
          infoText: "Naam van de laag of de resource",
        },
        {
          label: "Beschrijving",
          id: "description",
          name: "Description",
          type: "text",
          required: true,
          multiLine: true,
          infoText: "Een beschrijvende tekst voor beheerders",
        },
      ],
    },
  };
};

// onMounted
onMounted(() => {
  Promise.all([getAuthorizations(), getSources()]).then((result) => {
    authorizations.value = result[0].results;
    sources.value = result[1];
    loading.value = false;
  });
});
</script>

<template>
  <AdminListView
    ref="childRef"
    :loading="loading"
    singular-name="Autorisatie"
    plural-name="Autorisaties"
    api-name="authorizations"
    :get-objects="getAuthorizations"
    :get-create-object-dialog-sections="getCreateAuthorizationSections"
    :initial-create-object-dialog-data="newAuthorizationData"
    :save-create-object-dialog-data="saveAuthorization"
    :table-headers="tableHeaders"
  />
</template>
