<template>
  <div v-if="routeArray.length >= 1" class="tw-bg-white tw-border-b tw-border-gray-200">
    <div class="tw-max-w-7xl tw-mx-auto tw-px-6 tw-py-3">
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
  </div>
</template>

<script>
import { useRoute } from "@/utils/inertia-routing";

export default {
  name: "PortalBreadcrumb",
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
        this.routeArray = value.fullPath.split("/");
        this.routeArray = this.routeArray.filter((item) => item !== "" && !item.startsWith("?"));
        this.breadcrumbs = this.routeArray.map((item, index) => {
          const name = index >= this.routeArray.length - 1 ? value.meta.breadcrumb : value.meta.parentName;
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
}

.grey {
  color: var(--color-text-grey);
}
</style>
