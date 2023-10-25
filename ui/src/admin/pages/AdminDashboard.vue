<template>
  <div class="container">
    <div class="section">
      <div class="buttons">
        <router-link to="/maps" class="button __tertiary __large"><MapIcon class="icon" />Kaarten</router-link>
        <router-link to="/sources" class="button __tertiary __large"><SourceIcon class="icon" />Bronnen</router-link>
        <router-link to="/layers" class="button __tertiary __large"><LayerIcon class="icon" />Kaartlagen</router-link>
        <router-link to="/categories" class="button __tertiary __large"
          ><CategoryIcon class="icon" />Categorieën</router-link
        >
      </div>
    </div>
  </div>
</template>

<script>
import MapIcon from "../../assets/icons/map-icon.svg";
import SourceIcon from "../../assets/icons/source-icon.svg";
import LayerIcon from "../../assets/icons/layer-icon.svg";
import CategoryIcon from "../../assets/icons/category-icon.svg";

export default {
  name: "AdminDashboard",
  components: {
    MapIcon,
    SourceIcon,
    LayerIcon,
    CategoryIcon,
  },
};
</script>

<style scoped>
.buttons {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  row-gap: 14px;
  column-gap: 14px;
}
</style>
