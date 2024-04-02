<template>
  <div>
    <div class="template-form">
      <div class="layer-settings">
        <div class="layer-setting">
          <label class="question-label" for="source">Bron</label>
          <select id="source" v-model="template.source.id" name="source" class="config-select-wrapper">
            <option disabled value="-1">Selecteer bron</option>
            <option v-for="source in sources" :key="source.id" :value="source.id">
              {{ source.label }}
            </option>
          </select>
        </div>
        <div class="layer-setting">
          <label class="question-label" for="endpoint">Endpoint</label>
          <input id="endpoint" v-model.trim="template.endpoint" name="endpoint" type="text" />
        </div>
        <div class="layer-setting">
          <label class="question-label" for="Method">Methode</label>
          <select id="method" v-model="template.method" name="method" class="config-select-wrapper">
            <option disabled value="-1">Selecteer methode</option>
            <option v-for="method in methods" :key="method.id" :value="method.id">
              {{ method.label }}
            </option>
          </select>
        </div>
        <div class="layer-setting">
          <label class="question-label" for="title">Titel</label>
          <input id="title" v-model.trim="template.title" name="title" type="text" />
        </div>
        <div class="layer-setting">
          <label class="question-label" for="list">Tabel veld met lijst</label>
          <input id="list" v-model.trim="template.list" name="list" type="text" />
        </div>
      </div>
      <div class="">
        <div class="layer-setting">
          <label class="question-label" for="headers">Tabel kopjes</label>
          <textarea
            id="headers"
            name="headers"
            rows="6"
            :value="headers"
            @change="(e) => updateMultiLineField(template, 'headers', e.target.value)"
          />
        </div>
        <div class="layer-setting">
          <label class="question-label" for="fields">Tabel velden</label>
          <textarea
            id="fields"
            name="fields"
            rows="6"
            :value="fields"
            @change="(e) => updateMultiLineField(template, 'fields', e.target.value)"
          />
        </div>
        <div class="layer-setting">
          <label class="question-label" for="template">Vrij veld template</label>
          <textarea id="template" v-model="template.template" name="template" rows="6" />
        </div>
      </div>
    </div>
    <div class="config-btn-wrapper">
      <button class="button __secondary" type="button" @click="cancel()">Annuleer</button>
      <button class="button __primary" type="submit" @click="save">Opslaan</button>
    </div>
  </div>
</template>

<script>
import { updateMultiLineField } from "@/utils/admin-form-helpers";

export default {
  name: "TemplateForm",
  props: {
    initialTemplate: Object,
  },
  data() {
    return {
      template: null,
      sources: null,
      methods: [],
    };
  },
  computed: {
    headers() {
      return this.template.headers.join("\n");
    },
    fields() {
      return this.template.fields.join("\n");
    },
  },
  async created() {
    this.template = { ...this.initialTemplate };
    this.methods = [
      { id: "GET", label: "GET" },
      { id: "POST", label: "POST" },
    ];
    this.sources = await this.getSources();
  },
  methods: {
    updateMultiLineField,
    async getSources() {
      const result = await fetch("/atlas/api/v1/sources/", {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch sources");
      }

      const response = await result.json();

      return response.map((source) => {
        return { id: source.id, label: source.title, url: source.url, type: source.source_type };
      });
    },

    cancel() {
      this.$emit("close");
    },
    save() {
      this.$emit("save", this.template);
    },
  },
};
</script>

<style scoped>
.template-form {
  display: grid;
  grid-template-columns: 1fr 1fr;
  column-gap: 36px;
}

.layer-settings {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.layer-setting {
  display: flex;
  flex-direction: column;
}

.config-btn-wrapper {
  display: flex;
  justify-content: flex-end;
  gap: 20px;
  padding-top: 30px;
}

.config-select-wrapper {
  height: 40px;
  width: 100%;
}
</style>
