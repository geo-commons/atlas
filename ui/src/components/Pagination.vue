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
        <li v-if="hasElipses && currentPageNumber >= 5">...</li>
        <li v-for="page in visiblePageLabels" :key="page.label" :class="`${currentPageNumber === page.label ? 'active-page' : ''}`">
          <span v-if="page.disabled">...</span>
          <button v-else class="iconbutton pagination-btn" @click="gotoPage(page.label)">
            {{ page.label }}
          </button>
        </li>
        <li v-if="hasElipses && currentPageNumber <= pageCount - 4">...</li>
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
    visiblePageLabels() {
      // comment
      if (this.pageCount <= this.displayRange) {
        return this.pages.slice(1, this.pageCount - 1);
      }

      // Return the first page numbers when the current page number is smaller than the display range.
      if (this.currentPageNumber < this.displayRange) {
        return this.pages.slice(1, 5);
        // console.log("minder dan 5", this.pages);
        // output = this.pages.slice(1, 5);
        // return output;
      }

      // Return the last page numbers when being in range of the final page number.
      if (this.currentPageNumber > this.pageCount - 4) {
        output = this.pages.slice(this.pageCount - 5, this.pageCount - 1);
        return output;
      }

      let valPrev = this.currentPageNumber - 1; // for easier navigation - gives one previous page
      let valNext = this.currentPageNumber + 1; // one next page

      let output = [];

      output = this.pages.slice(valPrev, valNext);
      console.log(output);
      // return output;
      return this.pages.slice(valPrev - 1, valNext);
    },
    hasElipses() {
      return this.pageCount > this.displayRange + 1;
    },
  },
  mounted() {
    for (let i = 1; i <= this.pageCount; i += 1) {
      this.pages.push({
        label: i,
      });
    }

    console.log(this.pages);
  },
  methods: {
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
  //padding-top: 10px;
  padding: 10px 0;
}

ul.pagination > li {
  float: left;
}

ul.pagination > li:not(:last-child) {
  margin-right: 6px;
}
</style>
