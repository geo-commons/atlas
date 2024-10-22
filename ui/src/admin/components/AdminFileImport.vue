<template>
  <div class="import-wrapper">
    <h4 v-if="importFailed" class="warning-text">
      Er is iets fout gegaan bij het importeren, controleer uw data en probeer het opnieuw.
    </h4>

    <div v-if="errors.length" class="error-wrapper">
      <h4>Foutmelding(en):</h4>
      <ul>
        <li v-for="error in errors" :key="error">{{ error }}</li>
      </ul>
    </div>

    <div v-if="!importSuccessful">
      <input id="file" ref="fileInput" type="file" name="file" class="inputfile" />
      <label for="file" class="button __primary_admin __import">
        <ArrowDownTrayIcon class="icon" />
        <span ref="fileLabelText">Selecteer een bestand om te importeren</span>
      </label>
    </div>
    <h3 v-else class="successful-import-text">Importeren geslaagd!</h3>

    <div v-if="uploadedFileResponse && !importSuccessful" class="selected-rows">
      <ul>
        <li v-for="row in uploadedFileResponse.rows" :key="row">
          <h4 class="upload-row-title" v-html="getRowTitle(row)"></h4>
          <div class="upload-content" v-html="getHTML(row)"></div>
        </li>
      </ul>
    </div>

    <div class="admin-btn-wrapper">
      <button
        class="button"
        :class="importSuccessful ? '__primary_admin' : '__secondary_admin'"
        type="button"
        @click="closeFormModal"
      >
        {{ importSuccessful ? "Sluit" : "Annuleer" }}
      </button>
      <button
        v-if="!importSuccessful"
        :disabled="!uploadedFile"
        class="button __primary_admin"
        type="button"
        @click="importFile"
      >
        Importeer
      </button>
    </div>
  </div>
</template>

<script>
// Note: for now supporting 1 file is probably enough.
import ArrowDownTrayIcon from "@/assets/icons/arrow-down-tray-icon.svg";
import Cookies from "js-cookie";

export default {
  name: "AdminFileImport",
  components: { ArrowDownTrayIcon },
  props: {
    objectName: Object,
  },
  data() {
    return {
      uploadedFile: null,
      uploadedFileResponse: null,
      importSuccessful: false,
      importFailed: false,
      errors: [],
    };
  },
  mounted() {
    this.$refs.fileInput.addEventListener("change", this.onFileUpload);
  },
  methods: {
    getHTML(row) {
      if (!row.diff) {
        return "";
      }

      return row.diff.join("");
    },
    getRowTitle(row) {
      if (row.diff && row.diff[3]) {
        return row.diff[3];
      }
      return "";
    },
    closeFormModal() {
      this.$emit("close");
    },
    onFileUpload() {
      this.uploadedFile = this.$refs.fileInput.files[0];

      if (this.uploadedFile) {
        this.setLabelText();
        this.fetchImportData(true);
      }
    },
    setLabelText() {
      const file = this.$refs.fileInput.files[0];
      this.$refs.fileLabelText.innerHTML = file?.name;
    },
    getErrors(response) {
      response.rows.forEach((row) => {
        row.errors.forEach((error) => {
          this.errors.push(error.error);
        });
      });
    },
    async fetchImportData(dryRun = false) {
      if (!this.uploadedFile) {
        console.error("No file available.");
        return;
      }

      const data = new FormData();
      data.append("file", this.uploadedFile);

      let fetchUrl = `/atlas/api/v1/${this.objectName.apiName}/import/`;

      if (dryRun) {
        fetchUrl += "?dry_run=1";
      }

      const result = await fetch(fetchUrl, {
        method: "POST",
        credentials: "same-origin",
        headers: {
          "X-CSRFToken": Cookies.get("csrftoken"),
        },
        body: data,
      });

      if (!result.ok) {
        console.error("Import failed");
        this.importFailed = true;
        return;
      }

      const response = await result.json();

      if (response.has_errors) {
        this.importFailed = true;
        this.uploadedFileResponse = null;
        this.getErrors(response);
        return;
      }

      this.importFailed = false;
      this.uploadedFileResponse = response;
      return result;
    },
    async importFile() {
      const response = await this.fetchImportData();

      if (response.ok) {
        this.importSuccessful = true;
        this.$emit("import-successful");
      }
    },
  },
};
</script>

<style scoped>
.__import {
  width: fit-content;
  cursor: pointer;
}

.inputfile:focus + label {
  outline: 2px solid var(--color-primary);
  outline-offset: 1px;
}

.inputfile {
  width: 0.1px;
  height: 0.1px;
  opacity: 0;
  overflow: hidden;
  position: absolute;
  z-index: -1;
}

.selected-rows {
  max-height: 55vh;
  overflow: auto;
  overscroll-behavior: contain;
}

.upload-content {
  padding: 8px 0;
  display: flex;
  flex-direction: column;
}

.successful-import-text {
  color: var(--color-succesful);
}

.upload-row-title {
  margin-bottom: 0;
}

.error-wrapper {
  padding-bottom: 28px;
}
</style>
