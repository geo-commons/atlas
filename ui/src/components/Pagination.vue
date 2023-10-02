<template>
  <div>
    <div class="content">
      <slot></slot>
    </div>

    <div v-if="items && pages.length > 1" class="flex-center">
      <ul class="pagination">
        <li>
          <button v-show="currentPageNumber > 1" class="iconbutton pagination-btn bg-color" @click="prevPage">
            <ChevronLeftIcon />
          </button>
        </li>
        <li :class="`${currentPageNumber === 1 ? 'active-page' : ''}`">
          <button class="iconbutton pagination-btn" @click="firstPage">1</button>
        </li>
        <li v-if="hasEllipses && currentPageNumber >= displayRange">...</li>
        <li v-for="page in visiblePages" :key="page.label" :class="`${currentPageNumber === page.label ? 'active-page' : ''}`">
          <button class="iconbutton pagination-btn" @click="gotoPage(page.label)">
            {{ page.label }}
          </button>
        </li>
        <li v-if="hasEllipses && currentPageNumber <= pageCount - (displayRange - 1)">...</li>
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
    </div>
  </div>
</template>

<script>
import ChevronLeftIcon from "@/icons/ChevronLeftIcon.vue";
import ChevronRightIcon from "@/icons/ChevronRightIcon.vue";

export default {
  name: "PaginationComponent",
  components: {
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
    items: "getPageNrArray",
  },
  mounted() {
    this.getPageNrArray();
  },
  methods: {
    getPageNrArray() {
      this.pages = [];
      for (let i = 1; i <= this.pageCount; i += 1) {
        this.pages.push({
          label: i,
        });
      }
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
  },
};
</script>

<style scoped>
.pagination-btn {
  border-radius: var(--radius-small);
  width: 30px;
  height: 30px;
}

.bg-color {
  background: var(--color-grey-20);
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
</style>
