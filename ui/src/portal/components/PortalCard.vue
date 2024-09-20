<template>
  <a class="card-link" :href="objectUrl">
    <img v-if="showThumbnail" :src="getImageUrl" alt="Voorbeeldweergave themakaart" class="thumbnail" />
    <h3 class="brand-color">{{ title }}</h3>
    <p v-if="summary">{{ summary }}</p>
  </a>
</template>

<script>
import defaultMapsThumbnail from "@/assets/images/default_map_thumbnail.png";
import defaultTableThumbnail from "@/assets/images/default_table_thumbnail.png";
import defaultDatasetThumbnail from "@/assets/images/default_dataset_thumbnail.png";

export default {
  name: "PortalCard",
  props: {
    thumbnail: String,
    title: String,
    summary: String,
    objectUrl: String,
    objectType: String,
    showThumbnail: {
      default: false,
      type: Boolean,
    },
  },
  computed: {
    getImageUrl() {
      if (!this.thumbnail) {
        switch (this.objectType) {
          case "map":
            return defaultMapsThumbnail;
          case "table":
            return defaultTableThumbnail;
          case "dataset":
            return defaultDatasetThumbnail;
        }
      }
      return this.thumbnail;
    },
  },
};
</script>

<style scoped>
.card-link {
  text-decoration: none;
  color: var(--color-black);
  padding: 0;
  width: 100%;
}

.card-link:hover {
  cursor: pointer;
}

.card-link:focus {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

.card-link:hover > h3 {
  text-decoration: underline;
}

h3 {
  margin: 0;
  font-size: var(--font-size-large);
}

p {
  margin: 0;
  font-size: var(--font-size-small);
}

.thumbnail {
  object-fit: cover;
  height: auto;
  width: 100%;
  border: 1px solid var(--color-grey-50);
}

@media (min-width: 1024px) {
  h3 {
    font-size: var(--font-size-xl);
  }

  p {
    font-size: var(--font-size-normal);
  }

  .card-link {
    max-width: 280px;
  }
}

@media (max-width: 660px) {
  .thumbnail {
    max-height: 200px;
  }
}
</style>
