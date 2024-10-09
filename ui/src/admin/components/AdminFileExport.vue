<template>
  <div class="export-wrapper">
    <p v-if="selectedRows.length > 0">
      Weet u zeker dat u de volgende {{ objectName.pluralName.toLowerCase() }} wilt exporteren?
    </p>
    <p v-else>Er zijn geen {{ objectName.pluralName.toLowerCase() }} geselecteerd.</p>
    <ul v-if="!isAllSelected" class="selected-rows">
      <li v-for="row in selectedRows" :key="row.id">- {{ row.title }}</li>
    </ul>
    <p v-if="isAllSelected">Alle {{ objectName.pluralName.toLowerCase() }}.</p>
    <div class="admin-btn-wrapper">
      <button class="button __secondary_admin" type="button" @click="closeFormModal">Annuleer</button>
      <button class="button __primary_admin" type="button" :disabled="!selectedRows" @click="exportItems">
        Exporteer
      </button>
    </div>
  </div>
</template>

<script>
import Cookies from "js-cookie";
import { getDateString } from "@/utils/date-formatter";

export default {
  name: "AdminFileExport",
  props: {
    selectedRows: Array,
    objectName: Object,
    isAllSelected: Boolean,
  },
  data() {
    return {};
  },
  methods: {
    closeFormModal() {
      this.$emit("close");
    },
    getObjectPath(objectType) {
      switch (objectType) {
        case "kaartlagen":
          return "layers";
        case "layers":
          return "layers";
        case "bronnen":
          return "sources";
        case "sources":
          return "sources";
        case "categorieën":
          return "categories";
        case "categories":
          return "categories";
        case "kaarten":
          return "maps";
        case "maps":
          return "maps";
        case "themes":
          return "themes";
        case "datasets":
          return "datasets";
        case "tables":
          return "tables";
        case "viewers":
          return "viewers";
        case "authorizations":
          return "authorizations";
      }
    },
    async exportItems() {
      const ids = { ids: this.selectedRows.map((row) => row.id) };

      const data = JSON.stringify(this.isAllSelected ? { ids: [] } : ids);

      let fetchUrl = `/atlas/api/v1/${this.getObjectPath(this.objectName.apiName)}/export/`;

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
    },
  },
};
</script>

<style scoped>
.selected-rows {
  max-height: 70vh;
  overflow: auto;
  overscroll-behavior: contain;
}
</style>
