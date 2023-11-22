<template>
  <div class="feature-details-wrapper">
    <div class="feature-details-header">
      <h2>{{ layer.title }}</h2>
      <button
        v-tippy="{ placement: 'right' }"
        class="iconbutton __normal __outline"
        type="button"
        content="Sluit paneel"
        aria-label="Sluit paneel"
        @click="close"
      >
        <CloseIcon />
      </button>
    </div>

    <div class="feature-details-content">
      <table>
        <tbody>
          <tr v-for="property in filterProperties(feature.properties)" :key="property">
            <td>
              {{
                layer.friendly_fields && layer.friendly_fields[property]
                  ? layer.friendly_fields[property]
                  : property | capitalize
              }}
            </td>
            <td>
              <RichValue :data-key="property" :data-value="feature.properties[property]" />
            </td>
          </tr>
          <tr v-for="property in Object.keys(layer.templated_properties)" :key="property">
            <td>
              {{
                layer.friendly_fields && layer.friendly_fields[property]
                  ? layer.friendly_fields[property]
                  : property | capitalize
              }}
            </td>
            <td>
              <MarkdownTemplate
                :source="layer.templated_properties[property]"
                :data="getTemplatedPropertiesData(feature.properties)"
              />
            </td>
          </tr>
        </tbody>
      </table>

      <div v-for="(linkedData, key) in layer.linked_data" :key="key" class="linked-data">
        <div v-if="feature.properties[linkedData.source_key]">
          <FeatureTableExpandable
            :layer="linkedData"
            :overall-filter="{
              key: linkedData.target_key,
              value: feature.properties[linkedData.source_key],
            }"
          />
          <!--          :position="position"-->
          <!--          @set-position="setPosition"-->
        </div>
      </div>

      <!--      <div v-for="(template, key) in layer.templates" :key="key">-->
      <!--        <FeatureInfoTemplate :layer="layer" :template="template" :feature="feature" class="template" />-->
      <!--      </div>-->
    </div>
  </div>
</template>

<script>
import MarkdownTemplate from "@/components/MarkdownTemplate.vue";
import RichValue from "@/components/RichValue.vue";
import FeatureTableExpandable from "@/components/FeatureTableExpandable.vue";
import CloseIcon from "@/assets/icons/close-icon.svg";
// import FeatureInfoTemplate from "@/components/FeatureInfoTemplate.vue";

export default {
  name: "FeatureInfoDetails",
  components: { CloseIcon, FeatureTableExpandable, RichValue, MarkdownTemplate },
  filters: {
    capitalize: function (value) {
      if (!value) return "";
      // Replace underscores by spaces
      value = value.toString().replace(/_/g, " ");
      // Uppercase first character
      return value.charAt(0).toUpperCase() + value.slice(1);
    },
  },
  props: {
    feature: Object,
    layer: Object,
  },
  data() {
    return {};
  },
  computed: {},
  created() {},
  methods: {
    filterProperties(fetchedProperties) {
      if (this.layer.display_properties?.length > 0) {
        return this.layer.display_properties.filter((p) => Object.keys(fetchedProperties).includes(p));
      }

      return Object.keys(fetchedProperties);
    },
    getTemplatedPropertiesData(properties) {
      return {
        properties,
        position: this.position,
      };
    },
    close() {
      this.$emit("close");
    },
  },
};
</script>

<style scoped>
.feature-details-wrapper {
  position: relative;
  flex-shrink: 0;
  z-index: 2;
  margin: var(--padding-screen);
  padding: 10px 10px;
  height: 90%;
  width: 400px;
  background: var(--color-white);
  box-shadow: var(--shadow-normal);
  border-radius: var(--radius-normal);
}

.feature-details-header {
  display: flex;
  justify-content: space-between;
  gap: 16px;
}

/* todo: hoogte tabel goed zetten */
.feature-details-content {
  display: flex;
  flex-direction: column;
  gap: 10px;
  overflow: auto;
  height: inherit;
}
</style>
