<template>
  <div :class="{ 'create-view-container': createView }">
    <div v-for="section in sections" :key="section.label">
      <hr v-if="!createView" />
      <div :class="{ 'config-section-wrapper': !createView }">
        <div v-if="!createView" class="section-label">
          <h3 class="">{{ section.label }}</h3>
        </div>

        <div class="section-questions">
          <div v-for="question in section.questions" :key="question.id">
            <!-- note: currently we can only add one custom field per AdminFormSection component.
                        If this is no longer sufficient in the future take a look at how ol-view and ol-layer
                        are decomposed in the OpenLayers.vue component -->
            <slot v-if="question.type === 'custom'" name="custom"></slot>
            <div v-else-if="question.type === 'dropdown'">
              <validation-provider v-slot="{ errors }" :name="question.name" class="flex __column">
                <label class="question-label" :for="question.id">{{ question.label }}</label>
                <select
                  :id="question.id"
                  v-model="currentValues[question.id]"
                  class="config-select-wrapper"
                  :required="question.required"
                  :disabled="question.disabled"
                >
                  <option disabled value="">Selecteer een {{ question.placeholder }}</option>
                  <option v-for="option in options[question.id]" :key="option.id" :value="option.id">
                    {{ option.label }}
                  </option>
                </select>
                <span>{{ errors[0] }}</span>
              </validation-provider>
            </div>
            <div v-else-if="question.type === 'checkbox'">
              <validation-provider v-slot="{ errors }" :name="question.name" class="flex __align-center">
                <input
                  :id="question.id"
                  v-model="currentValues[question.id]"
                  :checked="currentValues[question.id]"
                  :disabled="question.disabled"
                  type="checkbox"
                />
                <label :for="question.id">{{ question.label }}</label>
                <span>{{ errors[0] }}</span>
              </validation-provider>
            </div>
            <div v-else>
              <validation-provider v-slot="{ errors }" :name="question.name" class="flex __column">
                <label class="question-label" :for="question.id">{{ question.label }}</label>
                <textarea
                  v-if="question.type === 'text' && question.multiLine"
                  :id="question.id"
                  v-model="currentValues[question.id]"
                  :rows="question.rows ? question.rows : 5"
                  :disabled="question.disabled"
                  type="text"
                  class="width"
                />
                <input
                  v-else-if="question.type === 'text'"
                  :id="question.id"
                  v-model="currentValues[question.id]"
                  :disabled="question.disabled"
                  :name="question.id"
                  type="text"
                  :required="question.required"
                  :maxlength="question.maxLength"
                />
                <input
                  v-else-if="question.type === 'url'"
                  :id="question.id"
                  v-model="currentValues[question.id]"
                  type="url"
                  :disabled="question.disabled"
                  :required="question.required"
                />
                <input
                  v-else-if="question.type === 'email'"
                  :id="question.id"
                  v-model="currentValues[question.id]"
                  type="email"
                  :disabled="question.disabled"
                  :required="question.required"
                />
                <input
                  v-else-if="question.type === 'number'"
                  :id="question.id"
                  v-model="currentValues[question.id]"
                  type="number"
                  :disabled="question.disabled"
                  :min="question.minValue"
                  :max="question.maxValue"
                  :required="question.required"
                />
                <input
                  v-else-if="question.type === 'decimal'"
                  :id="question.id"
                  v-model="currentValues[question.id]"
                  type="number"
                  :disabled="question.disabled"
                  :min="question.minValue"
                  :max="question.maxValue"
                  :step="question.step"
                  :required="question.required"
                />
                <label v-else-if="question.type === 'label'">{{ currentValues[question.id] }}</label>
                <label v-else-if="question.type === 'display_date'">{{
                  formatDateValue(currentValues[question.id])
                }}</label>
                <span class="warning-text">{{ errors[0] }}</span>
              </validation-provider>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ValidationProvider } from "vee-validate";
import { formatDateValue } from "@/utils/date-formatter";

export default {
  name: "AdminFormSections",
  components: {
    ValidationProvider,
  },
  props: {
    sections: Object,
    initialValues: Object,
    createView: {
      default: false,
      type: Boolean,
    },
  },
  data() {
    return {
      currentValues: this.initialValues,
      options: {},
    };
  },
  computed: {},
  watch: {
    initialValues(newValues) {
      this.currentValues = newValues;
    },
    currentValues: {
      handler(newValues) {
        this.$emit("update", newValues);
      },
      deep: true,
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

.warning-text {
  color: var(--color-alert);
  font-weight: var(--font-weight-bold);
}
</style>
