<template>
  <div>
    <div class="content">
      <slot></slot>
    </div>

    <div v-if="items && pages.length > 1" class="pagination-wrapper">
      <div class="nr-pages-wrapper">
        <multiselect
          id="selected_columns"
          v-model="internalNrOfRecords"
          :placeholder="'Kies aantal'"
          :options="nrRecordsOptions"
          :show-labels="false"
          :allow-empty="false"
          @input="(value) => updateNrOfRecords(value)"
        />
        <label>Aantal rijen per pagina</label>
      </div>

      <ul class="pagination">
        <li>
          <button v-show="currentPageNumber > 1" class="iconbutton pagination-btn bg-color" @click="prevPage">
            <ChevronLeftIcon />
          </button>
        </li>
        <li :class="`${currentPageNumber === 1 ? 'active-page' : ''}`">
          <button class="iconbutton pagination-btn" @click="firstPage">1</button>
        </li>
        <li v-if="hasEllipses && currentPageNumber >= displayRange" class="flex-center ellipses-wrapper">...</li>
        <li
          v-for="pageNr in visiblePages"
          :key="pageNr"
          :class="`${currentPageNumber === pageNr ? 'active-page' : ''}`"
        >
          <button class="iconbutton pagination-btn" @click="gotoPage(pageNr)">
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
          <button class="iconbutton pagination-btn" @click="lastPage">
            {{ pageCount }}
          </button>
        </li>
        <li>
          <button v-show="currentPageNumber < pageCount" class="iconbutton pagination-btn bg-color" @click="nextPage">
            <ChevronRightIcon />
          </button>
        </li>
      </ul>

      <span>Totaal aantal resultaten: {{ items.length }}</span>
    </div>
  </div>
</template>

<script>
import ChevronLeftIcon from "@/icons/ChevronLeftIcon.vue";
import ChevronRightIcon from "@/icons/ChevronRightIcon.vue";
import Multiselect from "vue-multiselect";

export default {
  name: "PaginationComponent",
  components: {
    Multiselect,
    ChevronLeftIcon,
    ChevronRightIcon,
  },
  props: {
    items: Array,
    nrOfRecords: { default: 10, type: Number },
    displayRange: { default: 5, type: Number },
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
      return Math.ceil(nrOfPages / this.nrOfRecords);
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
    items: "resetPagination",
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
      this.$emit("records-change", value);
      this.resetPagination();
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

.bg-color {
  background: var(--color-grey-60);
}

.pagination-wrapper {
  display: flex;
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
  border: 1px solid var(--color-primary);
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
