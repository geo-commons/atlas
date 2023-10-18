<template>
  <div>
    <div v-for="section in sections" :key="section.label">
      <hr v-if="!createView" />
      <div :class="{ 'config-section-wrapper': !createView, 'full-width': createView }">
        <div v-if="!createView" class="section-label">
          <h3 class="">{{ section.label }}</h3>
        </div>

        <div class="section-questions">
          <div v-for="question in section.questions" :key="question.id">
            <div v-if="question.type === 'dropdown'">
              <validation-provider v-slot="{ errors }" :name="question.name" class="flex __column">
                <label :for="question.id">{{ question.label }}</label>
                <select
                  :id="question.id"
                  v-model="currentValues[question.id]"
                  class="config-select-wrapper"
                  :required="question.required"
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
                  type="checkbox"
                />
                <label :for="question.id">{{ question.label }}</label>
                <span>{{ errors[0] }}</span>
              </validation-provider>
            </div>

            <div v-else>
              <validation-provider v-slot="{ errors }" :name="question.name" class="flex __column">
                <label :for="question.id">{{ question.label }}</label>
                <textarea
                  v-if="question.type === 'text' && question.multiLine"
                  :id="question.id"
                  v-model="currentValues[question.id]"
                  :rows="question.rows ? question.rows : 5"
                  type="text"
                  class="width"
                />
                <input
                  v-else-if="question.type === 'text'"
                  :id="question.id"
                  v-model="currentValues[question.id]"
                  type="text"
                  :required="question.required"
                />
                <input
                  v-else-if="question.type === 'number'"
                  :id="question.id"
                  v-model="currentValues[question.id]"
                  type="number"
                  :min="question.min"
                  :max="question.max"
                  :required="question.required"
                />
                <input
                  v-else-if="question.type === 'decimal'"
                  :id="question.id"
                  v-model="currentValues[question.id]"
                  type="number"
                  :min="question.min"
                  :max="question.max"
                  :step="question.step"
                  :required="question.required"
                />
                <span>{{ errors[0] }}</span>
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

export default {
  name: "AdminFormSections",
  components: {
    ValidationProvider,
  },
  props: {
    formData: Object,
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
input {
  background: var(--color-white);
}

textarea {
  border: 1px solid var(--color-grey-60);
  border-radius: var(--radius-normal);

  resize: vertical;
}

textarea.width {
  width: 100%;
}

h3 {
  margin: 0;
}

select {
  padding: 0 16px;
  border: 1px solid var(--color-grey-60);
  border-radius: var(--radius-normal);
  //font-family: var(--font-family);
  font-family: "Roboto", sans-serif;
  font-size: var(--font-size-normal);
  font-weight: var(--font-weight-normal);
}

.full-width {
  width: 100%;
}

.section-label {
  grid-area: section-label;
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
}

.config-select-wrapper {
  height: 40px;
  width: 100%;
}
</style>
