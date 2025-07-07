<template>
  <div v-if="loading">laden...</div>
  <vee-form
    v-else
    v-slot="{ values }"
    ref="formRef"
    :initial-values="currentValues"
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
                    v-slot="{ field }"
                    :name="question.id"
                    type="checkbox"
                    :value="true"
                    :unchecked-value="false"
                    :rules="getRules(question)"
                  >
                    <input
                      v-bind="field"
                      :id="question.id"
                      type="checkbox"
                      :name="question.id"
                      :value="true"
                      :disabled="question.disabled"
                    />
                  </vee-field>
                  <span class="label-info-text-wrapper">
                    <label :for="question.id">{{ question.label }}</label>
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
                  <label for="file" class="question-label">{{ question.label }}</label>
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
                  <label class="question-label" :for="question.id">{{ question.label }}</label>
                  <vee-field
                    :id="question.id"
                    :name="question.id"
                    :rules="getRules(question)"
                    class="__admin config-select-wrapper"
                    :disabled="question.disabled"
                  >
                    <PickList
                      v-model="currentValues[question.id]"
                      data-key="id"
                      breakpoint="900px"
                      :disabled="question.disabled"
                      :show-source-controls="false"
                      :show-target-controls="false"
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
                  <AdminFormInfoText
                    v-if="question.infoText && question.infoText !== ''"
                    :info-text="question.infoText"
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
                    v-if="currentValues[question.id]"
                    type="button"
                    class="iconbutton __small __round __transparent-bg"
                    @click="reset(question)"
                  >
                    <close-icon class="icon __small"></close-icon>
                  </button>
                </div>
                <vee-field
                  v-else-if="question.type === 'url'"
                  :id="question.id"
                  v-model="currentValues[question.id]"
                  :name="question.id"
                  :disabled="question.disabled"
                  :rules="getRules(question)"
                  type="text"
                />
                <vee-field
                  v-else-if="question.type === 'number'"
                  :id="question.id"
                  v-model="currentValues[question.id]"
                  :name="question.id"
                  type="number"
                  :disabled="question.disabled"
                >
                  <input
                    :id="question.id"
                    :value="currentValues[question.id]"
                    :name="question.id"
                    type="number"
                    :disabled="question.disabled"
                    @change="(e) => handleInput(e, question)"
                  />
                </vee-field>
                <vee-field
                  v-else-if="question.type === 'decimal'"
                  :id="question.id"
                  :value="currentValues[question.id]"
                  :name="question.id"
                  :rules="getRules(question)"
                  type="number"
                  :disabled="question.disabled"
                  :step="question.step"
                >
                  <input
                    :id="question.id"
                    :value="currentValues[question.id]"
                    :name="question.id"
                    type="number"
                    :disabled="question.disabled"
                    :step="question.step"
                    @change="(e) => handleInput(e, question)"
                  />
                </vee-field>
                <label v-else-if="question.type === 'label'">{{
                  currentValues[question.id] ? currentValues[question.id] : "-"
                }}</label>
                <label v-else-if="question.type === 'display_date'">{{
                  formatDateValue(currentValues[question.id])
                }}</label>
                <vee-field
                  v-else-if="question.type === 'text' && question.multiLine"
                  :id="question.id"
                  v-model="currentValues[question.id]"
                  :name="question.id"
                  as="textarea"
                  :rules="getRules(question)"
                  :rows="question.rows ? question.rows : 5"
                  :disabled="question.disabled"
                  class="width"
                />
                <vee-field
                  v-else-if="question.type === 'json'"
                  v-model="currentValues[question.id]"
                  :name="question.id"
                  :rules="getRules(question)"
                  :disabled="question.disabled"
                  class="width"
                >
                  <CodeMirror
                    :id="question.id"
                    v-model="currentValues[question.id]"
                    :lang="json()"
                    :linter="jsonParseLinter()"
                    :extensions="[clouds]"
                    basic
                    gutter
                    :wrap="true"
                    class="!tw-text-sm"
                  ></CodeMirror>
                </vee-field>
                <vee-field
                  v-else-if="question.type === 'layer-select'"
                  v-slot="{ field }"
                  :name="question.id"
                  :rules="getRules(question)"
                >
                  <InputText :id="question.id" v-bind="field" class="!tw-mb-2" placeholder="Laagnaam" type="text" />
                  <span>Of selecteer een laagnaam</span>
                  <layer-field
                    :model-value="currentValues[question.id]"
                    :field="field"
                    :current-source-id="values[question.sourceField]"
                    :sources="question.options || []"
                    @update:modelValue="(value) => (currentValues[question.id] = value)"
                  />
                </vee-field>
                <vee-field v-else-if="question.type === 'theme-select'" v-slot="{ field }" :name="question.id">
                  <theme-field
                    :model-value="currentValues[question.id]"
                    :field="field"
                    @update:modelValue="(value) => (currentValues[question.id] = value)"
                  />
                </vee-field>
                <vee-field
                  v-else-if="question.type === 'date'"
                  :id="question.id"
                  :value="currentValues[question.id] ? currentValues[question.id] : ''"
                  :name="question.id"
                  :disabled="question.disabled"
                  :rules="getRules(question)"
                  type="date"
                  @input="(event) => (message = event.target.value)"
                />
                <vee-field
                  v-else-if="question.type === 'color'"
                  :id="question.id"
                  :name="question.id"
                  :value="currentValues[question.id]"
                  :disabled="question.disabled"
                  :rules="getRules(question)"
                  type="color"
                  @input="(event) => (currentValues[question.id] = event.target.value)"
                />
                <vee-field
                  v-else
                  :id="question.id"
                  v-model="currentValues[question.id]"
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
import ThemeField from "@/admin/components/ThemeField.vue";
import ArrowDownTrayIcon from "@/assets/icons/arrow-down-tray-icon.svg";
import CloseIcon from "@/assets/icons/close-icon.svg";
import { formatDateValue } from "@/utils/date-formatter";
import { json, jsonParseLinter } from "@codemirror/lang-json";
import Cookies from "js-cookie";
import { clouds } from "thememirror";
import { ErrorMessage as VeeErrorMessage, Field as VeeField, Form as VeeForm } from "vee-validate";
import CodeMirror from "vue-codemirror6";
import { mapState } from "pinia";
import { useGlobalStore } from "@/stores";

