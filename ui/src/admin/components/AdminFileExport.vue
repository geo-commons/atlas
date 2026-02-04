<template>
  <div class="export-wrapper">
    <div v-if="exportType === EDialogTypes.Export">
      <p>Weet u zeker dat u de volgende {{ objectName.pluralName.toLowerCase() }} wilt exporteren?</p>
      <ul class="selected-rows">
        <li v-for="row in selectedRows" :key="row.id">- {{ row.title }}</li>
      </ul>
    </div>
    <p v-else-if="exportType === EDialogTypes.ExportAll">
      Alle beschikbare {{ objectName.pluralName.toLowerCase() }} exporteren.
    </p>

    <div class="admin-btn-wrapper">
      <Button type="button" severity="secondary" outlined @click="closeFormModal"> Annuleer </Button>
      <Button type="button" :loading="isLoading" @click="exportItems"> Exporteer </Button>
    </div>
  </div>
</template>

<script>
import Cookies from "js-cookie";
import { getDateString } from "@/utils/date-formatter";
import { EDialogTypes } from "@/types/dialog";
import { useToast } from "primevue";

export default {
  name: "AdminFileExport",
  props: {
    selectedRows: Array,
    objectName: Object,
    exportType: EDialogTypes,
  },
  emits: ["close", "export-successful"],
  data() {
    return {
      exportSuccessful: false,
      toast: useToast(),
      isLoading: false,
    };
  },
  computed: {
    EDialogTypes() {
      return EDialogTypes;
    },
  },
  methods: {
    closeFormModal() {
      this.$emit("close", "export-successful");
    },
    async exportItems() {
      this.isLoading = true;

      const ids = { ids: this.selectedRows.map((row) => row.id) };

      const data = JSON.stringify(this.exportType === EDialogTypes.ExportAll ? { ids: [] } : ids);

      let fetchUrl = `/atlas/api/v1/${this.objectName.apiName}/export/`;

      try {
        const result = await fetch(fetchUrl, {
          method: "POST",
          credentials: "same-origin",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": Cookies.get("csrftoken"),
          },
          body: data,
        });

        if (!result.ok) {
          throw new Error("Export failed: ", result.error());
        }

        const blob = await result.blob();
        const fileBlob = window.URL.createObjectURL(blob);

        // create <a> element dynamically
        let fileLink = document.createElement("a");
        fileLink.href = fileBlob;
        fileLink.setAttribute("target", "_blank");

        const exportName = this.objectName.apiName + "_" + getDateString();
        fileLink.download = exportName + ".json";

        // simulate click
        fileLink.click();
        window.URL.revokeObjectURL(fileBlob);

        this.isLoading = false;
        this.closeFormModal();
        this.$emit("export-successful");

        this.toast.add({
          severity: "success",
          summary: "Exporteren gelukt",
          detail: `Het exporteren van ${this.objectName.pluralName.toLowerCase()} is gelukt`,
          life: 5000,
        });
      } catch (e) {
        console.error(e);

        this.toast.add({
          severity: "error",
          summary: "Exporteren mislukt",
          detail: `Het exporteren van ${this.objectName.pluralName.toLowerCase()} is niet gelukt`,
          life: 5000,
        });
      }
    },
  },
};
</script>

<style scoped>
.selected-rows {
  max-height: 55vh;
  overflow: auto;
  overscroll-behavior: contain;
}
</style>
