<template>
  <div v-if="routeArray.length >= 1" class="breadcrumb-wrapper container __admin">
    <ul class="breadcrumb">
      <li>
        <router-link class="text-button" to="/">Home</router-link>
        <span class="grey">/</span>
      </li>
      <li v-for="(crumb, index) in breadcrumbs" :key="crumb.path">
        <router-link v-if="index < breadcrumbs.length - 1" class="text-button" :to="`/${crumb.path}`"
          >{{ crumb.name }}
        </router-link>
        <span v-if="index < breadcrumbs.length - 1" class="grey">/</span>
        <span v-else class="grey">{{ crumb.name }}</span>
      </li>
    </ul>
  </div>
</template>

<script>
import { useRoute } from "@/utils/inertia-routing";

export default {
  name: "AdminBreadcrumb",
  data() {
    return {
      route: null,
      router: null,
      routeArray: [],
      breadcrumbs: [],
    };
  },
  watch: {
    route: {
      handler(value) {
        if (!value.meta.menu) {
          return [];
        }

        this.routeArray = value.fullPath.split("/");
        // Remove root and Id values from route.
        this.routeArray = this.routeArray.filter((item) => item !== "" && !/^\d+$/.test(item));
        this.breadcrumbs = this.routeArray.map((item, index) => {
          const name = index >= this.routeArray.length - 1 ? value.meta.title : value.meta.breadcrumb[item].title;
          return { path: item, name: name };
        });
      },
      deep: true,
    },
  },
  created() {
    this.route = useRoute();
  },
};
</script>

<style scoped>
.breadcrumb-wrapper {
  padding: 12px 20px;
}

@media (min-width: 1024px) {
  .breadcrumb-wrapper {
    padding: 12px 32px;
  }
}

ul.breadcrumb > li {
  display: flex;
  align-items: center;
  float: left;
  gap: 6px;
  padding-right: 6px;
}

.text-button {
  color: var(--color-text-grey);
  font-weight: var(--font-weight-normal);
  background-color: transparent;
}

.grey {
  color: var(--color-text-grey);
}
</style>
