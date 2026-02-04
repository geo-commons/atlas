<template>
  <div class="portal-search-field" :class="sizeCssFormat">
    <input
      :value="searchQuery"
      class="search-field"
      type="search"
      :placeholder="placeholder"
      @keyup="(e) => setSearchQuery(e)"
      @keydown.enter="onSearch"
    />
    <button
      v-tippy="{ placement: 'bottom' }"
      class="flex __center"
      :aria-label="placeholder"
      content="Zoek"
      @click="onSearch"
    >
      <SearchIcon class="icon __grey" :class="sizeCssFormat" />
    </button>
  </div>
</template>

<script>
import SearchIcon from "@/assets/icons/search-icon.svg";

export default {
  name: "PortalSearchField",
  components: { SearchIcon },
  props: {
    initialSearchQuery: { default: "", type: String },
    size: {
      default: "medium",
      type: String,
    },
    placeholder: {
      default: "Zoek naar metadatasets...",
      type: String,
    },
  },
  emits: ["on-search"],
  data() {
    return {
      searchQuery: "",
    };
  },
  computed: {
    sizeCssFormat() {
      return `__${this.size}`;
    },
  },
  created() {
    this.searchQuery = this.initialSearchQuery;
  },
  methods: {
    setSearchQuery(e) {
      e.preventDefault();
      this.searchQuery = e.target.value;
    },
    onSearch() {
      if (!this.searchQuery) {
        this.$emit("on-search", "");
        return;
      }

      this.$emit("on-search", this.searchQuery);
    },
  },
};
</script>

<style scoped>
.portal-search-field {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

.portal-search-field.__medium {
  height: 40px;
  font-size: var(--font-size-normal);
  border: 1px solid var(--color-grey-50);
  padding: 0 8px;
}

.portal-search-field.__large {
  height: 60px;
  font-size: var(--font-size-xl);
  border-bottom: 3px solid var(--color-primary-organization);
}

.search-field {
  display: flex;
  flex: 1;
}
</style>
