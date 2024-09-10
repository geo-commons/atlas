<template>
  <div class="container __admin">
    <h1 class="font-weight-normal">Log</h1>
    <AdminFormSections
      ref="formSections"
      :sections="sections"
      :initial-values="initialValues"
      :compact-layout="false"
      :form-object="'logs'"
      :disable-create-and-update="true"
    />
  </div>
</template>

<script>
/* TODO: Implement AdminFormSummary in the future, in the case you only have read-only data to show a whole Form component is unneccessary */
import AdminFormSections from "@/admin/components/AdminFormSections.vue";

export default {
  name: "LogView",
  components: {
    AdminFormSections,
  },
  data() {
    return {
      sections: {},
      initialValues: {},
      currentValues: {},
    };
  },
  created() {
    this.getLog();
    this.sections = this.getSections();
  },
  methods: {
    async getLog() {
      const result = await fetch(`/atlas/api/v1/logs/${this.$route.params.id}/`, {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch log");
      }

      this.initialValues = await result.json();
    },
    getSections() {
      return {
        general: {
          label: "Algemene gegevens",
          questions: [
            {
              label: "Gebruikersnaam",
              id: "username",
              name: "Username",
              type: "label",
            },
            {
              label: "E-mail",
              id: "email",
              name: "Email",
              type: "label",
            },
            {
              label: "User agent",
              id: "user_agent",
              name: "UserAgent",
              type: "label",
            },
            {
              label: "Ip-adres",
              id: "ip",
              name: "ip",
              type: "label",
            },
          ],
        },
        log: {
          label: "Log",
          questions: [
            {
              label: "Bron",
              id: "source",
              name: "Source",
              type: "label",
            },
            {
              label: "Resource",
              id: "resource",
              name: "Resource",
              type: "label",
            },
            {
              label: "Parameters",
              id: "params",
              name: "Params",
              type: "label",
            },
            {
              label: "Datum",
              id: "time_created",
              name: "Date",
              type: "display_date",
            },
          ],
        },
      };
    },
  },
};
</script>
