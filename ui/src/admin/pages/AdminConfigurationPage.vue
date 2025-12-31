<template>
  <div class="container __admin">
    <h1 class="font-weight-normal">Configuratie</h1>
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

<script>
import AdminFormSections from "@/admin/components/AdminFormSections.vue";
import Cookies from "js-cookie";
import Spinner from "@/components/Spinner.vue";

export default {
  name: "AdminConfigurationPage",
  components: { Spinner, AdminFormSections },
  props: {},
  data() {
    return {
      sections: {},
      initialValues: {},
      currentValues: {},
      uploadedFile: null,
      loading: false,
    };
  },
  created() {
    this.loading = true;
    Promise.all([this.getConfigurations()]).then(() => {
      this.sections = this.getSections();
      this.loading = false;
    });
  },
  methods: {
    async getConfigurations() {
      const result = await fetch(`/atlas/api/v1/configurations/`, {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch configurations");
        return;
      }

      let data = await result.json();
      this.initialValues = this.constructFormValues(data);
    },
    async saveConfiguration(currentValues, continueEditing = false) {
      try {
        let fetchUrl = `/atlas/api/v1/configurations/`;

        const data = new FormData();

        Object.entries(currentValues).forEach(([key, value]) => {
          data.append(key, value);
        });

        const result = await fetch(fetchUrl, {
          method: "POST",
          credentials: "same-origin",
          headers: {
            "X-CSRFToken": Cookies.get("csrftoken"),
          },
          body: data,
        });
        if (result.ok) {
          if (!continueEditing) {
            this.$router.push(`/`);
          }

          this.$toast.add({
            severity: "success",
            summary: "Configuratie opgeslagen",
            detail: "De configuratie is succesvol opgeslagen.",
            life: 3000,
          });
        }
      } catch (e) {
        console.error("An unexpected error occurred:", e);
      }
    },
    constructFormValues(data) {
      return data.reduce((formValues, item) => {
        formValues[item.key] = item.value === "true" ? true : item.value === "false" ? false : item.value;
        return formValues;
      }, {});
    },
    getSections() {
      return {
        organization: {
          label: "Organisatie",
          questions: [
            {
              label: "Naam organisatie",
              id: "ORGANIZATION_NAME",
              name: "organizationName",
              type: "text",
              required: true,
            },
            {
              id: "ORGANIZATION_LOGO",
              name: "organizationLogo",
              type: "image",
              label: "Logo van de organisatie",
            },
            {
              label: "Favicon URL",
              id: "FAVICON_URL",
              name: "faviconUrl",
              type: "text",
              infoText: "Configureer een eigen favicon. Voorbeeld: http://www.organization.com/favicon.ico",
            },
            {
              label: "Disclaimer",
              id: "DISCLAIMER",
              name: "disclaimer",
              type: "text",
              multiLine: true,
              infoText: "Inhoud van de disclaimer die getoond wordt",
            },
          ],
        },
        mapConfiguration: {
          label: "Kaartconfiguratie",
          questions: [
            {
              label: "Centrum X-coördinaat",
              id: "POSITION_CENTER_X",
              name: "positionCenterX",
              type: "decimal",
              step: 0.1,
              required: true,
              infoText: "Het centrum X-coördinaat van de opstart-positie",
            },
            {
              label: "Centrum Y-coördinaat",
              id: "POSITION_CENTER_Y",
              name: "positionCenterY",
              type: "decimal",
              step: 0.1,
              required: true,
              infoText: "Het centrum Y-coördinaat van de opstart-positie",
            },
            {
              label: "Zoomniveau",
              id: "POSITION_ZOOM",
              name: "positionZoom",
              type: "decimal",
              step: 0.1,
              required: true,
              infoText: "Het zoomniveau van de opstart-positie",
            },
            {
              label: "Doorzoek deze gemeentes",
              id: "SUGGEST_MUNICIPALITIES",
              name: "suggestMunicipalities",
              required: true,
              infoText:
                "Een komma-gescheiden lijst van gemeenten om adressen in te zoeken (voor auto-aanvul functionaliteit)",
            },
            {
              label: "Standaard kaartgebied",
              id: "MAP_AREA",
              name: "mapArea",
              type: "text",
              infoText: "Configureer een gebied dat standaard uitgelicht wordt op de kaart",
            },
          ],
        },
        matomo: {
          label: "Matomo",
          questions: [
            {
              label: "Matomo Site Url",
              id: "MATOMO_URL",
              name: "matomoUrl",
              type: "text",
              infoText: "Configureer de URL van Matomo om statistieken bij te houden",
            },
            {
              label: "Matomo Site Id",
              id: "MATOMO_SITE_ID",
              name: "matomoSiteId",
              type: "text",
              infoText: "Configureer het site ID van Matomo om statistieken bij te houden",
            },
          ],
        },
        features: {
          label: "Features",
          questions: [
            {
              label: "Portaalfunctionaliteit",
              id: "FEATURE_PORTAL",
              name: "featurePortal",
              type: "checkbox",
            },
            {
              label: "Printfunctionaliteit",
              id: "FEATURE_PRINT",
              name: "featurePrint",
              type: "checkbox",
            },
            {
              label: "Sorteer kaartlagen in de viewer",
              id: "FEATURE_SORT_LAYER",
              name: "featureSortLayer",
              type: "checkbox",
            },
            {
              label: "Zet oude beheerpaneel uit",
              id: "FEATURE_DISABLE_ADMIN1",
              name: "featureDisableAdmin1",
              type: "checkbox",
            },
            {
              label: "Kaartlaagvergelijk functionaliteit op hoofdkaart",
              id: "FEATURE_COMPARE_LAYERS",
              name: "featureCompareLayers",
              type: "checkbox",
            },
            {
              label: "Tekenfunctionaliteit op hoofdkaart",
              id: "FEATURE_DRAW",
              name: "featureDraw",
              type: "checkbox",
            },
            {
              label: "CRUD functionaliteit op hoofdkaart",
              id: "FEATURE_EDIT_LAYER_FEATURES",
              name: "featureAddFeature",
              type: "checkbox",
            },
          ],
        },
        portalConfiguration: {
          label: "Portaal configuratie",
          questions: [
            {
              id: "ORGANIZATION_IMAGE",
              name: "organizationImage",
              type: "image",
              label: "Organisatie specifieke afbeelding die bovenaan de portaal pagina getoond wordt",
            },
            {
              id: "ORGANIZATION_PRIMARY_COLOR",
              name: "organizationPrimaryColor",
              type: "color",
              label: "Primaire kleur van de organisatie",
              infoText: "Klik op de kleur om de kleur aan te passen. NB: voor nu alleen beschikbaar in HEX",
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
      };
    },
  },
};
</script>

<style scoped></style>