export default {
  name: "AdminFormSections",
  components: {
    ArrowDownTrayIcon,
    ThemeField,
    LayerField,
    CloseIcon,
    CodeMirror,
    AdminFormInfoText,
    VeeForm,
    VeeField,
    VeeErrorMessage,
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
  data() {
    return {
      currentValues: { ...this.initialValues },
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

        // Check if we should apply the contains-colon validation
        // Only apply if atlas_write_groups has items selected or authenticated_can_mutate is true
        let atlasWriteGroupsHasItems =
          Array.isArray(this.currentValues.atlas_write_groups) && this.currentValues.atlas_write_groups[1].length > 0;
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
  watch: {
    initialValues(newValues) {
      this.currentValues = newValues;

      if (this.containsImageField && this.currentValues) {
        this.setImageFieldValues();
      }
    },
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
      this.currentValues[question.id] = "";
      const dropdownElement = document.getElementById(question.id);
      dropdownElement.value = "";
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
      if (this.createView) {
        this.objectSpecificSave(values, this.continueEditing, this.sendSaveRequest);
      } else if (this.containsImageField) {
        // Manually add image fields to values object.
        Object.keys(this.imageFieldValues).forEach((key) => {
          values[key] = this.currentValues[key];
        });

        this.objectSpecificSave(values, this.continueEditing, this.sendSaveRequest);
      } else {
        this.objectSpecificSave(values, this.continueEditing, this.sendSaveRequest);
      }
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
    handleInput(event, question) {
      event.preventDefault();
      let value = event.target.value;
      if (value === "") {
        value = null;
      }
      this.currentValues[question.id] = value;
    },
    setImageFieldValues() {
      Object.values(this.sections).forEach((section) => {
        section.questions.forEach((question) => {
          if (question.type === "image") {
            this.imageFieldValues[question.id] = {
              imagePath: this.currentValues[question.id],
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
        this.currentValues[id] = file;
      }
    },
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
  display: flex;
  gap: 5px;
  align-items: center;
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
