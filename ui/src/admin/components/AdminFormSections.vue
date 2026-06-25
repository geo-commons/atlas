<template>
  <div v-if="loading">laden...</div>
  <vee-form
    v-else
    v-slot="{ values }"
    ref="formRef"
    :initial-values="initialValues"
    @submit="onSubmit"
    @invalid-submit="invalidSubmit"
  >
    <div :class="{ 'create-view-container': createView || compactLayout }">
      <p v-if="unexpectedError" class="warning-text">{{ unexpectedError }}</p>
      <div v-for="section in sections" :key="section.label">
        <hr v-if="!createView && !compactLayout && section?.showIf !== undefined ? section.showIf : true" />
        <div
          v-if="section?.showIf !== undefined ? section.showIf : true"
          :class="{ 'config-section-wrapper': !createView && !compactLayout }"
        >
          <div v-if="!createView && !compactLayout" class="section-label">
            <h3>{{ section.label }}</h3>
          </div>

          <div v-if="section.label === 'Gerelateerde data'" class="section-questions">
            <slot name="relatedData"></slot>
          </div>

          <div v-if="section.label === '(Oud) Gekoppelde data'" class="section-questions">
            <slot name="linkedData"></slot>
          </div>

          <div v-if="section.label === '(Oud) Templates'" class="section-questions" style="z-index: 1">
            <slot name="templates"></slot>
          </div>

          <div v-if="!section.disableInputs" class="section-questions">
            <div v-for="question in section.questions" :key="question.id">
              <!-- note: currently we can only add one custom field per AdminFormSection component.
                            If this is no longer sufficient in the future take a look at how ol-view and ol-layer
                            are decomposed in the OpenLayers.vue component -->
              <slot v-if="question.type === 'custom'" name="custom"></slot>
              <div v-else-if="question.type === 'checkbox'">
                <div v-if="question.showIf !== undefined ? question.showIf : true" class="tw-flex tw-flex-col tw-gap-1">
                  <div class="tw-flex tw-flex-row tw-gap-2">
                    <vee-field
                      :id="question.id"
                      v-slot="{ value, handleChange, handleBlur }"
                      :name="question.id"
                      :disabled="question.disabled"
                      :rules="getRules(question)"
                    >
                      <Checkbox
                        :model-value="value"
                        :disabled="question.disabled"
                        :input-id="question.id"
                        binary
                        @update:model-value="handleChange"
                        @blur="handleBlur"
                      />
                      <span class="label-info-text-wrapper">
                        <label :for="question.id">{{ question.label }}</label>
                        <VisibilityIndicator :visibility="question.visibility" />
                        <AdminFormInfoText
                          v-if="question.infoText && question.infoText !== ''"
                          :info-text="question.infoText"
                        />
                      </span>
                    </vee-field>
                    <span class="warning-text"><vee-error-message :name="question.id" /></span>
                  </div>
                  <template
                    v-for="hint in [question.getHintText ? question.getHintText(values) : '']"
                    :key="`${question.id}-${hint}`"
                  >
                    <Message v-if="hint" severity="secondary" class="tw-ml-7">{{ hint }}</Message>
                  </template>
                </div>
              </div>
              <div v-else-if="question.type === 'image'" class="image-wrapper">
                <div
                  v-if="imageFieldValues[question.id]?.imagePath || imageFieldValues[question.id]?.previewUrl"
                  class="preview-image-wrapper"
                >
                  <div
                    v-if="imageFieldValues[question.id]?.imagePath"
                    class="current-logo tw-flex tw-items-start tw-gap-2"
                  >
                    <div>
                      <div class="question-label">Huidige afbeelding</div>
                      <div class="tw-flex tw-gap-2">
                        <img
                          :src="`/atlas/media/${imageFieldValues[question.id]?.imagePath}`"
                          class="logo-preview"
                          :alt="`voorbeeld weergave van de huidige afbeelding voor ${question.id}`"
                        />
                        <Button
                          type="button"
                          icon="pi pi-trash"
                          severity="secondary"
                          outlined
                          rounded
                          aria-label="Verwijder afbeelding"
                          @click="clearImage(question.id)"
                        />
                      </div>
                    </div>
                  </div>
                  <div
                    v-if="imageFieldValues[question.id]?.previewUrl"
                    class="current-logo tw-flex tw-items-start tw-gap-2"
                  >
                    <div>
                      <div class="question-label">Geselecteerde afbeelding</div>
                      <div class="tw-flex tw-gap-2">
                        <img
                          :src="imageFieldValues[question.id]?.previewUrl"
                          class="logo-preview"
                          :alt="`voorbeeld weergave van geselecteerde afbeelding`"
                        />
                        <Button
                          type="button"
                          icon="pi pi-trash"
                          severity="secondary"
                          outlined
                          rounded
                          aria-label="Verwijder afbeelding"
                          @click="clearImage(question.id)"
                        />
                      </div>
                    </div>
                  </div>
                </div>
                <div class="upload-button">
                  <span class="label-info-text-wrapper">
                    <label :for="`file_${question.id}`" class="question-label">{{ question.label }}</label>
                    <VisibilityIndicator :visibility="question.visibility" />
                  </span>
                  <div class="tw-flex tw-flex-wrap tw-gap-2 tw-items-center">
                    <input
                      :id="`file_${question.id}`"
                      :ref="`fileInput_${question.id}`"
                      type="file"
                      :name="`file_${question.id}`"
                      class="inputfile"
                      accept="image/*"
                      @change="(e) => onFileUpload(e, question.id)"
                    />
                    <label :for="`file_${question.id}`" class="button __primary_admin __import">
                      <i class="pi pi-upload tw-mr-2" />
                      <span :ref="`fileLabelText_${question.id}`" :content="'selecteer afbeelding'">{{
                        imageFieldValues[question.id]?.uploadButtonText
                      }}</span>
                    </label>
                  </div>
                </div>
              </div>
              <div v-else-if="question.type === 'picklist'">
                <div v-if="question.showIf !== undefined ? question.showIf : true" class="picklist-wrapper">
                  <span class="label-info-text-wrapper">
                    <label class="question-label" :for="question.id">{{ question.label }}</label>
                    <VisibilityIndicator :visibility="question.visibility" />
                  </span>
                  <vee-field
                    :id="question.id"
                    v-slot="{ value, handleChange, handleBlur }"
                    :name="question.id"
                    :rules="getRules(question)"
                    class="__admin config-select-wrapper"
                    :disabled="question.disabled"
                  >
                    <PickList
                      :model-value="value"
                      data-key="id"
                      breakpoint="900px"
                      :disabled="question.disabled"
                      :show-source-controls="false"
                      :show-target-controls="false"
                      @blur="handleBlur"
                      @update:model-value="handleChange"
                    >
                      <template #option="{ option }">
                        {{ option.name }}
                      </template>
                      <template #sourceheader>
                        <span class="picklist-header">Beschikbare {{ question.objectDisplayName }}</span>
                      </template>
                      <template #targetheader>
                        <span class="picklist-header">Geselecteerde {{ question.objectDisplayName }}</span>
                      </template>
                    </PickList>
                  </vee-field>
                  <span class="warning-text"><vee-error-message :name="question.id" /></span>
                </div>
              </div>
              <div v-else>
                <span class="label-info-text-wrapper">
                  <label class="question-label" :for="question.id">{{ question.label }}</label>
                  <VisibilityIndicator :visibility="question.visibility" />
                  <AdminFormInfoText
                    v-if="question.infoText && question.infoText !== ''"
                    :info-text="question.infoText"
                    class="tw-ml-auto"
                  />
                </span>
                <div v-if="question.type === 'dropdown'" class="dropdown-wrapper">
                  <vee-field
                    :id="question.id"
                    v-slot="{ value, handleChange, handleBlur }"
                    :name="question.id"
                    :rules="getRules(question)"
                    :disabled="question.disabled"
                  >
                    <Select
                      :model-value="value"
                      :options="question.options"
                      option-label="label"
                      option-value="id"
                      :disabled="question.disabled"
                      :placeholder="`Selecteer een ${question.placeholder}`"
                      filter
                      :filter-placeholder="`Zoek een ${question.placeholder}`"
                      fluid
                      show-clear
                      @update:model-value="handleChange"
                      @blur="handleBlur"
                    />
                  </vee-field>
                </div>
                <vee-field
                  v-else-if="question.type === 'decimal'"
                  :id="question.id"
                  v-slot="{ value, handleChange, handleBlur }"
                  :name="question.id"
                  :rules="getRules(question)"
                  :disabled="question.disabled"
                  :step="question.step"
                >
                  <InputNumber
                    :model-value="value"
                    :input-id="question.id"
                    mode="decimal"
                    show-buttons
                    :step="question.step"
                    min="0"
                    fluid
                    @blur="handleBlur"
                    @update:model-value="handleChange"
                  />
                </vee-field>
                <label v-else-if="question.type === 'label'">
                  <p class="tw-mt-0 tw-mb-0 tw-font-normal">
                    {{ initialValues[question.id] ? initialValues[question.id] : "-" }}
                  </p>
                </label>
                <label v-else-if="question.type === 'display_date'">
                  <p class="tw-mt-0 tw-mb-0 tw-font-normal">
                    {{ formatDateValue(initialValues[question.id]) }}
                  </p>
                </label>
                <vee-field
                  v-else-if="question.type === 'text' && question.multiLine"
                  :id="question.id"
                  v-slot="{ value, handleChange, handleBlur }"
                  :name="question.id"
                  :rules="getRules(question)"
                  :disabled="question.disabled"
                >
                  <Textarea
                    :disabled="question.disabled"
                    :model-value="value"
                    :rows="question.rows ? question.rows : 5"
                    fluid
                    @update:model-value="handleChange"
                    @blur="handleBlur"
                  />
                </vee-field>
                <vee-field
                  v-else-if="question.type === 'json'"
                  v-slot="{ value, handleChange, handleBlur }"
                  :name="question.id"
                  :rules="getRules(question)"
                  :disabled="question.disabled"
                  class="width"
                >
                  <CodeMirror
                    :id="question.id"
                    :model-value="value"
                    basic
                    :lang="json()"
                    :linter="jsonParseLinter()"
                    :extensions="[clouds]"
                    gutter
                    :wrap="true"
                    class="!tw-text-sm"
                    @update:model-value="handleChange"
                    @blur="handleBlur"
                  />
                </vee-field>
                <vee-field
                  v-else-if="question.type === 'layer-select'"
                  v-slot="{ value, handleChange }"
                  :name="question.id"
                  :rules="getRules(question)"
                >
                  <InputText
                    :id="question.id"
                    :model-value="value"
                    class="!tw-mb-2"
                    placeholder="Laagnaam"
                    type="text"
                    fluid
                    @update:model-value="(updatedValue) => selectedLayerChanged(handleChange, updatedValue)"
                  />
                  <span>Of selecteer een laagnaam</span>
                  <layer-field
                    :model-value="value"
                    :current-source-id="values[question.sourceField]"
                    :sources="question.options || []"
                    @update:model-value="(updatedValue) => selectedLayerChanged(handleChange, updatedValue)"
                  />
                </vee-field>
                <vee-field
                  v-else-if="question.type === 'metadataset-select'"
                  v-slot="{ value, handleChange }"
                  :name="question.id"
                  :rules="getRules(question)"
                >
                  <MetadatasetsField
                    :model-value="value"
                    :options="question.options || []"
                    @update:model-value="handleChange"
                  />
                </vee-field>
                <vee-field
                  v-else-if="question.type === 'related-tables-select'"
                  v-slot="{ value, handleChange }"
                  :name="question.id"
                  :rules="getRules(question)"
                >
                  <RelatedTablesField
                    :related-tables="value"
                    :parent-id="initialValues.id"
                    :options="question.options || []"
                    @related-tables-changed="
                      (newValue) => {
                        handleChange(newValue);
                        $emit('related-tables-changed', newValue);
                      }
                    "
                  />
                </vee-field>
                <vee-field
                  v-else-if="question.type === 'date'"
                  :id="question.id"
                  v-slot="{ value, handleChange, handleBlur }"
                  :name="question.id"
                  :disabled="question.disabled"
                  :rules="getRules(question)"
                >
                  <DatePicker
                    fluid
                    date-format="yy-mm-dd"
                    :pt="{
                      panel: '!tw-min-w-8',
                    }"
                    :model-value="value ? new Date(value) : null"
                    @blur="handleBlur"
                    @update:model-value="handleChange"
                  />
                </vee-field>

                <vee-field
                  v-else-if="question.type === 'color'"
                  :id="question.id"
                  :name="question.id"
                  :disabled="question.disabled"
                  :rules="getRules(question)"
                  type="color"
                  as="input"
                />
                <vee-field
                  v-else-if="question.type === 'array'"
                  :id="question.id"
                  v-slot="{ value, handleChange, handleBlur }"
                  :name="question.id"
                  :disabled="question.disabled"
                  :rules="getRules(question)"
                >
                  <AutoComplete
                    :model-value="value"
                    :input-id="question.id"
                    :suggestions="question.suggestionsFrom ? autoCompleteSuggestions[question.id] || [] : []"
                    multiple
                    fluid
                    :typeahead="!!question.suggestionsFrom"
                    @complete="(e) => onAutoComplete(e, question, values)"
                    @update:model-value="handleChange"
                    @blur="handleBlur"
                    @keydown.enter.prevent
                  />
                </vee-field>
                <vee-field
                  v-else
                  :id="question.id"
                  v-slot="{ value, handleChange, handleBlur }"
                  :name="question.id"
                  :disabled="question.disabled"
                  :rules="getRules(question)"
                  type="text"
                >
                  <InputText
                    :id="question.id"
                    :model-value="value"
                    class="!tw-mb-2"
                    type="text"
                    fluid
                    :disabled="question.disabled"
                    @update:model-value="handleChange"
                    @blur="handleBlur"
                  />
                  <div v-if="question.withImagePreview" class="tw-flex tw-flex-col tw-gap-1 tw-items-start">
                    <span>Legenda voorbeeld:</span>
                    <img class="tw-max-w-full" :src="value" />
                  </div>
                </vee-field>
                <span class="warning-text">
                  <vee-error-message :name="question.id" />
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="config-btn-wrapper">
      <Button
        v-if="!disableCreateAndUpdate"
        text
        severity="secondary"
        class="!tw-text-sm !tw-font-semibold"
        type="button"
        @click="cancel()"
      >
        Annuleren
      </Button>
      <Button
        v-if="!disableCreateAndUpdate"
        outlined
        class="!tw-text-sm !tw-font-semibold !tw-bg-white hover:!tw-bg-transparent"
        type="submit"
        @click="setContinueEditing(true)"
      >
        Opslaan
      </Button>
      <Button
        v-if="!disableCreateAndUpdate && !createView"
        class="!tw-text-sm !tw-font-semibold"
        type="submit"
        @click="setContinueEditing(false)"
      >
        Opslaan en sluiten
      </Button>
      <Button v-if="createView" class="!tw-text-sm !tw-font-medium" type="submit" @click="continueEditing = true">
        Opslaan en openen
      </Button>
    </div>
  </vee-form>
