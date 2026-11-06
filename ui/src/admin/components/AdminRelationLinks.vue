<template>
  <div v-if="links.length" class="tw-mt-3 tw-flex tw-flex-wrap tw-gap-2">
    <router-link v-for="link in links" :key="link.id" v-slot="{ href }" custom :to="`/${resource}/update/${link.id}`">
      <Button
        as="a"
        :href="href"
        target="_blank"
        rel="noopener"
        :label="`Bekijk ${link.label}`"
        icon="pi pi-external-link"
        severity="secondary"
        outlined
        class="!tw-no-underline"
        :aria-label="`Open ${relationName} ${link.label} in een nieuw tabblad`"
      />
    </router-link>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { getRelationLinks, type IRelationOption } from "@/admin/utils/relation-links";

interface IAdminRelationLinksProps {
  resource: string;
  value: unknown;
  options?: IRelationOption[];
}

const props = withDefaults(defineProps<IAdminRelationLinksProps>(), {
  options: () => [],
});

const links = computed(() => getRelationLinks(props.value, props.options));

const relationNames: Record<string, string> = {
  categories: "categorie",
  groups: "groep",
  maps: "kaart",
  sources: "bron",
  tables: "tabel",
};

const relationName = computed(() => relationNames[props.resource] || "relatie");
</script>
