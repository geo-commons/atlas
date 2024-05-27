<template>
  <vee-form @submit="submitForm">
    <div class="linked-data-form">
      <div class="layer-settings">
        <div class="layer-setting">
          <label class="question-label" for="title">Titel</label>
          <vee-field id="title" v-model.trim="linkedData.title" name="title" type="text" rules="required" />
          <vee-error-message class="form-error" name="title" />
        </div>
        <div class="layer-setting">
          <label class="question-label" for="name">Laag naam</label>
          <vee-field id="name" v-model.trim="linkedData.name" name="name" type="text" rules="required" />
          <vee-error-message class="form-error" name="name" />
        </div>
        <div class="layer-setting">
          <label class="question-label" for="url">URL</label>
          <vee-field id="url" v-model.trim="linkedData.url" name="url" type="text" rules="required" />
          <vee-error-message class="form-error" name="url" />
        </div>
        <div class="layer-setting">
          <label class="question-label" for="source_key">Bronsleutel</label>
          <vee-field
            id="source_key"
            v-model.trim="linkedData.source_key"
            name="source_key"
            type="text"
            rules="required"
          />
          <vee-error-message class="form-error" name="source_key" />
        </div>
        <div class="layer-setting">
          <label class="question-label" for="target_key">Doelsleutel</label>
          <vee-field
            id="target_key"
            v-model.trim="linkedData.target_key"
            name="target_key"
            type="text"
            rules="required"
          />
          <vee-error-message class="form-error" name="target_key" />
        </div>
      </div>
      <div class="layer-settings">
        <div class="layer-setting">
          <label class="question-label" for="headers">Tabel kopjes</label>
          <textarea
            id="headers"
            name="headers"
            rows="6"
            :value="headers"
            @change="(e) => updateMultiLineField(linkedData, 'headers', e.target.value)"
          />
        </div>
        <div class="layer-setting">
          <label class="question-label" for="display_properties">Toon deze velden</label>
          <textarea
            id="display_properties"
            name="display_properties"
            rows="6"
            :value="display_properties"
            @change="(e) => updateMultiLineField(linkedData, 'display_properties', e.target.value)"
          />
        </div>
      </div>
    </div>
    <div class="config-btn-wrapper">
      <button class="button __secondary_admin" type="button" @click="cancel()">Annuleer</button>
      <button class="button __primary_admin" type="submit">
        {{ linkedData.edit ? "Pas toe" : "Voeg toe" }}
      </button>
    </div>
  </vee-form>
</template>

<script>
import { updateMultiLineField } from "@/utils/admin-form-helpers";
import { Form as VeeForm, Field as VeeField, ErrorMessage as VeeErrorMessage } from "vee-validate";

export default {
  name: "LinkedDataForm",
  components: { VeeForm, VeeField, VeeErrorMessage },
  props: {
    initialLinkedData: Object,
  },
  data() {
    return {
      linkedData: null,
    };
  },
  computed: {
    headers() {
      return this.linkedData.headers.join("\n");
    },
    display_properties() {
      return this.linkedData.display_properties.join("\n");
    },
  },
  created() {
    this.linkedData = {
      ...this.initialLinkedData,
    };
  },
  methods: {
    updateMultiLineField,
    submitForm(data) {
      const finalData = { ...this.linkedData, ...data };

      this.$emit("save", finalData);
    },
    cancel() {
      this.$emit("close");
    },
  },
};
</script>

<style scoped>
.linked-data-form {
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

.question-label {
  font-weight: var(--font-weight-bold);
}
</style>
