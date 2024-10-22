<template>
  <div class="export-wrapper">
    <p v-if="exportSuccessful" class="tw-text-green-700 tw-font-bold">Succesvol geëxporteerd!</p>
    <div v-else-if="exportType === EDialogTypes.Export && selectedRows.length > 0">
      <p>Weet u zeker dat u de volgende {{ objectName.pluralName.toLowerCase() }} wilt exporteren?</p>
      <ul class="selected-rows">
        <li v-for="row in selectedRows" :key="row.id">- {{ row.title }}</li>
      </ul>
    </div>
    <p v-else-if="exportType === EDialogTypes.ExportAll">
      Alle beschikbare {{ objectName.pluralName.toLowerCase() }} exporteren.
    </p>
    <p v-else>Er zijn geen {{ objectName.pluralName.toLowerCase() }} geselecteerd.</p>

    <div class="admin-btn-wrapper">
      <button v-if="!exportSuccessful" class="button __secondary_admin" type="button" @click="closeFormModal">
        Annuleer
      </button>
      <button
        v-if="!exportSuccessful"
        class="button __primary_admin"
        type="button"
        :disabled="exportType === EDialogTypes.Export && !selectedRows.length"
        @click="exportItems"
      >
        Exporteer
      </button>
      <button v-else class="button __primary_admin" type="button" @click="closeFormModal">Sluit</button>
    </div>
  </div>
</template>

<script>
import Cookies from "js-cookie";
import { getDateString } from "@/utils/date-formatter";
import { EDialogTypes } from "@/types/dialog";

export default {
  name: "AdminFileExport",
  props: {
    selectedRows: Array,
    objectName: Object,
    exportType: EDialogTypes,
  },
  data() {
    return {
      exportSuccessful: false,
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
      const ids = { ids: this.selectedRows.map((row) => row.id) };

      const data = JSON.stringify(this.exportType === EDialogTypes.ExportAll ? { ids: [] } : ids);

      let fetchUrl = `/atlas/api/v1/${this.objectName.apiName}/export/`;

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
        console.error("Export failed:", result.error());
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
      this.exportSuccessful = true;
      this.$emit("export-successful");
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