</template>

<script>
import AdminFormInfoText from "@/admin/components/AdminFormInfoText.vue";
import LayerField from "@/admin/components/LayerField.vue";
import MetadatasetsField from "@/admin/components/MetadatasetsField.vue";
import VisibilityIndicator from "@/components/VisibilityIndicator.vue";
import { useGlobalStore } from "@/stores";
import { formatDateValue } from "@/utils/date-formatter";
import { json, jsonParseLinter } from "@codemirror/lang-json";
import Cookies from "js-cookie";
import { mapState } from "pinia";
import InputText from "primevue/inputtext";
import PickList from "primevue/picklist";
import { clouds } from "thememirror";
import { ErrorMessage as VeeErrorMessage, Field as VeeField, Form as VeeForm } from "vee-validate";
import CodeMirror from "vue-codemirror6";
import RelatedTablesField from "@/admin/components/RelatedTablesField.vue";

export default {
  name: "AdminFormSections",
  components: {
    RelatedTablesField,
    LayerField,
    MetadatasetsField,
    CodeMirror,
    AdminFormInfoText,
    VeeForm,
    VeeField,
    VeeErrorMessage,
    VisibilityIndicator,
    InputText,
    PickList,
  },
  props: {
    sections: Object,
    initialValues: Object,
    createView: {
      default: false,
      type: Boolean,
    },
    containsImageField: {
      default: false,
      type: Boolean,
    },
    compactLayout: {
      default: false,
      type: Boolean,
    },
    disableCreateAndUpdate: {
      default: false,
      type: Boolean,
    },
    objectSpecificSave: Function,
    formObject: String,
  },
  emits: ["update-source", "related-tables-changed", "close"],
  expose: ["sendSaveRequest", "resetForm"],
  data() {
    return {
      options: {},
      unexpectedError: null,
      continueEditing: false,
      imageFieldValues: {},
      loading: false,
      clouds: clouds,
      // autoCompleteSuggestions e.g.: { [questionId]: [] }
      autoCompleteSuggestions: {},
    };
  },
  computed: {
    ...mapState(useGlobalStore, ["config"]),
    getRules() {
      return (question) => {
        let rules = [];
        const values = this.$refs.formRef?.values || {};

        // Check if we should apply the contains-colon validation
        // Only apply if atlas_write_groups has items selected or authenticated_can_mutate is true
        const groups = values.atlas_write_groups;
        let atlasWriteGroupsHasItems = Array.isArray(groups) && groups[1].length > 0;
        const authenticatedCanMutate = document.getElementById("authenticated_can_mutate")
          ? document.getElementById("authenticated_can_mutate").checked
          : false;

        const shouldApplyColonValidation = atlasWriteGroupsHasItems || authenticatedCanMutate;

        // Check if any field has specified this field in its contains_colon property
        const hasColonValidation = !!question.contains_colon;

        if (hasColonValidation && shouldApplyColonValidation) {
          rules.push("contains-colon");
        }

        if (question.required) {
          rules.push("required");
        }
        if (question.type === "email") {
          rules.push("email");
        }
        if (question.maxLength) {
          rules.push(`max:${question.maxLength}`);
        }
        if (question.type === "json") {
          rules.push("json");
        }

        return rules.join("|");
      };
    },
  },
  created() {
    if (this.containsImageField) {
      this.setImageFieldValues();
    }
  },
  unmounted() {
    // Remove all created previewUrls
    Object.values(this.imageFieldValues).forEach((value) => {
      if (value?.previewUrl) {
        URL.revokeObjectURL(value.previewUrl);
      }
    });
  },
  methods: {
    formatDateValue,
    json,
    jsonParseLinter,
    reset(question) {
      if (this.$refs.formRef) {
        this.$refs.formRef.setFieldValue(question.id, "");
      }
    },
    cancel() {
      if (!this.formObject) {
        this.$router.push("/");
        return;
      }

      if (this.createView) {
        this.$emit("close");
      } else {
        this.$router.push(`/${this.formObject}`);
      }
    },
    setContinueEditing(val) {
      if (!this.createView) {
        this.continueEditing = val;
      }
    },
    onSubmit(values) {
      this.save(values);
    },
    save(values) {
      if (this.containsImageField) {
        // Manually add image fields to values object.
        Object.keys(this.imageFieldValues).forEach((key) => {
          if (this.imageFieldValues[key].clearRequested) {
            values[key] = "";
          } else if (this.imageFieldValues[key].file) {
            values[key] = this.imageFieldValues[key].file;
          }
        });
      }
      this.objectSpecificSave(values, this.continueEditing, this.sendSaveRequest);
    },
    async sendSaveRequest(apiUrl, method, currentValues) {
      try {
        const result = await fetch(apiUrl, {
          method: method,
          credentials: "same-origin",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": Cookies.get("csrftoken"),
          },
          body: JSON.stringify(currentValues),
        });

        if (!result.ok) {
          const errors = await result.json();
          this.$refs.formRef.setErrors(errors);

          // Scroll and focus first element that does not meet validation criteria.
          const firstErrorKey = Object.keys(errors)[0];
          this.scrollToElementById(firstErrorKey);
        }
        return result;
      } catch (error) {
        console.error("Unexpected error in sendSaveRequest:", error);
        window.scrollTo({ top: 0, behavior: "smooth" });
        this.unexpectedError = "Er is een onverwachte fout opgetreden, probeer het later nog eens.";
      }
    },
    invalidSubmit() {
      const errors = this.$refs.formRef.getErrors();
      const firstErrorKey = Object.keys(errors)[0];
      this.scrollToElementById(firstErrorKey);
    },
    scrollToElementById(elementRefId) {
      const errorElement = document.getElementById(elementRefId);

      if (errorElement) {
        this.$nextTick(() => {
          errorElement.scrollIntoView({ behavior: "smooth", block: "center", inline: "nearest" });
          errorElement.focus({ preventScroll: true });
        });
      }
    },
    setImageFieldValues() {
      Object.values(this.sections).forEach((section) => {
        section.questions.forEach((question) => {
          if (question.type === "image") {
            this.imageFieldValues[question.id] = {
              imagePath: this.initialValues[question.id],
              uploadButtonText: "Selecteer afbeelding",
              clearRequested: false,
            };
          }
        });
      });
    },
    clearImage(id) {
      if (!(id in this.imageFieldValues)) return;
      const field = this.imageFieldValues[id];
      if (field?.previewUrl) {
        URL.revokeObjectURL(field.previewUrl);
      }
      this.imageFieldValues[id] = {
        imagePath: null,
        uploadButtonText: "Selecteer afbeelding",
        previewUrl: null,
        file: null,
        clearRequested: true,
      };
      const fileInput = this.$refs[`fileInput_${id}`];
      if (fileInput) {
        const el = Array.isArray(fileInput) ? fileInput[0] : fileInput;
        if (el) el.value = "";
      }
    },
    onFileUpload(event, id) {
      event.preventDefault();
      const file = event.target.files[0];
      if (file) {
        this.imageFieldValues[id].uploadButtonText = file?.name;
        this.imageFieldValues[id].previewUrl = URL.createObjectURL(file);
        this.imageFieldValues[id].file = file;
        this.imageFieldValues[id].clearRequested = false;
      }
    },
    // Note: this method is being used in the AdminListFormDialog.
    resetForm() {
      this.$refs.formRef.resetForm();
    },
    selectedLayerChanged(handleChange, value) {
      // Handles layer selection changes.
      // If `value` is a string (from a normal input), it represents the layer name directly.
      // If `value` is an object (from <layer-field>), it has the form { name: "layer-name", legends: [] }.
      // If there are no legends, `legend_url` is reset to an empty string.
      const { formRef } = this.$refs;

      if (typeof value === "string") {
        formRef?.setFieldValue("legend_url", "");
        handleChange(value);
        return;
      }

      const { name, legends } = value;
      handleChange(name);

      formRef?.setFieldValue("legend_url", legends?.[0] || "");
    },
    onAutoComplete({ query }, question, values) {
      const fieldId = question.id;

      if (!this.autoCompleteSuggestions[fieldId]) {
        this.autoCompleteSuggestions[fieldId] = [];
      }

      const suggestions = values[question.suggestionsFrom];

      if (!Array.isArray(suggestions)) {
        this.autoCompleteSuggestions[fieldId] = [];
        return;
      }

      const q = (query || "").toLowerCase();

      this.autoCompleteSuggestions[fieldId] = suggestions.filter((item) => String(item).toLowerCase().includes(q));
    },
  },
};
</script>

