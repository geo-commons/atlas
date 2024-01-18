<template>
  <validation-observer v-slot="{ handleSubmit, validateWithInfo }" ref="form">
    <form @submit.prevent="handleSubmit(save)">
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
                <div v-else-if="question.type === 'checkbox'">
                  <validation-provider
                    :vid="question.id"
                    mode="lazy"
                    :rules="getRules(question)"
                    v-slot="{ errors }"
                    :name="question.name"
                    class="flex __align-center"
                  >
                    <input
                      :id="question.id"
                      v-model="currentValues[question.id]"
                      :checked="currentValues[question.id]"
                      :disabled="question.disabled"
                      type="checkbox"
                    />
                    <span class="label-info-text-wrapper">
                      <label :for="question.id">{{ question.label }}</label>
                      <AdminFormInfoText
                        v-if="question.infoText && question.infoText !== ''"
                        :info-text="question.infoText"
                      />
                    </span>
                    <span class="warning-text">{{ errors[0] }}</span>
                  </validation-provider>
                </div>
                <div v-else>
                  <validation-provider
                    :vid="question.id"
                    :ref="question.id"
                    mode="lazy"
                    :rules="getRules(question)"
                    v-slot="{ errors }"
                    :name="question.name"
                    class="flex __column"
                  >
                    <span class="label-info-text-wrapper">
                      <label class="question-label" :for="question.id">{{ question.label }}</label>
                      <AdminFormInfoText
                        v-if="question.infoText && question.infoText !== ''"
                        :info-text="question.infoText"
                      />
                    </span>
                    <div v-if="question.type === 'dropdown'" class="dropdown-wrapper">
                      <select
                        :id="question.id"
                        v-model="currentValues[question.id]"
                        class="config-select-wrapper"
                        :disabled="question.disabled"
                      >
                        <option disabled value="-1">Selecteer een {{ question.placeholder }}</option>
                        <option v-for="option in options[question.id]" :key="option.id" :value="option.id">
                          {{ option.label }}
                        </option>
                      </select>
                      <button
                        v-if="currentValues[question.id]"
                        @click="reset(question)"
                        type="button"
                        class="iconbutton __small __round __transparent-bg"
                      >
                        <close-icon class="icon __small"></close-icon>
                      </button>
                    </div>
                    <input
                      v-else-if="question.type === 'url'"
                      :id="question.id"
                      v-model="currentValues[question.id]"
                      :disabled="question.disabled"
                      type="text"
                    />
                    <input
                      v-else-if="question.type === 'number'"
                      :id="question.id"
                      v-model="currentValues[question.id]"
                      type="number"
                      :disabled="question.disabled"
                    />
                    <input
                      v-else-if="question.type === 'decimal'"
                      :id="question.id"
                      v-model="currentValues[question.id]"
                      type="number"
                      :disabled="question.disabled"
                      :step="question.step"
                    />
                    <label v-else-if="question.type === 'label'">{{
                      currentValues[question.id] ? currentValues[question.id] : "-"
                    }}</label>
                    <label v-else-if="question.type === 'display_date'">{{
                      formatDateValue(currentValues[question.id])
                    }}</label>
                    <textarea
                      v-else-if="question.type === 'text' && question.multiLine"
                      :id="question.id"
                      v-model="currentValues[question.id]"
                      :rows="question.rows ? question.rows : 5"
                      :disabled="question.disabled"
                      class="width"
                    />
                    <input
                      v-else
                      :id="question.id"
                      v-model="currentValues[question.id]"
                      :disabled="question.disabled"
                      :name="question.id"
                      type="text"
                    />
                    <span class="warning-text">{{ errors[0] }}</span>
                  </validation-provider>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="config-btn-wrapper">
        <button class="button" :class="createView ? '__secondary' : '__tertiary'" type="button" @click="cancel()">
          Annuleer
        </button>
        <button
          class="button"
          :class="createView ? '__secondary' : '__primary'"
          type="submit"
          @click="validateFields(validateWithInfo)"
        >
          Opslaan
        </button>
        <button v-if="createView" class="button __primary" type="button" @click="save(true)">Opslaan en openen</button>
      </div>
    </form>
  </validation-observer>
</template>

<script>
import { ValidationObserver, ValidationProvider } from "vee-validate";
import { formatDateValue } from "@/utils/date-formatter";
import AdminFormInfoText from "@/admin/components/AdminFormInfoText.vue";
import CloseIcon from "@/assets/icons/close-icon.svg";
import Cookies from "js-cookie";

export default {
  name: "AdminFormSections",
  components: {
    CloseIcon,
    AdminFormInfoText,
    ValidationProvider,
    ValidationObserver,
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
    async validateFields(validateWithInfo) {
      // Check if any of the fields contain a validation error.
      const info = await validateWithInfo();

      if (!info.isValid) {
        // Get the id of the first corresponding element which has an error.
        let errorRefId = null;
        for (const [id, errors] of Object.entries(info.errors)) {
          if (errors.length > 0) {
            errorRefId = id;
            break;
          }
        }
        this.scrollToElementById(errorRefId);
      }
    },
    save(continueEditing = false) {
      if (this.createView) {
        this.objectSpecificSave(this.currentValues, continueEditing);
      } else {
        this.objectSpecificSave(this.currentValues);
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
          this.$refs.form.setErrors(errors);

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
</style>
