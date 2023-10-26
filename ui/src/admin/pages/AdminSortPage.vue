<template>
  <div class="container __admin">
    <h1>Sortering</h1>

    <div class="sort-container">
      <div class="category-table-wrapper">
        <h3>Categorieën</h3>
        <table class="sort-table">
          <thead>
            <tr class="table-border">
              <th class="sort-column-padding">Titel</th>
            </tr>
          </thead>
          <draggable
            v-model="categories"
            tag="tbody"
            item-key="currentOrder"
            group="categories"
            v-bind="dragOptions"
            @change="onCategoryMove"
          >
            <tr
              v-for="category in categories"
              :key="category.currentOrder"
              class="table-border"
              :class="{ 'active-row': checkRow(category) }"
              @click="selectRow(category)"
            >
              <td class="sort-column-padding">{{ category.title }}</td>
            </tr>
          </draggable>
        </table>
      </div>

      <div v-if="selectedCategory" class="layer-table-wrapper">
        <h3>Kaartlagen</h3>
        <table v-if="selectedLayers?.length > 0" class="sort-table">
          <thead>
            <tr class="table-border">
              <th class="sort-column-padding">Titel</th>
            </tr>
          </thead>
          <draggable
            v-model="selectedLayers"
            tag="tbody"
            item-key="order"
            group="layers"
            v-bind="dragOptions"
            @change="onLayerMove"
          >
            <tr v-for="layer in selectedLayers" :key="layer.id" class="table-border">
              <td class="sort-column-padding">{{ layer.title }}</td>
            </tr>
          </draggable>
        </table>
        <div v-else>De geselecteerde categorie heeft geen bijbehorende kaartlagen.</div>
      </div>
    </div>
  </div>
</template>

<script>
import draggable from "vuedraggable";
import Cookies from "js-cookie";
import { debounce } from "@/utils/debouncer";

export default {
  name: "AdminSortPage",
  components: {
    draggable,
  },
  data() {
    return {
      categories: [],
      layers: [],
      layerData: {},
      selectedCategory: null,
      selectedLayers: [],
      timeout: null,
    };
  },
  computed: {
    dragOptions() {
      return {
        animation: 0,
        group: "description",
        disabled: false,
        ghostClass: "ghost",
      };
    },
  },
  watch: {
    selectedCategory() {
      if (!this.selectedCategory) {
        this.selectedLayers = [];
        return;
      }

      this.selectedLayers = this.layers.filter((l) => {
        return l.category?.id === this.selectedCategory.id;
      });
      this.reorderSelectedLayers();
    },
  },
  created() {
    this.getCategories();
    this.getLayers();
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
      this.categories = response.map((c, index) => {
        return { title: c.title, newOrder: index + 1, id: c.id, currentOrder: c.ordering };
      });
    },
    async getLayers() {
      const result = await fetch("/atlas/api/v1/layers/", {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch layers");
      }

      this.layerData = await result.json();
      this.layers = this.layerData.map((l) => {
        return { title: l.title, newOrder: l.ordering, id: l.id, category: l.category, currentOrder: l.ordering };
      });
    },
    async reload() {
      // Wait for updated layers and categories to be retrieved before reloading layers and categories.
      await this.getCategories();
      await this.getLayers();

      if (!this.selectedCategory) {
        this.selectedLayers = [];
        return;
      }

      this.selectedLayers = this.layers.filter((l) => {
        return l.category?.id === this.selectedCategory.id;
      });
      this.reorderSelectedLayers();
    },
    save() {
      const promises = [];
      for (const category of this.categories) {
        if (category.newOrder !== category.currentOrder) {
          promises.push(this.saveCategory(category));
        }
      }

      if (this.selectedLayers.length > 0) {
        for (const layer of this.selectedLayers) {
          if (layer.newOrder !== layer.currentOrder) {
            promises.push(this.saveLayer(layer));
          }
        }
      }

      Promise.all(promises).then(() => {
        // todo: add warning to user when one or more results failed see issue 437.
        this.reload();
      });
    },
    async saveCategory(category) {
      let result;
      const categoryBody = { id: category.id, title: category.title, ordering: category.newOrder };

      result = await fetch(`/atlas/api/v1/categories/${category.id}/`, {
        method: "PATCH",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": Cookies.get("csrftoken"),
        },
        body: JSON.stringify(categoryBody),
      });

      if (!result.ok) {
        const text = await result.text();
        console.error("Er is iets fout gegaan tijdens het opslaan.", text);
      }

      return result;
    },
    async saveLayer(layer) {
      let result;
      const currentLayer = this.layerData.find((l) => l.id === layer.id);
      const layerBody = { ...currentLayer, ordering: layer.newOrder };

      result = await fetch(`/atlas/api/v1/layers/${layer.id}/`, {
        method: "PATCH",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": Cookies.get("csrftoken"),
        },
        body: JSON.stringify(layerBody),
      });

      if (!result.ok) {
        const text = await result.text();
        console.error("Er is iets fout gegaan tijdens het opslaan.", text);
      }

      return result;
    },
    onCategoryMove() {
      this.reorderCategories();
      this.timeout = debounce(this.save, this.timeout, 2000);
    },
    onLayerMove() {
      this.reorderSelectedLayers();
      this.timeout = debounce(this.save, this.timeout, 2000);
    },
    reorderCategories() {
      this.categories = this.categories.map((category, index) => {
        return { ...category, newOrder: index + 1 };
      });
    },
    reorderSelectedLayers() {
      this.selectedLayers = this.selectedLayers.map((layer, index) => {
        return {
          ...layer,
          newOrder: index + 1,
        };
      });
    },
    selectRow(category) {
      if (this.selectedCategory?.id === category.id) {
        this.selectedCategory = null;
        return;
      }

      this.selectedCategory = category;
    },
    checkRow(category) {
      return this.selectedCategory?.id === category?.id;
    },
  },
};
</script>

<style scoped>
.ghost {
  opacity: 0.5;
  background: var(--color-primary);
}

.layer-table-wrapper {
  grid-area: layer-table;
}

.category-table-wrapper {
  grid-area: category-table;
}

.sort-container {
  display: grid;
  grid-template-areas: "category-table layer-table";
  grid-template-columns: 1fr 1fr;
  column-gap: 100px;
  padding-bottom: 50px;
}

@media (max-width: 576px) {
  .sort-container {
    grid-template-areas:
      "category-table"
      "layer-table";
    grid-template-columns: 1fr;
  }
}

.active-row {
  background: var(--color-primary-active);
  box-shadow: 3px 0 0 var(--color-primary) inset;
}

.sort-table {
  width: 100%;
  border-collapse: collapse;
  background: var(--color-white);
}

tbody > tr:hover {
  background-color: var(--color-primary-hover);
  cursor: move;
}

.sort-table thead tr th {
  text-align: left;
  font-weight: var(--font-weight-normal);
  color: var(--color-text-grey);
  padding-top: 10px;
  padding-bottom: 10px;
}

.sort-table tbody tr td {
  text-align: left;
  font-weight: var(--font-weight-normal);
  padding-top: 5px;
  padding-bottom: 5px;
}

tr.table-border:not(:last-child) > td,
th {
  border-bottom: 1px solid var(--color-grey-60);
}

tr > td:not(:nth-last-child(-n + 2)) {
  padding-right: 8px;
}

.sort-column-padding {
  padding: 0 12px;
}
</style>
