<template>
  <div v-if="loading">laden...</div>
  <vee-form
    v-else
    v-slot="{ values, setFieldValue }"
    ref="formRef"
    :initial-values="initialValues"
    @submit="onSubmit"
    @invalid-submit="invalidSubmit"
  >
    <div :class="{ 'create-view-container': createView || compactLayout }">
      <p v-if="unexpectedError" class="warning-text">{{ unexpectedError }}</p>
      <div v-for="section in sections" :key="section.label">
        <hr v-if="!createView && !compactLayout" />
        <div :class="{ 'config-section-wrapper': !createView && !compactLayout }">
          <div v-if="!createView && !compactLayout" class="section-label">
            <h3>{{ section.label }}</h3>
          </div>

          <div v-if="section.label === 'Gekoppelde data'" class="section-questions">
            <slot name="linkedData"></slot>
          </div>

          <div v-if="section.label === 'Templates'" class="section-questions" style="z-index: 1">
            <slot name="templates"></slot>
          </div>

          <div v-if="!section.disableInputs" class="section-questions">
            <div v-for="question in section.questions" :key="question.id">
              <!-- note: currently we can only add one custom field per AdminFormSection component.
                            If this is no longer sufficient in the future take a look at how ol-view and ol-layer
                            are decomposed in the OpenLayers.vue component -->
              <slot v-if="question.type === 'custom'" name="custom"></slot>
              <div v-else-if="question.type === 'checkbox'">
                <div v-if="question.showIf !== undefined ? question.showIf : true" class="checkbox-wrapper">
                  <vee-field
                    :id="question.id"
                    :name="question.id"
                    type="checkbox"
                    as="input"
                    :value="true"
                    :unchecked-value="false"
                    :disabled="question.disabled"
                    :rules="getRules(question)"
                  />
                  <span class="label-info-text-wrapper">
                    <label :for="question.id">{{ question.label }}</label>
                    <VisibilityIndicator :visibility="question.visibility" />
                    <AdminFormInfoText
                      v-if="question.infoText && question.infoText !== ''"
                      :info-text="question.infoText"
                    />
                  </span>
                  <span class="warning-text"><vee-error-message :name="question.id" /></span>
                </div>
              </div>
              <div v-else-if="question.type === 'image'" class="image-wrapper">
                <div
                  v-if="imageFieldValues[question.id]?.imagePath || imageFieldValues[question.id]?.previewUrl"
                  class="preview-image-wrapper"
                >
                  <div v-if="imageFieldValues[question.id]?.imagePath" class="current-logo">
                    <div class="question-label">Huidige afbeelding</div>
                    <img
                      :src="`/atlas/media/${imageFieldValues[question.id]?.imagePath}`"
                      class="logo-preview"
                      :alt="`voorbeeld weergave van de huidige afbeelding voor ${question.id}`"
                    />
                  </div>
                  <div v-if="imageFieldValues[question.id]?.previewUrl" class="current-logo">
                    <div class="question-label">Geselecteerde afbeelding</div>
                    <img
                      :src="imageFieldValues[question.id]?.previewUrl"
                      class="logo-preview"
                      :alt="`voorbeeld weergave van geselecteerde afbeelding`"
                    />
                  </div>
                </div>
                <div class="upload-button">
                  <span class="label-info-text-wrapper">
                    <label for="file" class="question-label">{{ question.label }}</label>
                    <VisibilityIndicator :visibility="question.visibility" />
                  </span>
                  <div>
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
                      <ArrowDownTrayIcon class="icon" />
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
                      @update:modelValue="handleChange"
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
                    :name="question.id"
                    :rules="getRules(question)"
                    as="select"
                    class="__admin config-select-wrapper"
                    :disabled="question.disabled"
                  >
                    <option disabled value="-1">Selecteer een {{ question.placeholder }}</option>
                    <option v-for="option in question.options" :key="option.id" :value="option.id">
                      {{ option.label }}
                    </option>
                  </vee-field>
                  <button
                    v-if="values[question.id]"
                    type="button"
                    class="iconbutton __small __round __transparent-bg"
                    @click="setFieldValue(question.id, '')"
                  >
                    <close-icon class="icon __small"></close-icon>
                  </button>
                </div>
                <vee-field
                  v-else-if="question.type === 'url'"
                  :id="question.id"
                  :name="question.id"
                  :disabled="question.disabled"
                  :rules="getRules(question)"
                  type="text"
                />
                <vee-field
                  v-else-if="question.type === 'number'"
                  :id="question.id"
                  :rules="getRules(question)"
                  :name="question.id"
                  type="number"
                  as="input"
                  :disabled="question.disabled"
                />
                <vee-field
                  v-else-if="question.type === 'decimal'"
                  :id="question.id"
                  :name="question.id"
                  :rules="getRules(question)"
                  type="number"
                  as="input"
                  :disabled="question.disabled"
                  :step="question.step"
                />
                <label v-else-if="question.type === 'label'">
                  {{ values[question.id] ? values[question.id] : "-" }}
                </label>
                <label v-else-if="question.type === 'display_date'">
                  {{ formatDateValue(values[question.id]) }}
                </label>
                <vee-field
                  v-else-if="question.type === 'text' && question.multiLine"
                  :id="question.id"
                  :name="question.id"
                  as="textarea"
                  :rules="getRules(question)"
                  :rows="question.rows ? question.rows : 5"
                  :disabled="question.disabled"
                  class="width"
                />
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
                    @update:model-value="handleChange"
                  />
                  <span>Of selecteer een laagnaam</span>
                  <layer-field
                    :model-value="value"
                    :current-source-id="values[question.sourceField]"
                    :sources="question.options || []"
                    @update:model-value="handleChange"
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
                    @metadataset-changed="
                      (newValue) => {
                        handleChange(newValue);
                        $emit('metadataset-changed', newValue);
                      }
                    "
                  />
                </vee-field>
                <vee-field
                  v-else-if="question.type === 'date'"
                  :id="question.id"
                  :name="question.id"
                  :disabled="question.disabled"
                  :rules="getRules(question)"
                  type="date"
                  as="input"
                />
                <vee-field
                  v-else-if="question.type === 'color'"
                  :id="question.id"
                  :name="question.id"
                  :disabled="question.disabled"
                  :rules="getRules(question)"
                  type="color"
                  as="input"
                />
                <div v-else-if="question.type === 'radio'" class="tw-flex tw-flex-col tw-gap-2">
                  <div
                    v-for="option in question.options"
                    :key="option.id"
                    class="tw-flex tw-items-start tw-gap-2 tw-cursor-pointer tw-py-1"
                  >
                    <vee-field
                      :id="option.id"
                      :name="question.id"
                      type="radio"
                      as="input"
                      :value="option.id"
                      :disabled="question.disabled"
                      :rules="getRules(question)"
                      class="tw-mt-[6px]"
                    />
                    <label :for="option.id" class="tw-flex-1 tw-leading-relaxed tw-font-normal tw-cursor-pointer">
                      {{ option.label }}
                    </label>
                  </div>
                  <span class="warning-text">
                    <vee-error-message :name="question.id" />
                  </span>
                </div>
                <vee-field
                  v-else
                  :id="question.id"
                  :name="question.id"
                  :disabled="question.disabled"
                  :rules="getRules(question)"
                  type="text"
                />
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
      <button
        v-if="!disableCreateAndUpdate"
        class="button"
        :class="createView ? '__secondary_admin' : '__tertiary'"
        type="button"
        @click="cancel()"
      >
        Annuleren
      </button>
      <button
        v-if="!disableCreateAndUpdate"
        class="button __secondary_admin"
        type="submit"
        @click="setContinueEditing(true)"
      >
        Opslaan
      </button>
      <button
        v-if="!disableCreateAndUpdate && !createView"
        class="button"
        :class="createView ? '__secondary_admin' : '__primary_admin'"
        type="submit"
        @click="setContinueEditing(false)"
      >
        Opslaan en sluiten
      </button>
      <button v-if="createView" class="button __primary_admin" type="submit" @click="continueEditing = true">
        Opslaan en openen
      </button>
    </div>
  </vee-form>
