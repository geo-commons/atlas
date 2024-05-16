<template>
  <vee-form v-slot="{ values }" ref="formRef" :initial-values="currentValues" @submit="save">
    <div :class="{ 'create-view-container': createView || compactLayout }">
      <p v-if="unexpectedError" class="warning-text">{{ unexpectedError }}</p>
      <div v-for="section in sections" :key="section.label">
        <hr v-if="!createView && !compactLayout" />
        <div :class="{ 'config-section-wrapper': !createView && !compactLayout }">
          <div v-if="!createView && !compactLayout" class="section-label">
            <h3 class="">{{ section.label }}</h3>
          </div>

          <div class="section-questions">
            <div v-for="question in section.questions" :key="question.id">
              <!-- note: currently we can only add one custom field per AdminFormSection component.
                            If this is no longer sufficient in the future take a look at how ol-view and ol-layer
                            are decomposed in the OpenLayers.vue component -->
              <slot v-if="question.type === 'custom'" name="custom"></slot>
              <div v-else-if="question.type === 'checkbox'" class="checkbox-wrapper">
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
                    <option v-for="option in options[question.id]" :key="option.id" :value="option.id">
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
                  :rules="getRules(question)"
                  :disabled="question.disabled"
                />
                <vee-field
                  v-else-if="question.type === 'decimal'"
                  :id="question.id"
                  v-model="currentValues[question.id]"
                  :name="question.id"
                  type="number"
                  :rules="getRules(question)"
                  :disabled="question.disabled"
                  :step="question.step"
                />
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
                <vee-field v-else-if="question.type === 'layer-select'" v-slot="{ field }" :name="question.id">
                  <layer-field
                    v-model="currentValues[question.id]"
                    :field="field"
                    :current-source-id="values[question.sourceField]"
                    :sources="options[question.sourceField] || []"
                  />
                </vee-field>
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
      <button class="button" :class="createView ? '__secondary_admin' : '__tertiary'" type="button" @click="cancel()">
        Annuleer
      </button>
      <button class="button" :class="createView ? '__secondary_admin' : '__primary_admin'" type="submit">
        Opslaan
      </button>
      <button v-if="createView" class="button __primary_admin" type="submit" @click="continueEditing = true">
        Opslaan en openen
      </button>
    </div>
  </vee-form>
</template>

<script>
import { ErrorMessage as VeeErrorMessage, Field as VeeField, Form as VeeForm } from "vee-validate";
import { formatDateValue } from "@/utils/date-formatter";
import AdminFormInfoText from "@/admin/components/AdminFormInfoText.vue";
import CloseIcon from "@/assets/icons/close-icon.svg";
import Cookies from "js-cookie";
import LayerField from "@/admin/components/LayerField.vue";

export default {
  name: "AdminFormSections",
  components: {
    LayerField,
    CloseIcon,
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
    compactLayout: {
      default: false,
      type: Boolean,
    },
    objectSpecificSave: Function,
    formObject: String,
  },
  data() {
    return {
      currentValues: this.initialValues,
      options: {},
      unexpectedError: null,
      continueEditing: false,
    };
  },
  watch: {
    initialValues(newValues) {
      this.currentValues = newValues;
    },
  },
  created() {
    this.retrieveOptions();
  },
  methods: {
    formatDateValue,
    retrieveOptions() {
      Object.values(this.sections).forEach((section) => {
        section.questions.forEach(async (question) => {
          if (question.type !== "dropdown") {
            return;
          }

          if (question.options instanceof Array) {
            this.$set(this.options, question.id, question.options);
            return;
          }

          if (question.options instanceof Function) {
            this.$set(this.options, question.id, await question.options());
            return;
          }

          console.error(`Expected options of question id: ${question.id} to be of type Array or Function.`);
        });
      });
    },
    getRules(question) {
      let rules = [];

      if (question.required) {
        rules.push("required");
      }
      if (question.type === "email") {
        rules.push("email");
      }
      if (question.maxLength) {
        rules.push(`max:${question.maxLength}`);
      }

      return rules.join("|");
    },
    reset(question) {
      this.currentValues[question.id] = "";
      const dropdownElement = document.getElementById(question.id);
      dropdownElement.value = "";
    },
    cancel() {
      if (this.createView) {
        this.$emit("close");
      } else {
        this.$router.push(`/${this.formObject}`);
      }
    },
    save(values) {
      if (this.createView) {
        this.objectSpecificSave(values, this.continueEditing);
      } else {
        this.objectSpecificSave(values);
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
    scrollToElementById(elementRefId) {
      const errorRef = this.$refs.form.$children.find((child) => child.id === elementRefId);
      const errorElement = errorRef?.$el;

      if (errorElement) {
        this.$nextTick(() => {
          errorElement.scrollIntoView({ behavior: "smooth", block: "end", inline: "nearest" });
          errorElement.focus({ preventScroll: true });
        });
      }
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

label.question-label {
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
  gap: 20px;
  padding: 30px 0;
}

.width {
  min-width: 100%;
}
</style>
