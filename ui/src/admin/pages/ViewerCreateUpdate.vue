<template>
  <div class="container __admin">
    <h1 class="font-weight-normal">Viewer wijzigen</h1>
    <AdminFormSections
      ref="formSections"
      :sections="sections"
      :initial-values="initialValues"
      :compact-layout="false"
      :form-object="'viewers'"
      :object-specific-save="saveViewer"
    />
  </div>
</template>

<script>
import AdminFormSections from "@/admin/components/AdminFormSections.vue";

export default {
  name: "ViewerCreateUpdate",
  components: {
    AdminFormSections,
  },
  data() {
    return {
      sections: {},
      initialValues: {},
      currentValues: {},
      viewerTypes: [],
    };
  },
  created() {
    this.viewerTypes = [
      { id: "GOOGLE_MAPS", label: "Google Maps" },
      { id: "STREET_SMART", label: "Street Smart" },
      { id: "OBLIQUO", label: "Obliquo" },
      { id: "IFRAME", label: "Iframe" },
      { id: "BUTTON", label: "Knop naar nieuw tabblad" },
    ];

    this.getViewer();
    this.sections = this.getSections();
  },
  methods: {
    async getViewer() {
      const result = await fetch(`/atlas/api/v1/viewers/${this.$route.params.id}/`, {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch viewer");
      }

      this.initialValues = await result.json();
    },
    async saveViewer(currentValues) {
      const url = `/atlas/api/v1/viewers/${this.$route.params.id}/`;

      try {
        const result = await this.$refs.formSections.sendSaveRequest(url, "PATCH", currentValues);

        if (result.ok) {
          this.$router.push(`/viewers`);
        }
      } catch (e) {
        console.error("An unexpected error occurred:", e);
      }
    },
    getSections() {
      return {
        general: {
          label: "Algemene gegevens",
          questions: [
            {
              label: "Label",
              id: "label",
              name: "Label",
              type: "text",
              required: true,
            },
            {
              label: "Sortering",
              id: "ordering",
              name: "Ordering",
              type: "decimal",
              required: false,
              step: 1,
            },
          ],
        },
        viewer: {
          label: "Viewer instellingen",
          questions: [
            {
              label: "Type",
              id: "type",
              name: "Type",
              type: "dropdown",
              required: true,
              placeholder: "bron",
              options: this.viewerTypes,
            },
            {
              label: "Username",
              id: "username",
              name: "Username",
              type: "text",
              required: false,
            },
            {
              label: "Password",
              id: "password",
              name: "Password",
              type: "text",
              required: false,
            },
            {
              label: "Api Key",
              id: "api_key",
              name: "ApiKey",
              type: "text",
              required: false,
            },
            {
              label: "URL",
              id: "url",
              name: "Url",
              type: "text",
              required: false,
            },
            {
              label: "Is oblique",
              id: "is_oblique",
              name: "IsOblique",
              type: "checkbox",
              required: false,
            },
          ],
        },
        access: {
          label: "Toegang",
          questions: [
            {
              label: "Alleen zichtbaar voor ingelogde gebruikers en interne omgeving",
              id: "internal",
              name: "Internal",
              type: "checkbox",
              required: false,
              infoText:
                "Hou er rekening mee dat de gebruikernaam, het wachtwoord of de API key gedeeld wordt met het publieke internet op het moment dat deze optie uit staat.",
            },
          ],
        },
      };
    },
  },
};
</script>
