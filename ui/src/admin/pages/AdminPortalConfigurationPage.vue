<template>
  <div class="container __admin">
    <h1 class="font-weight-normal">Portaal configuratie</h1>
    <Spinner v-if="loading" style-type="'admin'" />
    <AdminFormSections
      v-else
      ref="formSections"
      :sections="sections"
      :initial-values="initialValues"
      :object-specific-save="saveConfiguration"
      :contains-image-field="true"
    />
  </div>
</template>

<script setup lang="ts">
import AdminFormSections from "@/admin/components/AdminFormSections.vue";
import Spinner from "@/components/Spinner.vue";
import type { AdminFormConfig, AdminFormValues } from "@/types/AdminFormType";
import { useToast } from "primevue/usetoast";
import { useRouter } from "@/utils/inertia-routing";
import Cookies from "js-cookie";
import { onMounted, ref } from "vue";

const PORTAL_CONFIG_KEYS = [
  "FEATURE_PORTAL",
  "ORGANIZATION_IMAGE",
  "ORGANIZATION_PRIMARY_COLOR",
  "ORGANIZATION_TITLE_COLOR",
  "ORGANIZATION_TEXT_COLOR",
  "ORGANIZATION_HEADER",
  "ORGANIZATION_INTRODUCTION",
] as const;

interface ConfigurationItem {
  key: string;
  value: string;
}

const router = useRouter();
const toast = useToast();

const sections = ref<AdminFormConfig>({});
const initialValues = ref<AdminFormValues>({});
const loading = ref(false);

const constructAdminFormValues = (data: ConfigurationItem[]): AdminFormValues => {
  return data.reduce<AdminFormValues>((formValues, item) => {
    formValues[item.key] = item.value === "true" ? true : item.value === "false" ? false : item.value;
    return formValues;
  }, {});
};

const getSections = (): AdminFormConfig => {
  return {
    features: {
      label: "Algemeen",
      questions: [
        {
          label: "Portaal inschakelen",
          id: "FEATURE_PORTAL",
          name: "featurePortal",
          type: "checkbox",
          infoText: "Maak het portaal zichtbaar als startscherm",
        },
      ],
    },
    header: {
      label: "Header",
      questions: [
        {
          id: "ORGANIZATION_IMAGE",
          name: "organizationImage",
          type: "image",
          label: "Organisatie header afbeelding",
        },
        {
          label: "Organisatie header tekst",
          id: "ORGANIZATION_HEADER",
          name: "organizationHeader",
          type: "text",
        },
        {
          label: "Organisatie introductie",
          id: "ORGANIZATION_INTRODUCTION",
          name: "organizationIntroduction",
          type: "text",
          multiLine: true,
          infoText: "Introductie tekst die wordt laten zien bovenaan de pagina",
        },
      ],
    },
    kleuren: {
      label: "Kleuren",
      questions: [
        {
          id: "ORGANIZATION_PRIMARY_COLOR",
          name: "organizationPrimaryColor",
          type: "color",
          label: "Primaire kleur van de organisatie",
          infoText: "Klik op de kleur om de kleur aan te passen. NB: voor nu alleen beschikbaar in HEX",
        },
        {
          id: "ORGANIZATION_TITLE_COLOR",
          name: "organizationTitleColor",
          type: "color",
          label: "Titel kleur",
        },
        {
          id: "ORGANIZATION_TEXT_COLOR",
          name: "organizationTextColor",
          type: "color",
          label: "Tekst kleur",
        },
      ],
    },
  };
};

const getConfigurations = async (): Promise<void> => {
  const result = await fetch(`/atlas/api/v1/configurations/`, {
    credentials: "same-origin",
    headers: { "Content-Type": "application/json" },
  });

  if (!result.ok) {
    console.error("Could not fetch configurations");
    return;
  }

  const data: ConfigurationItem[] = await result.json();
  const allValues = constructAdminFormValues(data);
  initialValues.value = Object.fromEntries(
    Object.entries(allValues).filter(([key]) => (PORTAL_CONFIG_KEYS as readonly string[]).includes(key)),
  );
};

const saveConfiguration = async (currentValues: AdminFormValues, continueEditing = false): Promise<void> => {
  try {
    const data = new FormData();
    Object.entries(currentValues).forEach(([key, value]) => {
      data.append(key, value instanceof File ? value : String(value));
    });

    const result = await fetch(`/atlas/api/v1/configurations/`, {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "X-CSRFToken": Cookies.get("csrftoken") ?? "",
      },
      body: data,
    });

    if (result.ok) {
      if (!continueEditing) {
        router.push("/");
      }
      toast.add({
        severity: "success",
        summary: "Portaal configuratie opgeslagen",
        detail: "De portaal configuratie is succesvol opgeslagen.",
        life: 3000,
      });
    } else {
      toast.add({
        severity: "error",
        summary: "Opslaan mislukt",
        detail: "De portaal configuratie kon niet worden opgeslagen. Probeer het later opnieuw.",
        life: 5000,
      });
    }
  } catch (e) {
    console.error("An unexpected error occurred:", e);
    toast.add({
      severity: "error",
      summary: "Opslaan mislukt",
      detail: "Er is een onverwachte fout opgetreden. Probeer het later opnieuw.",
      life: 5000,
    });
  }
};

onMounted(async () => {
  loading.value = true;
  await getConfigurations();
  sections.value = getSections();
  loading.value = false;
});
</script>
