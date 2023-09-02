<template>
  <div class="container">
    <div class="top-menu-container">
      <router-link to="/layers/create" class="button __tertiary __large">
        <add-icon />
        <span style="padding-right: 6px">Maak laag</span>
      </router-link>
      <button class="button __tertiary __large" @click="openFormModal">Nieuwe laag</button>
      <div class="search-wrapper">
        <svg
          width="18px"
          height="18px"
          viewBox="0 0 18 18"
          version="1.1"
          xmlns="http://www.w3.org/2000/svg"
          xmlns:xlink="http://www.w3.org/1999/xlink"
        >
          <g id="Admin" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
            <g id="Kaart---Lagen" transform="translate(-45.000000, -183.000000)" fill="#000000" fill-rule="nonzero">
              <g id="search_black_24dp" transform="translate(42.000000, 180.000000)">
                <path
                  id="Shape"
                  d="M15.5,14 L14.71,14 L14.43,13.73 C15.41,12.59 16,11.11 16,9.5 C16,5.91 13.09,3 9.5,3 C5.91,3 3,5.91 3,9.5 C3,13.09 5.91,16 9.5,16 C11.11,16 12.59,15.41 13.73,14.43 L14,14.71 L14,15.5 L19,20.49 L20.49,19 L15.5,14 Z M9.5,14 C7.01,14 5,11.99 5,9.5 C5,7.01 7.01,5 9.5,5 C11.99,5 14,7.01 14,9.5 C14,11.99 11.99,14 9.5,14 Z"
                ></path>
              </g>
            </g>
          </g>
        </svg>
        <input id="layers-search" v-model="searchQuery" type="search" name="query" placeholder="Zoek laag" />
      </div>
    </div>

    <FormModal v-show="showFormModal" @close="closeFormModal">
      <template #header> header </template>
      <template #body> body </template>
    </FormModal>

    <div v-if="visibleLayers.length > 0" class="layers-list-wrapper">
      <PaginationComponent :items="visibleLayers" :nr-of-records="nrOfRecords" @page-change="(pageNumber) => (currentPageNumber = pageNumber)">
        <template #default>
          <ul class="layers-list">
            <li v-for="layer in paginatedData" :key="layer.id">
              <div class="menu-item-wrapper">
                <router-link class="layer-item-wrapper" :to="`/layers/update/${layer.id}`">
                  {{ layer.title }}
                </router-link>
                <button
                  v-tippy="{ placement: 'bottom' }"
                  class="iconbutton __normal __round"
                  aria-label="Verwijder laag"
                  content="Verwijder"
                  type="button"
                  @click="deleteLayer(layer)"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 0 24 24" width="24px" fill="#000000">
                    <path d="M0 0h24v24H0V0z" fill="none" />
                    <path d="M16 9v10H8V9h8m-1.5-6h-5l-1 1H5v2h14V4h-3.5l-1-1zM18 7H6v12c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7z" />
                  </svg>
                </button>
              </div>
            </li>
          </ul>
        </template>
      </PaginationComponent>
    </div>
  </div>
</template>

<script>
import AddIcon from "../../icons/AddIcon.vue";
import Cookies from "js-cookie";
import PaginationComponent from "@/components/Pagination.vue";
import FormModal from "@/components/FormModal.vue";

export default {
  name: "LayerList",
  components: { FormModal, PaginationComponent, AddIcon },
  data() {
    return {
      layers: [],
      searchQuery: "",
      currentPageNumber: 1,
      nrOfRecords: 10,
      showFormModal: false,
    };
  },
  computed: {
    visibleLayers() {
      if (!this.searchQuery) {
        return this.layers;
      }

      return this.layers.filter((layer) => layer.title.toLowerCase().search(this.searchQuery.toLowerCase()) !== -1);
    },
    paginatedData() {
      const start = (this.currentPageNumber - 1) * this.nrOfRecords;
      const end = start + this.nrOfRecords;
      return this.visibleLayers.slice(start, end);
    },
  },
  created() {
    this.getLayers();
  },
  methods: {
    async getLayers() {
      const result = await fetch("/atlas/api/v1/layers/", {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch layers");
      }

      this.layers = await result.json();
    },
    async deleteLayer(layer) {
      const acknowledged = confirm("Weet je zeker dat je de laag wil verwijderen?");
      if (!acknowledged) {
        return;
      }

      const result = await fetch(`/atlas/api/v1/layers/${layer.id}/`, {
        method: "DELETE",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": Cookies.get("csrftoken"),
        },
      });

      if (result.ok) {
        this.getLayers();
      }
    },
    openFormModal() {
      this.showFormModal = true;
    },
    closeFormModal() {
      this.showFormModal = false;
    },
  },
};
</script>

<style scoped>
.top-menu-container {
  width: 70%;
  padding: 20px 0;
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.layers-list-wrapper {
  width: clamp(335px, 70%, 800px);
}

ul.layers-list > li:not(:last-child) {
  border-bottom: 1px solid var(--color-grey-60);
}

.menu-item-wrapper {
  display: flex;
  align-items: center;
}

.button {
  max-width: 300px;
}

/* todo: use margin: 0 auto for reactive centering */
.search-wrapper {
  width: clamp(250px, 35%, 400px);
  position: relative;
  /* margin-left: auto; */
  border: 2px solid var(--color-grey-60);
  border-radius: var(--radius-normal);
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

.layer-item-wrapper {
  display: flex;
  align-items: center;
  flex-grow: 1;
  text-decoration: none;
  color: var(--color-text-grey);
  border-radius: var(--radius-normal);
  padding: 10px 10px;
}

.layer-item-wrapper:hover {
  background: var(--color-grey-40);
}
</style>
