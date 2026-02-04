<template>
  <div>
    <button class="back-button" @click="back">
      <ArrowLeftIcon class="icon __smedium" /> <span class="back-button-text">Terug naar overzicht</span>
    </button>

    <h4>{{ capitalizeFirstLetter(feature.title) }}</h4>

    <table-list>
      <table>
        <tbody>
          <tr v-for="field in feature.detailViewFields" :key="field">
            <td>
              {{ formatRawString(field) }}
            </td>
            <td>
              <RichValue :data-key="field" :data-value="feature.properties[field]" />
            </td>
          </tr>
        </tbody>
      </table>
    </table-list>
  </div>
</template>

<script>
import RichValue from "@/components/RichValue.vue";
import TableList from "@/components/TableList.vue";
import ArrowLeftIcon from "@/assets/icons/arrow-left-icon.svg";
import { capitalizeFirstLetter, formatRawString } from "@/utils/string-helpers";

export default {
  name: "FeatureInfoDetails",
  components: { ArrowLeftIcon, TableList, RichValue },
  props: {
    feature: Object,
  },
  emits: ["back"],
  methods: {
    capitalizeFirstLetter,
    formatRawString,
    back() {
      this.$emit("back");
    },
  },
};
</script>

<style scoped>
h4 {
  margin: 30px 20px 8px 20px;
}

.back-button {
  display: flex;
  align-items: center;
  font-size: var(--font-size-small);
  gap: 4px;
  margin: 0 0 24px 6px;
}

.back-button-text:hover {
  text-decoration: underline;
}

.table-wrapper td:first-child {
  width: 40%;
  color: var(--color-text-grey);
}

.table-wrapper td:last-child {
  padding-left: 20px;
}

.table-wrapper th,
.table-wrapper td {
  padding: 3px;
  vertical-align: top;
}
</style>
