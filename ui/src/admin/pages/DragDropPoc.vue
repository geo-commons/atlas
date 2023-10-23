<template>
  <div class="container __admin">
    <div class="top-menu-container">
      <div class="page-title-wrapper">
        <h1>POC: drag and drop</h1>
      </div>
    </div>
    <table>
      <thead>
        <tr>
          <td>ordening</td>
          <td>name</td>
          <td>id</td>
        </tr>
      </thead>
      <draggable
        v-model="categories"
        class="list-group"
        tag="tbody"
        item-key="order"
        v-bind="dragOptions"
        :move="onMove"
        @change="onChange"
        @start="isDragging = true"
        @end="isDragging = false"
      >
        <tr v-for="cat in categories" :key="cat.order">
          <td>{{ cat.order }}</td>
          <td>{{ cat.title }}</td>
          <td>{{ cat.id }}</td>
        </tr>
      </draggable>
    </table>
  </div>
</template>

<script>
// import Cookies from "js-cookie";
import draggable from "vuedraggable";

export default {
  name: "CategoryList",
  components: {
    draggable,
  },
  data() {
    return {
      categories: [],
      isDragging: false,
      editable: true,
      delayedDragging: false,
    };
  },
  computed: {
    dragOptions() {
      return {
        animation: 0,
        group: "description",
        disabled: !this.editable,
        ghostClass: "ghost",
      };
    },
  },
  watch: {
    isDragging(newValue) {
      if (newValue) {
        this.delayedDragging = true;
        return;
      }
      this.$nextTick(() => {
        this.delayedDragging = false;
      });
    },
  },
  created() {
    this.getCategories();
  },
  methods: {
    async getCategories() {
      const result = await fetch("/atlas/api/v1/categories/", {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch categories");
      }

      const response = await result.json();
      console.log(response);
      this.categories = response.map((c, index) => {
        return { title: c.title, order: index + 1, id: c.id };
      });
    },
    onMove({ relatedContext, draggedContext }) {
      // console.log({ relatedContext, draggedContext });
      const relatedElement = relatedContext.element;
      const draggedElement = draggedContext.element;
      console.log("successful drag: ", (!relatedElement || !relatedElement.fixed) && !draggedElement.fixed);
      return (!relatedElement || !relatedElement.fixed) && !draggedElement.fixed;
    },
    onChange() {
      this.reorder();
    },
    reorder() {
      this.categories = this.categories.map((category, index) => {
        return { title: category.title, id: category.id, order: index + 1 };
      });
    },
  },
};
</script>

<style scoped>
.flip-list-move {
  transition: transform 0.5s;
}

.no-move {
  transition: transform 0s;
}

.ghost {
  opacity: 0.5;
  background: #c8ebfb;
}

.list-group {
  min-height: 20px;
}

.list-group-item {
  cursor: move;
}

.list-group-item i {
  cursor: pointer;
}

.top-menu-container {
  padding: 20px 0;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.page-title-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
}

.search-wrapper {
  width: clamp(300px, 35%, 400px);
  height: 48px;
  position: relative;
  border: 1px solid var(--color-grey-60);
  border-radius: var(--radius-normal);
  background: var(--color-white);
}

.search-wrapper svg {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 16px;
  margin: auto 0;
  pointer-events: none;
}

.search-wrapper input {
  width: 100%;
  height: 48px;
  padding: 0 0 0 48px;
}

@media (max-width: 576px) {
  .page-title-wrapper {
    flex-direction: column;
    align-items: flex-start;
  }

  .search-wrapper {
    width: 100%;
  }

  .top-menu-container {
    gap: 16px;
  }
}

.category-title-link {
  text-decoration: none;
  color: var(--color-black);
}

.category-title-link:hover {
  text-decoration: underline;
}

.category-link-btn {
  color: var(--color-black);
  display: flex;
}

.form-model-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.category-table {
  width: 100%;
  border-collapse: collapse;
  background: var(--color-white);
}

tbody > tr:hover {
  background-color: var(--color-grey-40);
}

.category-table thead tr th {
  text-align: left;
  font-weight: var(--font-weight-normal);
  color: var(--color-text-grey);
  padding-top: 10px;
  padding-bottom: 10px;
}

tr.table-border:not(:last-child) > td,
th {
  border-bottom: 1px solid var(--color-grey-60);
}

tr > td:not(:nth-last-child(-n + 2)) {
  padding-right: 8px;
}

.first-column-padding {
  padding-left: 12px;
}
</style>
