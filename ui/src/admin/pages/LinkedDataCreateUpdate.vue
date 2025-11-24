<template>
  <div class="container __admin">
    <h1 class="font-weight-normal">Gekoppelde data wijzigen</h1>
    <Spinner v-if="loading" style-type="'admin'" />
    <AdminFormSections
      v-else
      ref="formSections"
      :sections="sections"
      :initial-values="initialValues"
      :compact-layout="true"
      :form-object="'linked-data'"
      :object-specific-save="saveLinkedData"
    />
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useToast } from "primevue/usetoast";
import AdminFormSections from "@/admin/components/AdminFormSections.vue";
import Spinner from "@/components/Spinner.vue";

const route = useRoute();
const router = useRouter();
const toast = useToast();

const sections = ref({});
const initialValues = ref({});
const loading = ref(false);
const formSections = ref<{
  sendSaveRequest: (url: string, method: string, currentValues: any) => Promise<Response>;
} | null>(null);

onMounted(() => {
  loading.value = true;

  Promise.all([getLinkedData()]).then(() => {
    sections.value = getSections();
    loading.value = false;
  });
});

const getLinkedData = async () => {
  const result = await fetch(`/atlas/api/v1/linked-data/${route.params.id}/`, {
    credentials: "same-origin",
    headers: { "Content-Type": "application/json" },
  });

  if (!result.ok) {
    console.error("Could not fetch linked data");
    return;
  }

  initialValues.value = await result.json();
  console.log(initialValues.value);
};

const saveLinkedData = async (currentValues: any, continueEditing = false) => {
  const url = `/atlas/api/v1/linked-data/${route.params.id}/`;

  try {
    if (!formSections.value) {
      console.error("Form sections not available");
      return;
    }

    const result = await formSections.value.sendSaveRequest(url, "PATCH", currentValues);

    if (result.ok) {
      if (!continueEditing) {
        router.push("/linked-data");
      }

      toast.add({
        severity: "success",
        summary: "Gekoppelde data opgeslagen",
        detail: "De gekoppelde data is succesvol opgeslagen.",
        life: 3000,
      });
    }
  } catch (e) {
    console.error("An unexpected error occurred:", e);
  }
};

const getSections = () => {
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
          label: "Laag naam",
          id: "name",
          name: "LayerName",
          type: "text",
          required: true,
        },
        {
          label: "Type",
          id: "kind",
          name: "Kind",
          type: "select",
          required: true,
          choices: [
            { value: "layer_join", label: "Layer Join" },
            { value: "external_api", label: "External API Lookup" },
          ],
        },
        {
          label: "URL",
          id: "url",
          name: "Url",
          type: "text",
          required: true,
        },
        {
          label: "Bronsleutel",
          id: "source_key",
          name: "SourceKey",
          type: "text",
          required: true,
        },
        {
          label: "Doelsleutel",
          id: "target_key",
          name: "TargetKey",
          type: "text",
          required: true,
        },
        {
          label: "Bronlaag",
          id: "source",
          name: "Source",
          type: "select",
          required: true,
          endpoint: "/atlas/api/v1/layers/",
          valueKey: "id",
          labelKey: "title",
        },
        {
          label: "Doellaag",
          id: "target_layer",
          name: "TargetLayer",
          type: "select",
          required: false,
          endpoint: "/atlas/api/v1/layers/",
          valueKey: "id",
          labelKey: "title",
          infoText: "Alleen vereist voor Layer Join type",
        },
      ],
    },
    display: {
      label: "Weergave instellingen",
      questions: [
        {
          label: "Tabel kopjes",
          id: "headers",
          name: "Headers",
          type: "textarea",
          required: false,
          multiLine: true,
          infoText: "Voer één veld per regel in.",
        },
        {
          label: "Tabel velden",
          id: "display_properties",
          name: "DisplayProperties",
          type: "textarea",
          required: false,
          multiLine: true,
          infoText: "Voer één veld per regel in. Bij geen invoer worden alle velden getoond.",
        },
        {
          label: "Gebruik detailweergave",
          id: "use_detail_view",
          name: "UseDetailView",
          type: "checkbox",
          required: false,
        },
        {
          label: "Detailweergave velden",
          id: "detail_view_fields",
          name: "DetailViewFields",
          type: "textarea",
          required: false,
          multiLine: true,
          infoText: "Voer één veld per regel in. Bij geen invoer worden alle velden getoond.",
        },
      ],
    },
  };
};
</script>

<style scoped></style>
