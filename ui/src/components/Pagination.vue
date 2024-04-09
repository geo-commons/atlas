<template>
  <div>
    <div class="content">
      <Spinner v-if="loading" :style-type="styleType" />
      <slot v-else-if="items.length > 0"></slot>
    </div>

    <div v-if="items" class="pagination-wrapper">
      <div class="nr-pages-wrapper">
        <multiselect
          id="selected_columns"
          v-model="internalNrOfRecords"
          :class="styleType"
          :placeholder="'Kies aantal'"
          :options="nrRecordsOptions"
          :show-labels="false"
          :allow-empty="false"
          :searchable="false"
          @update:modelValue="(value) => updateNrOfRecords(value)"
        />
        <label>Aantal rijen per pagina</label>
      </div>

      <ul v-if="pages.length > 1" class="pagination">
        <li>
          <button
            v-show="currentPageNumber > 1"
            v-tippy="{ placement: 'bottom' }"
            class="iconbutton pagination-btn bg-color"
            type="button"
            aria-label="Vorige"
            content="Vorige"
            @click="prevPage"
          >
            <ChevronLeftIcon />
          </button>
        </li>
        <li :class="`${currentPageNumber === 1 ? 'active-page' : ''}`">
          <button class="iconbutton pagination-btn" type="button" aria-label="Naar eerste pagina" @click="firstPage">
            1
          </button>
        </li>
        <li v-if="hasEllipses && currentPageNumber >= displayRange" class="flex-center ellipses-wrapper">...</li>
        <li
          v-for="pageNr in visiblePages"
          :key="pageNr"
          :class="`${currentPageNumber === pageNr ? 'active-page' : ''}`"
        >
          <button
            class="iconbutton pagination-btn"
            type="button"
            :aria-label="`Naar pagina nummer ${pageNr}`"
            @click="gotoPage(pageNr)"
          >
            {{ pageNr }}
          </button>
        </li>
        <li
          v-if="hasEllipses && currentPageNumber <= pageCount - (displayRange - 1)"
          class="flex-center ellipses-wrapper"
        >
          ...
        </li>
        <li :class="`${currentPageNumber === pageCount ? 'active-page' : ''}`">
          <button class="iconbutton pagination-btn" type="button" aria-label="Naar laatste pagina" @click="lastPage">
            {{ pageCount }}
          </button>
        </li>
        <li>
          <button
            v-show="currentPageNumber < pageCount"
            v-tippy="{ placement: 'bottom' }"
            class="iconbutton pagination-btn bg-color"
            type="button"
            aria-label="Volgende"
            content="Volgende"
            @click="nextPage"
          >
            <ChevronRightIcon />
          </button>
        </li>
      </ul>

      <span>Totaal aantal resultaten: {{ items.length }}</span>
    </div>
  </div>
</template>

<script>
import ChevronLeftIcon from "../assets/icons/chevron-left-icon.svg";
import ChevronRightIcon from "../assets/icons/chevron-right-icon.svg";
import Multiselect from "vue-multiselect";
import Spinner from "@/components/Spinner.vue";

export default {
  name: "PaginationComponent",
  components: {
    Multiselect,
    ChevronLeftIcon,
    ChevronRightIcon,
    Spinner,
  },
  props: {
    items: Array,
    loading: Boolean,
    nrOfRecords: { default: 10, type: Number },
    displayRange: { default: 5, type: Number },
    styleType: {
      type: String,
      default: "",
    },
  },
  data() {
    return {
      currentPageNumber: 1,
      pages: [],
      // todo: think about making this more dynamic?
      nrRecordsOptions: [10, 15, 20, 30, 50, 100, 200, 500],
      internalNrOfRecords: this.nrOfRecords,
    };
  },
  computed: {
    pageCount() {
      let nrOfPages = this.items.length;
      return Math.ceil(nrOfPages / this.internalNrOfRecords);
    },
    visiblePages() {
      // When the  total number of pages is smaller than the range of pages that will be shown,
      // simply return the page number minus first and last page.
      if (this.pageCount <= this.displayRange) {
        return this.pages.slice(1, this.pageCount - 1);
      }

      // Return the first page numbers when the current page number is smaller than the display range.
      if (this.currentPageNumber < this.displayRange) {
        return this.pages.slice(1, this.displayRange);
      }

      // Return the last page numbers when being in range of the page count number.
      if (this.currentPageNumber > this.pageCount - (this.displayRange - 1)) {
        return this.pages.slice(this.pageCount - this.displayRange, this.pageCount - 1);
      }

      // Compute the range for the pages array to slice.
      // Due to how slice computes its indexes valPrev is -2.
      let valPrev = this.currentPageNumber - 2;
      let valNext = this.currentPageNumber + 1;
      return this.pages.slice(valPrev, valNext);
    },
    hasEllipses() {
      return this.pageCount > this.displayRange + 1;
    },
  },
  watch: {
    items: {
      handler() {
        this.resetPagination();
      },
      deep: true,
    },
  },
  mounted() {
    this.getPageNrArray();
  },
  methods: {
    getPageNrArray() {
      this.pages = [];
      for (let i = 1; i <= this.pageCount; i += 1) {
        this.pages.push(i);
      }
    },
    updateNrOfRecords(value) {
      this.resetPagination();
      this.$emit("records-change", value);
    },
    nextPage() {
      this.currentPageNumber++;
      this.$emit("page-change", this.currentPageNumber);
    },
    prevPage() {
      this.currentPageNumber--;
      this.$emit("page-change", this.currentPageNumber);
    },
    firstPage() {
      this.currentPageNumber = 1;
      this.$emit("page-change", this.currentPageNumber);
    },
    lastPage() {
      this.currentPageNumber = this.pageCount;
      this.$emit("page-change", this.currentPageNumber);
    },
    gotoPage(pageNr) {
      this.currentPageNumber = pageNr;
      this.$emit("page-change", this.currentPageNumber);
    },
    resetPagination() {
      this.getPageNrArray();
      this.firstPage();
    },
  },
};
</script>

<style scoped>
.content {
  overflow: auto;
}

.pagination-btn {
  border-radius: var(--radius-small);
  width: 30px;
  height: 30px;
}

.pagination-btn:hover {
  background-color: var(--color-primary-hover);
}

.bg-color {
  background: var(--color-grey-60);
}

.pagination-wrapper {
  display: flex;
  min-height: 80px;
  justify-content: space-between;
  align-items: center;
  padding-top: 5px;
  padding-bottom: var(--padding-screen);
}

.nr-pages-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
}

.nr-pages-wrapper > .multiselect {
  width: fit-content;
}

.active-page {
  border-radius: var(--radius-small);
  border: 1px solid var(--color-admin-primary);
}

.pagination {
  padding: 10px 0;
}

ul.pagination > li {
  float: left;
}

ul.pagination > li:not(:last-child) {
  margin-right: 6px;
}

.ellipses-wrapper {
  height: 30px;
}

@media (max-width: 576px) {
  .pagination-wrapper {
    flex-direction: column-reverse;
    align-items: flex-start;
    gap: 8px;
    padding-top: var(--padding-screen);
  }
}
</style>
