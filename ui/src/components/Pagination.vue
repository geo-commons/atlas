<template>
  <div>
    <div class="content">
      <slot></slot>
    </div>

    <div class="" style="padding-top: 10px">
      <ul class="pagination">
        <!--      <li>-->
        <!--        <button class="iconbutton pagination-btn" @click="firstPage">-->
        <!--          <DoubleChevronLeftIcon />-->
        <!--        </button>-->
        <!--      </li>-->
        <li>
          <button
            :disabled="pageNumber === 0"
            class="iconbutton pagination-btn"
            @click="prevPage"
          >
            <ChevronLeftIcon />
          </button>
        </li>
        <li>
          <button class="iconbutton pagination-btn" @click="firstPage">
            1
          </button>
        </li>
        <li>
          <button class="iconbutton pagination-btn" @click="lastPage">
            {{ pageNumber + 1 }}
          </button>
        </li>
        <li>
          <button class="iconbutton pagination-btn" @click="lastPage">
            {{ pageCount }}
          </button>
        </li>
        <li>
          <button
            :disabled="pageNumber >= pageCount - 1"
            class="iconbutton pagination-btn"
            @click="nextPage"
          >
            <ChevronRightIcon />
          </button>
        </li>
        <!--      <li>-->
        <!--        <button-->
        <!--          :disabled="pageNumber >= pageCount - 1"-->
        <!--          class="iconbutton pagination-btn"-->
        <!--          @click="lastPage"-->
        <!--        >-->
        <!--          <DoubleChevronRightIcon />-->
        <!--        </button>-->
        <!--      </li>-->
      </ul>
    </div>
  </div>
</template>

<script>
import ChevronLeftIcon from "@/icons/ChevronLeftIcon.vue";
import ChevronRightIcon from "@/icons/ChevronRightIcon.vue";
// import DoubleChevronRightIcon from "@/icons/DoubleChevronRightIcon.vue";
// import DoubleChevronLeftIcon from "@/icons/DoubleChevronLeftIcon.vue";

export default {
  name: "PaginationComponent",
  components: {
    ChevronLeftIcon,
    // DoubleChevronLeftIcon,
    // DoubleChevronRightIcon,
    ChevronRightIcon,
  },
  props: {
    items: Array,
    nrOfRecords: { default: 10, type: Number },
  },
  data() {
    return {
      pageNumber: 0,
    };
  },
  computed: {
    pageCount() {
      let nrOfPages = this.items.length;
      return Math.ceil(nrOfPages / this.nrOfRecords);
    },
    paginatedData() {
      const start = this.pageNumber * this.nrOfRecords;
      const end = start + this.nrOfRecords;
      return this.items.slice(start, end);
    },
  },
  mounted() {},
  methods: {
    nextPage() {
      this.pageNumber++;
      this.$emit("page-change", this.pageNumber);
    },
    prevPage() {
      this.pageNumber--;
      this.$emit("page-change", this.pageNumber);
    },
    firstPage() {
      this.pageNumber = 0;
      this.$emit("page-change", this.pageNumber);
    },
    lastPage() {
      this.pageNumber = this.pageCount - 1;
      this.$emit("page-change", this.pageNumber);
    },
  },
};
</script>

<style scoped>
.pagination-btn {
  //border: solid 1px var(--color-grey-60);
  background: var(--color-grey-20);
  border-radius: var(--radius-small);
  width: 30px;
  height: 30px;
}

ul.pagination > li {
  float: left;
}

ul.pagination > li:not(:last-child) {
  margin-right: 6px;
}
</style>
