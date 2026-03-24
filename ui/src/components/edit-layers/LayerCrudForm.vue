<template>
  <vee-form
    v-if="layer"
    ref="form"
    v-slot="{ errors }"
    class="tw-flex tw-flex-col tw-gap-2 tw-mt-4"
    :initial-values="initialValues"
    @submit="handleSubmit"
  >
    <div v-for="property in layerProperties" :key="property.name">
      <div class="tw-grid tw-grid-cols-1 md:tw-grid-cols-2 tw-gap-1 tw-items-center">
        <div class="tw-flex tw-flex-col tw-gap-1">
          <label
            :for="property.name"
            :class="{
              'edit-layer-panel__error': errors[property.name],
            }"
            class="tw-font-bold"
            >{{ getFriendlyFieldName(property.name) }}</label
          >
          <Message
            :class="{
              'tw-hidden': !errors[property.name],
            }"
            :pt="{
              text: '!tw-text-sm',
            }"
            class="edit-layer-panel__error"
            severity="error"
            variant="simple"
            >{{ errors[property.name] }}
          </Message>
        </div>
        <vee-field
          v-if="property.localType === 'boolean'"
          v-slot="{ value, handleChange, handleBlur }"
          :name="property.name"
        >
          <Checkbox
            :id="property.name"
            :model-value="value"
            :invalid="Boolean(errors[property.name])"
            binary
            @update:model-value="handleChange"
            @blur="handleBlur"
          />
        </vee-field>
        <vee-field
          v-else-if="property.localType === 'date'"
          v-slot="{ value, handleChange }"
          :name="property.name"
          :rules="property.nillable ? '' : 'required'"
        >
          <DatePicker
            :id="property.name"
            :model-value="toDateOrNull(value)"
            :invalid="Boolean(errors[property.name])"
            fluid
            date-format="dd-mm-yy"
            :placeholder="getFriendlyFieldName(property.name)"
            @update:model-value="handleChange(formatDateForInput($event as Date))"
          />
        </vee-field>
        <vee-field
          v-else-if="
            (property.localType === 'number' || property.localType === 'int') &&
            property.restriction?.enumeration?.length
          "
          v-slot="{ value, handleChange }"
          :name="property.name"
          :rules="property.nillable ? '' : 'required'"
        >
          <Select
            :id="property.name"
            :model-value="value"
            :options="property.restriction.enumeration"
            :invalid="Boolean(errors[property.name])"
            fluid
            :show-clear="property.nillable"
            :placeholder="getFriendlyFieldName(property.name)"
            @update:model-value="handleChange"
          />
        </vee-field>
        <vee-field
          v-else-if="property.localType === 'number' || property.localType === 'int'"
          v-slot="{ value, handleChange }"
          :name="property.name"
          :rules="property.nillable ? '' : 'required'"
        >
          <!-- max-fraction-digits should be 0 for integers (integers, shorts and longs in GeoServer) and 16 for numbers (float, doubles in GeoServer) -->
          <InputNumber
            :id="property.name"
            :model-value="value"
            :invalid="Boolean(errors[property.name])"
            fluid
            :min="property.restriction?.minInclusive"
            :max="property.restriction?.maxInclusive"
            :min-fraction-digits="0"
            :max-fraction-digits="property.localType === 'int' ? 0 : 16"
            :placeholder="getFriendlyFieldName(property.name)"
            @update:model-value="handleChange"
          />
        </vee-field>
        <vee-field
          v-else-if="property.localType === 'time'"
          v-slot="{ value, handleChange }"
          :name="property.name"
          :rules="property.nillable ? '' : 'required'"
        >
          <DatePicker
            :id="property.name"
            :model-value="toDateOrNull(value)"
            :invalid="Boolean(errors[property.name])"
            time-only
            fluid
            :placeholder="getFriendlyFieldName(property.name)"
            @update:model-value="handleChange(toGeoServerDateTime($event as Date))"
          />
        </vee-field>
        <vee-field
          v-else-if="property.localType === 'date-time'"
          v-slot="{ value, handleChange }"
          :name="property.name"
          :rules="property.nillable ? '' : 'required'"
        >
          <DatePicker
            :id="property.name"
            :model-value="toDateOrNull(value)"
            :invalid="Boolean(errors[property.name])"
            fluid
            date-format="dd-mm-yy"
            show-time
            :placeholder="getFriendlyFieldName(property.name)"
            @update:model-value="handleChange(toGeoServerDateTime($event as Date))"
          />
        </vee-field>
        <vee-field
          v-else-if="property.localType === 'string' && property.restriction?.enumeration?.length"
          v-slot="{ value, handleChange }"
          :name="property.name"
          :rules="property.nillable ? '' : 'required'"
        >
          <Select
            :id="property.name"
            :model-value="value"
            :options="property.restriction.enumeration"
            :invalid="Boolean(errors[property.name])"
            fluid
            :show-clear="property.nillable"
            :placeholder="getFriendlyFieldName(property.name)"
            @update:model-value="handleChange"
          />
        </vee-field>
        <vee-field
          v-else
          v-slot="{ field }"
          :name="property.name"
          type="text"
          :rules="property.nillable ? '' : 'required'"
        >
          <InputText
            v-bind="field"
            :id="property.name"
            :placeholder="getFriendlyFieldName(property.name)"
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
import { ILayer, ILayerProperties } from "@/types/layer";
import { ref } from "vue";
import { format, isValid, parseISO } from "date-fns";
import { formatDateForInput } from "@/utils/date-formatter";

interface LayerCrudFormProps {
  initialValues?: { [key: string]: any };
  layerProperties: ILayerProperties;
  handleSubmit: (values: any) => void;
  layer: ILayer | null;
}

// Props
const { initialValues = {}, layerProperties, handleSubmit, layer } = defineProps<LayerCrudFormProps>();

// Refs
const form = ref<InstanceType<typeof VeeForm> | null>(null);

// Form helpers
const toDateOrNull = (value?: string | Date | null) => {
  if (!value) return null;

  if (value instanceof Date) {
    return isValid(value) ? value : null;
  }

  const normalized = value.replace(/Z$/, "").replace(/\.\d+$/, "");

  const date = parseISO(normalized);

  return isValid(date) ? date : null;
};

const toGeoServerDateTime = (date?: Date | null) => {
  if (!date) return null;

  return format(date, "yyyy-MM-dd'T'HH:mm:ss");
};

const getFriendlyFieldName = (propertyName: string) => {
  if (!layer) return propertyName;

  return layer.friendly_fields[propertyName] ? layer.friendly_fields[propertyName] : propertyName;
};

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
