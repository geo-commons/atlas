<template>
  <div>
    <!-- TODO: zoeken binnen andere objecttypen toevoegen -->
    <div class="tw-relative">
      <i
        class="pi pi-search tw-absolute tw-left-4 tw-top-1/2 -tw-translate-y-1/2 tw-text-lg tw-text-gray-400"
        aria-hidden="true"
      ></i>
      <input
        :value="searchQuery"
        type="search"
        :placeholder="placeholder"
        class="tw-w-full tw-pl-12 tw-pr-4 tw-py-3.5 !tw-border !tw-border-solid !tw-border-gray-300 tw-rounded-xl focus:tw-outline-none focus:tw-ring-2 focus:tw-ring-[var(--color-primary-organization)] focus:!tw-border-[var(--color-primary-organization)] tw-text-base tw-bg-white"
        @keyup="(e) => setSearchQuery(e)"
        @keydown.enter="onSearch"
      />
    </div>
    <button
      class="tw-mt-5 tw-px-8 tw-py-3 tw-rounded-xl tw-bg-[var(--color-primary-organization)] hover:tw-opacity-90 tw-text-white tw-font-medium tw-transition-colors"
      aria-label="Zoeken"
      @click="onSearch"
    >
      Zoeken
    </button>
  </div>
</template>

<script>
export default {
  name: "PortalSearchField",
  props: {
    initialSearchQuery: { default: "", type: String },
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
