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
    >
      <template #relatedData>
        <div class="layer-setting">
          <div class="admin-label-button">
            <button
              v-tippy
              aria-label="Voeg gerelateerde data toe"
              content="Voeg gerelateerde data toe"
              type="button"
              class="button __small __secondary_admin"
              @click="toggleModal()"
            >
              <AddIcon />
              Voeg toe
            </button>
          </div>

          <ul class="admin-list">
            <li v-for="relatedItem in initialValues.related" :key="relatedItem.id">
              {{ relatedItem }}
              <div class="admin-list-buttons">
                <button
                  v-tippy
                  :content="`Bewerk gerelateerde data ${relatedItem.title}`"
                  :aria-label="`Bewerk gerelateerde data ${relatedItem.title}`"
                  type="button"
                  class="iconbutton __normal __round"
                  @click="editRelatedData(relatedItem)"
                >
                  <EditIcon class="icon __medium"></EditIcon>
                </button>
                <button
                  v-tippy
                  :content="`Verwijder gerelateerde data ${relatedItem.title}`"
                  :aria-label="`Verwijder gerelateerde data ${relatedItem.title}`"
                  type="button"
                  class="iconbutton __normal __round"
                  @click="removeRelatedData(relatedItem)"
                >
                  <TrashIcon class="icon __medium"></TrashIcon>
                </button>
              </div>
            </li>
          </ul>
        </div>
      </template>
    </AdminFormSections>
  </div>
  <FormModal v-if="showFormModal" :toggle-modal="showFormModal" @close="closeFormModal">
    <template #header>
      <h3>Gerelateerde data selecteren</h3>
    </template>
    <template #body>
      <div class="related-data-selector">
        <label for="relatedDataSelect">Selecteer gerelateerde LinkedData:</label>
        <select id="relatedDataSelect" v-model="selectedRelatedDataId" class="form-control">
          <option value="">Selecteer...</option>
          <option v-for="linkedData in availableLinkedData" :key="linkedData.id" :value="linkedData.id">
            {{ linkedData.title }}
          </option>
        </select>
        <div class="modal-buttons">
          <button type="button" class="button __primary" :disabled="!selectedRelatedDataId" @click="addRelatedData">
            Toevoegen
          </button>
          <button type="button" class="button __secondary" @click="closeFormModal">Annuleren</button>
        </div>
      </div>
    </template>
  </FormModal>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useToast } from "primevue/usetoast";
import AdminFormSections from "@/admin/components/AdminFormSections.vue";
import Spinner from "@/components/Spinner.vue";
import AddIcon from "@/assets/icons/add-icon.svg";
import EditIcon from "@/assets/icons/edit-icon.svg";
import TrashIcon from "@/assets/icons/trash-icon.svg";
import FormModal from "@/components/FormModal.vue";

// Types
interface LinkedDataItem {
  id: number;
  title: string;
  layer_name?: string;
  kind?: string;
  url?: string;
  source_key?: string;
  target_key?: string;
  source?: number;
  target_layer?: number;
  headers?: string;
  display_properties?: string[];
  use_detail_view?: boolean;
  detail_view_fields?: string;
}

interface InitialValues {
  title?: string;
  name?: string;
  layer_name?: string;
  kind?: string;
  url?: string;
  source_key?: string;
  target_key?: string;
  source?: number;
  target_layer?: number;
  headers?: string;
  display_properties?: string[];
  use_detail_view?: boolean;
  detail_view_fields?: string;
  related: LinkedDataItem[];
}

const route = useRoute();
const router = useRouter();
const toast = useToast();

const sections = ref({});
const initialValues = ref<InitialValues>({ related: [] });
const loading = ref(false);
const formSections = ref<{
  sendSaveRequest: (url: string, method: string, currentValues: any) => Promise<Response>;
} | null>(null);

// Modal state
const showFormModal = ref(false);
const availableLinkedData = ref<LinkedDataItem[]>([]);
const selectedRelatedDataId = ref("");

onMounted(() => {
  loading.value = true;

  Promise.all([getLinkedData(), getAvailableLinkedData()]).then(() => {
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

  const response = await result.json();
  initialValues.value = { ...response, related: response.related || [] };
};

const getAvailableLinkedData = async () => {
  const result = await fetch("/atlas/api/v1/linked-data/", {
    credentials: "same-origin",
    headers: { "Content-Type": "application/json" },
  });

  if (!result.ok) {
    console.error("Could not fetch available linked data");
    return;
  }

  const response = await result.json();
  availableLinkedData.value = response.results || response;
};

const saveLinkedData = async (currentValues: any, continueEditing = false) => {
  const url = `/atlas/api/v1/linked-data/${route.params.id}/`;

  try {
    if (!formSections.value) {
      console.error("Form sections not available");
      return;
    }

    // Include the related data in currentValues
    currentValues.related = initialValues.value.related.map((item: LinkedDataItem) => item.id);

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

// Modal and related data management methods
const toggleModal = () => {
  selectedRelatedDataId.value = "";
  showFormModal.value = true;
};

const closeFormModal = () => {
  showFormModal.value = false;
  selectedRelatedDataId.value = "";
};

const addRelatedData = () => {
  if (!selectedRelatedDataId.value) return;

  const selectedItem = availableLinkedData.value.find(
    (item: LinkedDataItem) => item.id === parseInt(selectedRelatedDataId.value),
  );

  if (selectedItem && !initialValues.value.related.find((item: LinkedDataItem) => item.id === selectedItem.id)) {
    initialValues.value.related.push(selectedItem);
  }

  closeFormModal();
};

const editRelatedData = (relatedItem: LinkedDataItem) => {
  // Navigate to the edit page of the related LinkedData item
  router.push(`/linked-data/${relatedItem.id}`);
};

const removeRelatedData = (relatedItem: LinkedDataItem) => {
  const index = initialValues.value.related.findIndex((item: LinkedDataItem) => item.id === relatedItem.id);
  if (index > -1) {
    initialValues.value.related.splice(index, 1);
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
          type: "text",
          required: false,
          multiLine: true,
          infoText: "Voer één veld per regel in.",
        },
        {
          label: "Tabel velden",
          id: "display_properties",
          name: "DisplayProperties",
          type: "text",
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
          type: "text",
          required: false,
          multiLine: true,
          infoText: "Voer één veld per regel in. Bij geen invoer worden alle velden getoond.",
        },
      ],
    },
    relatedData: {
      label: "Gerelateerde data",
      questions: [],
      disableInputs: true,
    },
  };
};
</script>

<style scoped></style>
