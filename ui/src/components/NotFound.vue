<template>
  <div class="tw-flex tw-w-full tw-h-full tw-flex-col md:tw-flex-row bg-404 tw-fixed tw-top-0 tw-z-10">
    <div
      class="content tw-flex tw-flex-col tw-justify-center tw-h-auto md:tw-h-screen md:tw-p-24 tw-p-8 tw-pb-24 tw-bg-white tw-w-full tw-items-start md:tw-min-w-[500px] md:tw-w-1/4"
    >
      <h1 class="tw-text-5xl tw-font-bold tw-text-black tw-mb-4">{{ props.code || "404" }}</h1>
      <h2 class="tw-mb-0">{{ props.title }}</h2>
      <p class="tw-leading-6">{{ props.message }}</p>
      <a class="button __secondary_admin" :href="props.linkUrl">{{ props.linkText }}</a>
    </div>
    <div class="tw-relative tw-w-full tw-h-full tw-overflow-hidden">
      <div class="tw-absolute tw-bottom-0 tw-left-0 tw-max-w-[500px] tw-w-[40%]">
        <MapSvg class="tw-w-full tw-h-full" aria-label="Kaart illustratie" role="img" />
      </div>

      <div class="tw-absolute tw-top-0 tw-right-0 tw-max-w-[500px] tw-w-[40%]">
        <MapSvg class="tw-w-full tw-h-full" aria-label="Kaart illustratie" role="img" />
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import MapSvg from "@/assets/images/map.svg";
import "../assets/styles/main.css";

interface NotFoundProps {
  code: string;
  title: string;
  message: string;
  linkUrl: string;
  linkText: string;
}

const props = withDefaults(defineProps<NotFoundProps>(), {
  code: "404",
  title: "Oeps, verdwaald?",
  message: "De opgevraagde pagina bestaat niet (meer) of de URL is onjuist.",
  linkUrl: "/atlas/",
  linkText: "Terug naar de hoofdkaart",
});
</script>

<style scoped>
.bg-404 {
  margin: 0;
  padding: 0;
  background-color: #f6f6ff;
  overflow: hidden;
}
</style>