<style scoped>
h3 {
  margin: 0;
}

.section-label {
  grid-area: section-label;
}

.question-label {
  font-weight: var(--font-weight-bold);
}

.create-view-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.section-questions {
  grid-area: section-questions;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.config-section-wrapper {
  display: grid;
  grid-template-areas: "section-label section-questions";
  grid-template-columns: 1fr 2fr;
  padding: 20px 0;
}

.config-section-wrapper .section-questions {
  min-width: 0;
  max-width: 100%;
  overflow: hidden;
}

.config-section-wrapper .section-questions > * {
  max-width: 100%;
  min-width: 0;
}

@media (max-width: 576px) {
  .config-section-wrapper {
    grid-template-areas:
      "section-label"
      "section-questions";
    grid-template-columns: 100%;
  }

  h3 {
    margin-bottom: 20px;
  }
}

.config-select-wrapper {
  height: 40px;
  width: 100%;
}

.label-info-text-wrapper {
  display: inline-flex;
  gap: 4px;
  align-items: center;
  flex-wrap: nowrap;
  flex-direction: row;
  width: 100%;
}

.label-info-text-wrapper label {
  display: inline-block;
  margin-right: 0;
  white-space: nowrap;
  flex-shrink: 0;
  width: auto;
}

.dropdown-wrapper {
  display: flex;
  gap: 4px;
  align-items: center;
}

.config-btn-wrapper {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1rem 0;
  position: sticky;
  bottom: 0;
  background-color: var(--color-backdrop);
  z-index: 2;
  border-top: 1px solid var(--color-grey-60);
}

.p-dialog .config-btn-wrapper {
  position: relative;
  background-color: transparent;
  border-top: 0;
  padding-bottom: 0;
}

.width {
  min-width: 100%;
}

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

.image-wrapper {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.logo-preview {
  height: auto;
  max-height: 40px;
}

.upload-button {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.current-logo {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 6px;
}

.preview-image-wrapper {
  display: flex;
  gap: 80px;
  align-items: center;
}

.picklist-header {
  font-weight: var(--font-weight-bold);
}

.picklist-wrapper {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
</style>
