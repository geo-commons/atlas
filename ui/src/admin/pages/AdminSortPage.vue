<template>
  <div class="container __admin">
    <div class="page-title-wrapper">
      <h1>Sortering</h1>
      <button
        class="button __secondary_admin __normal top-menu-button"
        type="button"
        aria-label="Ga terug"
        @click="back"
      >
        <arrow-left-icon class="icon" />
        Terug
      </button>
    </div>

    <Message severity="info" icon="pi pi-info-circle" :closable="false">
      <p>Sleep de categorieën en kaartlagen naar de gewenste volgorde.</p>
    </Message>

    <div class="tw-pb-4 tw-my-4">
      <button
        type="button"
        class="tw-text-sm tw-bg-transparent hover:tw-underline hover:tw-text-admin-primary"
        @click="showKeyboardInstructions = !showKeyboardInstructions"
        @keydown.enter.prevent="showKeyboardInstructions = !showKeyboardInstructions"
        v-text="keyboardInstructionsButtonText"
      />
      <p
        v-if="showKeyboardInstructions"
        v-text="
          'Selecteer en deselecteer een actief element met behulp van de spatiebalk. Verplaats met behulp van pijlen omhoog en omlaag het element naar de gewenste plek.'
        "
      />

      <div id="reorder_instructions" aria-live="assertive" class="sr-only" v-text="assistiveText" />
    </div>

    <div class="sort-container">
      <SortableList
        :current-item-list="categories"
        :title="'Categorieën'"
        :group="'categories'"
        :selectable-items="true"
        class="category-table"
        @updateList="(newCategories) => updateCategories(newCategories)"
        @item-selected="(selectedItem) => selectCategory(selectedItem)"
      />

      <SortableList
        v-if="selectedCategory"
        :current-item-list="selectedLayers"
        :title="'Kaartlagen'"
        :group="'layers'"
        class="layer-table"
        @updateList="(newLayers) => updateLayers(newLayers)"
      >
        <template #empty-list>De geselecteerde categorie heeft geen bijbehorende kaartlagen.</template>
      </SortableList>
      <div v-else class="help-text-wrapper"><p>Selecteer een categorie om de bijbehorende lagen te sorteren.</p></div>
    </div>
  </div>
</template>

<script>
import Cookies from "js-cookie";
import ArrowLeftIcon from "../../assets/icons/arrow-left-icon.svg";
import SortableList from "@/admin/components/SortableList.vue";
import { getAllObjects } from "@/utils/api-helpers";

export default {
  name: "AdminSortPage",
  components: {
    SortableList,
    ArrowLeftIcon,
  },
  data() {
    return {
      categories: [],
      layers: [],
      layerData: {},
      selectedCategory: null,
      selectedLayers: [],
      showKeyboardInstructions: false,
      assistiveText: "Selecteer een element met behulp van de spatiebalk",
    };
  },
  computed: {
    keyboardInstructionsButtonText() {
      return this.showKeyboardInstructions ? "Verberg toetsenbord instructies" : "Toon toetsenbord instructies";
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
      const url = getAllObjects("/atlas/api/v1/categories/");
      const result = await fetch(url, {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch categories");
      }

      const response = await result.json();
      this.categories = response.results.map((c, index) => {
        return { title: c.title, newOrder: index, id: c.id, currentOrder: c.ordering };
      });
    },
    async getLayers() {
      const url = getAllObjects("/atlas/api/v1/layers/");
      const result = await fetch(url, {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch layers");
      }

      const response = await result.json();
      this.layerData = response.results;
      this.layers = this.layerData.map((l) => {
        return { title: l.title, newOrder: l.ordering, id: l.id, category: l.category, currentOrder: l.ordering };
      });
    },
    async reload() {
      // Wait for updated categories to be retrieved before reloading categories.
      await this.getCategories();

      if (!this.selectedCategory) {
        this.selectedLayers = [];
        return;
      }

      // Wait for updated layers to be retrieved before reloading layers.
      await this.getLayers();

      this.selectedLayers = this.layers.filter((l) => {
        return l.category?.id === this.selectedCategory.id;
      });
      this.reorderSelectedLayers();
    },
    updateCategories(newCategories) {
      this.categories = newCategories;
      this.save();
    },
    updateLayers(newLayers) {
      this.selectedLayers = newLayers;
      this.save();
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
      const categoryBody = { id: category.id, ordering: category.newOrder };

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
      const layerBody = { id: layer.id, ordering: layer.newOrder };

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
    reorderSelectedLayers() {
      this.selectedLayers = this.selectedLayers.map((layer, index) => {
        return {
          ...layer,
          newOrder: index,
        };
      });
    },
    back() {
      this.$router.push(`/${this.$route.params.parentRoute}`);
    },

    selectCategory(category) {
      this.selectedCategory = category;
    },
  },
};
</script>

<style scoped>
.page-title-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  padding-bottom: 24px;
}

.layer-table {
  grid-area: layer-table;
}

.category-table {
  grid-area: category-table;
}

.sort-container {
  display: grid;
  grid-template-areas: "category-table layer-table";
  grid-template-columns: 1fr 1fr;
  column-gap: 100px;
  padding-bottom: 50px;
}

.help-text-wrapper {
  display: flex;
  align-items: center;
}

@media (max-width: 576px) {
  .page-title-wrapper {
    flex-direction: column;
    align-items: flex-start;
  }

  .top-menu-button {
    width: 100%;
  }
}

@media (max-width: 768px) {
  .sort-container {
    grid-template-areas:
      "category-table"
      "layer-table";
    grid-template-columns: 1fr;
  }
}
</style>
