<template>
  <vee-form @submit="formSubmit">
    <div class="template-form">
      <div class="layer-settings">
        <div class="layer-setting">
          <label class="question-label" for="source">Bron</label>
          <vee-field
            id="source"
            v-model="template.source_id"
            as="select"
            name="source_id"
            class="__admin config-select-wrapper"
            rules="required"
          >
            <option disabled value="-1">Selecteer bron</option>
            <option v-for="source in sources" :key="source.id" :value="source.id">
              {{ source.label }}
            </option>
          </vee-field>
          <vee-error-message class="form-error" name="source_id" />
        </div>
        <div class="layer-setting">
          <label class="question-label" for="endpoint">Endpoint</label>
          <vee-field id="endpoint" v-model.trim="template.endpoint" name="endpoint" type="text" rules="required" />
          <vee-error-message class="form-error" name="endpoint" />
        </div>
        <div class="layer-setting">
          <label class="question-label" for="Method">Methode</label>
          <vee-field
            id="method"
            v-model="template.method"
            as="select"
            name="method"
            class="__admin config-select-wrapper"
            rules="required"
          >
            <option disabled value="-1">Selecteer methode</option>
            <option v-for="method in methods" :key="method.id" :value="method.id">
              {{ method.label }}
            </option>
          </vee-field>
          <vee-error-message class="form-error" name="method" />
        </div>
        <div class="layer-setting">
          <label class="question-label" for="title">Titel</label>
          <vee-field id="title" v-model.trim="template.title" name="title" type="text" rules="required" />
          <vee-error-message class="form-error" name="title" />
        </div>
        <div class="layer-setting">
          <label class="question-label" for="list">Tabel veld met lijst</label>
          <vee-field id="list" v-model.trim="template.list" name="list" type="text" rules="required" />
          <vee-error-message class="form-error" name="list" />
        </div>
      </div>
      <div>
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
      <button class="button __secondary_admin" type="button" @click="cancel()">Annuleer</button>
      <button class="button __primary_admin" type="submit">
        {{ template.edit ? "Pas toe" : "Voeg toe" }}
      </button>
    </div>
  </vee-form>
</template>

<script>
import { updateMultiLineField } from "@/utils/admin-form-helpers";
import { ErrorMessage as VeeErrorMessage, Field as VeeField, Form as VeeForm } from "vee-validate";
import { getAllObjects } from "@/utils/api-helpers";

export default {
  name: "TemplateForm",
  components: { VeeForm, VeeField, VeeErrorMessage },
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
      return this.template.headers ? this.template.headers.join("\n") : "";
    },
    fields() {
      return this.template.fields ? this.template.fields.join("\n") : "";
    },
  },
  async created() {
    this.template = {
      ...this.initialTemplate,
    };
    this.methods = [
      { id: "GET", label: "GET" },
      { id: "POST", label: "POST" },
    ];
    this.sources = await this.getSources();
  },
  methods: {
    updateMultiLineField,
    formSubmit(data) {
      const finalData = { ...this.template, ...data };
      this.$emit("save", finalData);
    },
    async getSources() {
      const url = getAllObjects("/atlas/api/v1/sources/");
      const result = await fetch(url, {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch sources");
      }

      const response = await result.json();

      return response.results.map((source) => {
        return { id: source.id, label: source.title, url: source.url, type: source.source_type };
      });
    },
    cancel() {
      this.$emit("close");
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

.question-label {
  font-weight: var(--font-weight-bold);
}
</style>
