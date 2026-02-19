<template>
  <PortalListCard v-if="layoutMode === LayoutMode.List" v-bind="cardProps" />
  <PortalGridCard v-else v-bind="cardProps" />
</template>

<script setup lang="ts">
import PortalGridCard from "@/portal/components/PortalGridCard.vue";
import PortalListCard from "@/portal/components/PortalListCard.vue";
import { LayoutMode, type PortalCardProps } from "@/portal/components/shared/portalCardShared";
import { computed } from "vue";

defineOptions({ name: "PortalCard" });

interface PortalCardWrapperProps extends PortalCardProps {
  layoutMode?: LayoutMode;
}

const props = withDefaults(defineProps<PortalCardWrapperProps>(), {
  thumbnail: null,
  summary: null,
  showThumbnail: false,
  lastUpdated: null,
  category: null,
  layoutMode: LayoutMode.Grid,
});
const cardProps = computed(() => {
  const { layoutMode, ...rest } = props;
  void layoutMode;
  return rest;
});
</script>
