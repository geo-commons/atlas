<template>
  <vee-form @submit="formSubmit">
    <div class="template-form">
      <div class="layer-settings">
        <div class="layer-setting">
          <label class="question-label" for="source">Bron</label>
          <vee-field
            id="source"
            v-slot="{ value, handleChange, handleBlur }"
            v-model="template.source_id"
            name="source_id"
            rules="required"
          >
            <Select
              :model-value="value"
              :options="sources"
              option-label="label"
              option-value="id"
              placeholder="Selecteer een bron"
              filter
              filter-placeholder="Zoek een bron"
              show-clear
              @update:model-value="handleChange"
              @blur="handleBlur"
            />
          </vee-field>
          <vee-error-message class="form-error" name="source_id" />
        </div>
        <div class="layer-setting">
          <label class="question-label" for="endpoint">Endpoint</label>
          <vee-field
            id="endpoint"
            v-slot="{ value, handleChange, handleBlur }"
            v-model.trim="template.endpoint"
            name="endpoint"
            type="text"
            rules="required"
          >
            <InputText :model-value="value" @update:modelValue="handleChange" @blur="handleBlur" />
          </vee-field>
          <vee-error-message class="form-error" name="endpoint" />
        </div>
        <div class="layer-setting">
          <label class="question-label" for="Method">Methode</label>
          <vee-field
            id="method"
            v-slot="{ value, handleChange, handleBlur }"
            v-model="template.method"
            name="method"
            rules="required"
          >
            <Select
              :model-value="value"
              :options="methods"
              option-label="label"
              option-value="id"
              placeholder="Selecteer een methode"
              filter
              filter-placeholder="Zoek een methode"
              show-clear
              @update:model-value="handleChange"
              @blur="handleBlur"
            />
          </vee-field>
          <vee-error-message class="form-error" name="method" />
        </div>
        <div class="layer-setting">
          <label class="question-label" for="title">Titel</label>
          <vee-field
            id="title"
            v-slot="{ value, handleChange, handleBlur }"
            v-model.trim="template.title"
            name="title"
            type="text"
            rules="required"
          >
            <InputText :model-value="value" @update:modelValue="handleChange" @blur="handleBlur" />
          </vee-field>
          <vee-error-message class="form-error" name="title" />
        </div>
        <div class="layer-setting">
          <label class="question-label" for="list">Tabel veld met lijst</label>
          <vee-field
            id="list"
            v-slot="{ value, handleChange, handleBlur }"
            v-model.trim="template.list"
            name="list"
            type="text"
          >
            <InputText :model-value="value" @update:modelValue="handleChange" @blur="handleBlur" />
          </vee-field>
          <vee-error-message class="form-error" name="list" />
        </div>
      </div>
      <div class="tw-flex tw-flex-col tw-gap-2">
        <div class="layer-setting">
          <label class="question-label" for="headers">Tabel kopjes</label>
          <Textarea
            id="headers"
            name="headers"
            rows="6"
            :model-value="headers"
            @update:modelValue="(value) => updateMultiLineField(template, 'headers', value)"
          />
        </div>
        <div class="layer-setting">
          <label class="question-label" for="fields">Tabel velden</label>
          <Textarea
            id="fields"
            name="fields"
            rows="6"
            :model-value="fields"
            @update:modelValue="(value) => updateMultiLineField(template, 'fields', value)"
          />
        </div>
        <div class="layer-setting">
          <label class="question-label" for="template">Vrij veld template</label>
          <Textarea id="template" v-model="template.template" name="template" rows="6" />
        </div>
      </div>
    </div>
    <div class="config-btn-wrapper">
      <Button text severity="secondary" class="!tw-text-sm !tw-font-semibold" type="button" @click="cancel()">
        Annuleer
      </Button>
      <Button class="!tw-text-sm !tw-font-semibold" type="submit">
        {{ template.edit ? "Pas toe" : "Voeg toe" }}
      </Button>
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
