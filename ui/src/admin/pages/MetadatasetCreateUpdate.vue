<template>
  <div class="container __admin">
    <h1 class="py-8">Metadataset wijzigen</h1>
    <Spinner v-if="loading" style-type="'admin'" />
    <AdminFormSections
      v-else
      ref="formSections"
      :sections="sections"
      :initial-values="initialValues"
      :form-object="'metadatasets'"
      :object-specific-save="saveMetadataset"
    />

    <div v-if="!loading">
      <Spinner v-if="layersAsyncStatus == 'loading'" style-type="'admin'" />
      <AssignedLayersList v-else :layers="layersState.data" />
    </div>
  </div>
</template>

<script setup lang="ts">
import AdminFormSections from "@/admin/components/AdminFormSections.vue";
import AssignedLayersList from "@/admin/components/AssignedLayersList.vue";
import Spinner from "@/components/Spinner.vue";
import {
  accessConstraintsTypeOptions,
  authorizationLevelTypeOptions,
  otherConstraintsTypeOptions,
  roleTypeOptions,
  statusTypeOptions,
  topicCategoryOptions,
  updateMethodTypeOptions,
  type AdminFormConfig,
} from "@/types";
import { IMetadataset } from "@/types/metadataset";
import { useToast } from "primevue/usetoast";
import { onMounted, ref, type Ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { formatDateForInput } from "@/utils/date-formatter";
import { useQueryCache } from "@pinia/colada";
import { useLayerList } from "@/admin/queries";

// Composables
const route = useRoute();
const router = useRouter();
const toast = useToast();
const queryCache = useQueryCache();

// Queries
const { layersState, layersSearch, asyncStatus: layersAsyncStatus } = useLayerList();

// Reactive data
const sections: Ref<AdminFormConfig> = ref({});
const initialValues: Ref<Partial<IMetadataset>> = ref({});
const loading = ref(false);
const formSections = ref();

layersSearch.value = route.params.id as string;

// Methods
const getMetadataset = async (): Promise<void> => {
  const result = await fetch(`/atlas/api/v1/metadatasets/${route.params.id}/`, {
    credentials: "same-origin",
    headers: { "Content-Type": "application/json" },
  });

  if (!result.ok) {
    console.error("Could not fetch metadataset");
    return;
  }

  initialValues.value = await result.json();

  initialValues.value.last_updated = formatDateForInput(initialValues.value.last_updated);
};

const saveMetadataset = async (currentValues: Partial<IMetadataset>, continueEditing = false): Promise<void> => {
  const url = `/atlas/api/v1/metadatasets/${route.params.id}/`;

  const payload: Partial<IMetadataset> = {
    ...currentValues,
    last_updated: formatDateForInput(currentValues.last_updated) || null,
  };

  try {
    const result = await formSections.value.sendSaveRequest(url, "PATCH", payload);

    if (result.ok) {
      await queryCache.invalidateQueries(["metadatasets"]);

      if (!continueEditing) {
        router.push(`/metadatasets`);
      }

      toast.add({
        severity: "success",
        summary: "Metadataset opgeslagen",
        detail: "De metadataset is succesvol opgeslagen.",
        life: 3000,
      });
    }
  } catch (e) {
    console.error("An unexpected error occurred:", e);
  }
};

const getSections = (): AdminFormConfig => {
  return {
    general: {
      label: "Algemene informatie",
      questions: [
        {
          label: "Naam",
          id: "title",
          name: "Title",
          type: "text",
          required: false,
          visibility: "Publiek",
          infoText: "De naam van de metadataset. Dit is de naam die wordt weergegeven in de interface.",
        },
        {
          label: "Kort kenmerk",
          id: "slug",
          name: "Slug",
          type: "text",
          required: false,
          visibility: "Publiek",
          infoText:
            "Een uniek kort kenmerk voor de metadataset in Atlas. Gebruik alleen kleine letters, cijfers en afbreekstreepjes.",
          maxLength: 255,
        },
        {
          label: "Beschrijving",
          id: "description",
          name: "Description",
          type: "text",
          multiLine: true,
          required: false,
          visibility: "Intern",
          infoText: "Beschrijving voor intern gebruik. Het is mogelijk om tekst op te maken met Markdown in dit veld.",
        },
        {
          label: "Toelichting dataset",
          id: "abstract",
          name: "Abstract",
          type: "text",
          multiLine: true,
          required: false,
          visibility: "Publiek",
          infoText:
            "Een beschrijving van de inhoud van de dataset, geef in deze samenvatting publieksvriendelijke informatie over de inhoud van de dataset. Deze is minimaal drie zinnen en maximaal één alinea lang (2000 karakters).",
        },
        {
          label: "Onderwerp",
          id: "topic_category",
          name: "Topic Category",
          type: "dropdown",
          placeholder: "onderwerp",
          required: false,
          visibility: "Publiek",
          infoText: "Het belangrijkste onderwerp van de dataset.",
          options: topicCategoryOptions,
        },
        {
          label: "Trefwoorden",
          id: "keyword",
          name: "Keyword",
          type: "text",
          multiLine: true,
          required: false,
          visibility: "Publiek",
          infoText:
            "In het algemeen gebruikte woorden of geformaliseerde zinnen om een dataset of datasetserie te beschrijven. Eén trefwoord per regel.",
        },
        {
          label: "Doel van de vervaardiging",
          id: "statement",
          name: "Purpose of Manufacture",
          type: "text",
          required: false,
          multiLine: true,
          visibility: "Publiek",
          infoText: "De reden waarom de dataset is gemaakt.",
        },
      ],
    },
    source: {
      label: "Bron",
      questions: [
        {
          label: "Oorspronkelijke bron",
          id: "source_origin",
          name: "Original Source",
          type: "text",
          required: false,
          visibility: "Publiek",
          infoText:
            "Algemene beschrijving herkomst. Dit is de bron waar de dataset vandaan komt, dat kan een URL zijn of een beschrijving van de bron.",
        },
        {
          label: "Bronlocatie",
          id: "source_location",
          name: "Source Location",
          type: "text",
          required: false,
          visibility: "Intern",
          infoText: "Bijvoorbeeld Objectstore (COG), S3, etc.",
        },
        {
          label: "Naam contactpersoon aanspreekpunt",
          id: "source_name_internal",
          name: "Source Name Internal",
          type: "text",
          required: false,
          visibility: "Intern",
          infoText: "De naam van de contactpersoon van het interne aanspreekpunt van de bron.",
        },
        {
          label: "E-mailadres aanspreekpunt",
          id: "source_email_internal",
          name: "Source Email Internal",
          type: "text",
          required: false,
          visibility: "Intern",
          infoText: "Het e-mailadres van het interne aanspreekpunt van de bron.",
        },
        {
          label: "Verantwoordelijke organisatie",
          id: "source_organization",
          name: "Source Organization",
          type: "text",
          required: false,
          visibility: "Publiek",
          infoText:
            "De organisatie van de verantwoordelijke van de bron, bijvoorbeeld de gemeente, provincie, Nederlandse organisatie voor toegepast-natuurwetenschappelijk onderzoek (TNO), etc.",
        },
        {
          label: "Naam contactpersoon aanspreekpunt",
          id: "source_name_public",
          name: "Source Name Public",
          type: "text",
          required: false,
          visibility: "Publiek",
          infoText: "De naam van de contactpersoon van de verantwoordelijke van de bron.",
        },
        {
          label: "E-mailadres verantwoordelijke",
          id: "source_email_public",
          name: "Source Email Public",
          type: "text",
          required: false,
          visibility: "Publiek",
          infoText: "Het e-mailadres van de verantwoordelijke organisatie van de bron.",
        },
        {
          label: "Rol verantwoordelijke",
          id: "source_role_person_responsible",
          name: "Data Manager Role",
          type: "dropdown",
          options: roleTypeOptions,
          required: false,
          visibility: "Publiek",
          placeholder: "rol",
          infoText: "De rol van de verantwoordelijke over de bron.",
        },
      ],
    },
    status: {
      label: "Status",
      questions: [
        {
          label: "Updatemethode",
          id: "update_method",
          name: "Update Method",
          type: "dropdown",
          required: false,
          visibility: "Intern",
          options: updateMethodTypeOptions,
          placeholder: "updatemethode",
          infoText: "De methode waarmee de dataset wordt bijgewerkt.",
        },
        {
          label: "Updatefrequentie",
          id: "update_frequency",
          name: "Update Frequency",
          type: "text",
          required: false,
          visibility: "Publiek",
          infoText:
            "De frequentie waarmee de dataset wordt bijgewerkt. Bijvoorbeeld: dagelijks, wekelijks, maandelijks, jaarlijks.",
        },
        {
          label: "Laatst bijgewerkt",
          id: "last_updated",
          name: "Last Updated",
          type: "date",
          required: false,
          visibility: "Publiek",
          infoText: "De datum waarop de dataset voor het laatst is bijgewerkt.",
        },
        {
          label: "FME-script",
          id: "fme_script",
          name: "FME Script",
          type: "text",
          required: false,
          visibility: "Intern",
          placeholder: "bijv. workspace.fmw",
          infoText:
            "Naam of pad van de FME-workspace of script waarmee de dataset wordt bijgewerkt. Alleen zichtbaar in Atlas Admin.",
        },
        {
          label: "Autorisatieniveau",
          id: "authorization_level",
          name: "Authorization Level",
          type: "dropdown",
          required: false,
          visibility: "Intern",
          placeholder: "autorisatieniveau",
          options: authorizationLevelTypeOptions,
          infoText:
            "Open, Intern of Extra autorisatie. De gekozen waarde wordt opgeslagen bij de metadataset en heeft geen invloed op de toegang tot de metadataset.",
        },
        {
          label: "Status",
          id: "status",
          name: "Status",
          type: "dropdown",
          required: false,
          placeholder: "status",
          options: statusTypeOptions,
        },
        {
          label: "Toon in dataportaal voor niet-ingelogde gebruikers",
          id: "show_in_overview",
          name: "showInOverview",
          type: "checkbox",
          required: false,
          visibility: "Publiek",
          infoText:
            "Toon de metadataset in het dataportaal voor niet-ingelogde gebruikers. Ingelogde gebruikers zien gepubliceerde metadatasets altijd.",
        },
      ],
    },
    restrictions: {
      label: "Beperkingen",
      questions: [
        {
          label: "Juridische toegangsrestricties",
          id: "access_constraints",
          name: "Legal Access Restrictions",
          type: "dropdown",
          required: false,
          visibility: "Publiek",
          options: accessConstraintsTypeOptions,
          placeholder: "toegangsrestrictie",
          infoText: "Juridische toegangsrestricties die van toepassing zijn op de dataset.",
        },
        {
          label: "Overige beperkingen",
          id: "other_constraints",
          name: "Other Restrictions",
          type: "dropdown",
          required: false,
          visibility: "Publiek",
          placeholder: "beperking",
          options: otherConstraintsTypeOptions,
          infoText:
            "Selecteer een optie wanneer je bij juridische toegangsrestricties 'Overige beperkingen' hebt gekozen.",
        },
        {
          label: "Gebruiksbeperkingen",
          id: "usage_constraints",
          name: "Usage Restrictions",
          type: "text",
          required: false,
          visibility: "Publiek",
          infoText:
            "In dit veld geef je aan waarvoor de dataset niet mag of kan worden gebruikt. Bijvoorbeeld: Niet gebruiken voor navigatie.",
        },
      ],
    },
    responsible_organization: {
      label: "Verantwoordelijke metadata",
      questions: [
        {
          label: "E-mailadres aanspreekpunt",
          id: "meta_email_internal",
          name: "Responsible Email Internal",
          type: "text",
          required: false,
          visibility: "Intern",
          infoText: "Het e-mailadres van het interne aanspreekpunt van de verantwoordelijke van de metadata.",
        },
        {
          label: "Organisatie",
          id: "meta_organization",
          name: "Responsible Organization",
          type: "text",
          required: false,
          visibility: "Publiek",
          infoText:
            "De naam van de organisatie verantwoordelijk voor de metadata. Gebruik de volledig uitgeschreven naam van de verantwoordelijke organisatie. Bijvoorbeeld: Gemeente Purmerend.",
        },
        {
          label: "E-mailadres verantwoordelijke",
          id: "meta_email_person_responsible",
          name: "Responsible Email Public",
          type: "text",
          required: false,
          visibility: "Publiek",
          infoText:
            "Het e-mailadres van de organisatie verantwoordelijk voor de metadata. Gebruik bij voorkeur een functioneel e-mailadres.",
        },
        {
          label: "Rol verantwoordelijke",
          id: "meta_role_person_responsible",
          name: "Responsible Role",
          type: "dropdown",
          options: roleTypeOptions,
          required: false,
          visibility: "Publiek",
          placeholder: "rol",
          infoText: "De rol van de verantwoordelijke over de metadata.",
        },
      ],
    },
  };
};

// Lifecycle
onMounted(async () => {
  loading.value = true;

  await Promise.all([getMetadataset()]);

  sections.value = getSections();
  loading.value = false;
});
</script>
