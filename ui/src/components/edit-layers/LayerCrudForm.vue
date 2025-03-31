<template>
  <vee-form
    ref="form"
    v-slot="{ errors }"
    class="tw-flex tw-flex-col tw-gap-2"
    :initial-values="initialValues"
    @submit="handleSubmit"
  >
    <div v-for="property in layerProperties" :key="property.name">
      <Message
        :class="{
          'tw-hidden': !errors[property.name],
        }"
        class="edit-layer-panel__error"
        severity="error"
        variant="simple"
        >{{ errors[property.name] }}
      </Message>
      <div class="tw-grid tw-grid-cols-1 md:tw-grid-cols-2 tw-items-center">
        <label
          :for="property.name"
          :class="{
            'edit-layer-panel__error': errors[property.name],
          }"
          >{{ property.name }}</label
        >
        <vee-field v-slot="{ field }" :name="property.name" type="text" :rules="property.nillable ? '' : 'required'">
          <InputText
            v-bind="field"
            :id="property.name"
            :placeholder="property.name"
            type="text"
            :invalid="Boolean(errors[property.name])"
          />
        </vee-field>
      </div>
    </div>
  </vee-form>
</template>

<script setup lang="ts">
import { Field as VeeField, Form as VeeForm } from "vee-validate";
import { ILayerProperties } from "@/types/layer";
import { ref } from "vue";

interface LayerCrudFormProps {
  initialValues?: { [key: string]: any };
  layerProperties: ILayerProperties;
  handleSubmit: (values: any) => void;
}

// Props
const { initialValues = {}, layerProperties, handleSubmit } = defineProps<LayerCrudFormProps>();

// Refs
const form = ref<InstanceType<typeof VeeForm> | null>(null);

// Expose
defineExpose({
  form,
});
</script>

<style scoped lang="scss">
.edit-layer-panel__error {
  color: var(--color-alert) !important;
}
</style>
