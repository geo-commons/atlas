<template>
  <div>
    <div class="linked-data-form">
      <div class="layer-settings">
        <div class="layer-setting">
          <label class="question-label" for="title">Titel</label>
          <input id="title" v-model.trim="linkedData.title" name="title" type="text" />
        </div>
        <div class="layer-setting">
          <label class="question-label" for="name">Laag naam</label>
          <input id="name" v-model.trim="linkedData.name" name="name" type="text" />
        </div>
        <div class="layer-setting">
          <label class="question-label" for="url">URL</label>
          <input id="url" v-model.trim="linkedData.url" name="url" type="text" />
        </div>
        <div class="layer-setting">
          <label class="question-label" for="source_key">Bronsleutel</label>
          <input id="source_key" v-model.trim="linkedData.source_key" name="source_key" type="text" />
        </div>
        <div class="layer-setting">
          <label class="question-label" for="target_key">Doelsleutel</label>
          <input id="target_key" v-model.trim="linkedData.target_key" name="target_key" type="text" />
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
      <button class="button __primary_admin" type="submit" @click="save">Opslaan</button>
    </div>
  </div>
</template>

<script>
import { updateMultiLineField } from "@/utils/admin-form-helpers";

export default {
  name: "LinkedDataForm",
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
    this.linkedData = { ...this.initialLinkedData };
  },
  methods: {
    updateMultiLineField,
    cancel() {
      this.$emit("close");
    },
    save() {
      this.$emit("save", this.linkedData);
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
</style>