</template>

<script>
import AdminFormInfoText from "@/admin/components/AdminFormInfoText.vue";
import LayerField from "@/admin/components/LayerField.vue";
import MetadatasetsField from "@/admin/components/MetadatasetsField.vue";
import VisibilityIndicator from "@/admin/components/VisibilityIndicator.vue";
import ArrowDownTrayIcon from "@/assets/icons/arrow-down-tray-icon.svg";
import CloseIcon from "@/assets/icons/close-icon.svg";
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

export default {
  name: "AdminFormSections",
  components: {
    ArrowDownTrayIcon,
    LayerField,
    MetadatasetsField,
    CloseIcon,
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
  emits: ["update-source", "metadataset-changed"],
  expose: ["updateFieldValue", "sendSaveRequest"],
  data() {
    return {
      options: {},
      unexpectedError: null,
      continueEditing: false,
      imageFieldValues: {},
      loading: false,
      clouds: clouds,
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

        if (hasColonValidation && shouldApplyColonValidation && this.config?.features?.edit_layer_features) {
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
    updateFieldValue(fieldName, value) {
      // Update the vee-validate form value
      if (this.$refs.formRef) {
        this.$refs.formRef.setFieldValue(fieldName, value);
      }
    },
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
          if (this.imageFieldValues[key].file) {
            // Only add image to values if there is a file available,
            // otherwise we overwrite the current image with an undefined value.
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
            };
          }
        });
      });
    },
    onFileUpload(event, id) {
      event.preventDefault();
      const file = event.target.files[0];
      if (file) {
        this.imageFieldValues[id].uploadButtonText = file?.name;
        this.imageFieldValues[id].previewUrl = URL.createObjectURL(file);
        this.imageFieldValues[id].file = file;
      }
    },
    // Note: this method is being used in the AdminListFormDialog.
    resetForm() {
      this.$refs.formRef.resetForm();
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

.checkbox-wrapper {
  display: flex;
  flex-direction: row;
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
