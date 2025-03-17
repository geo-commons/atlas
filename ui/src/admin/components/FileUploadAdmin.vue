<template>
  <div class="tw-flex tw-flex-col tw-justify-start tw-gap-2">
    <span v-if="newThumbnailSelected">Selecteer een afbeelding</span>
    <div
      :class="
        newThumbnailSelected
          ? 'tw-flex tw-justify-center tw-items-center tw-border-dashed tw-rounded-xl tw-border-gray-300 tw-w-[300px] tw-h-[225px]'
          : 'tw-flex tw-justify-start'
      "
    >
      <FileUpload
        mode="basic"
        custom-upload
        auto
        severity="secondary"
        accept="image/jpeg, image/png, image/jpg"
        :choose-label="src ? 'Wijzig' : 'Kies een bestand'"
        :show-upload-button="false"
        :show-cancel-button="false"
        :max-file-size="MAX_FILE_SIZE"
        :invalid-file-size-message="'Bestandsgrootte mag niet groter zijn dan 10MB'"
        :invalid-file-type-message="'Ongeldig bestandstype. Gebruik een JPG of PNG.'"
        @select="onFileSelect"
      >
      </FileUpload>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";
import type { FileUploadSelectEvent } from "primevue/fileupload";
import { ALLOWED_TYPES, MAX_FILE_SIZE } from "@/constants/file-upload";
import { useToast } from "primevue";

const props = defineProps<{
  initialThumbnail?: string | null;
}>();

const emit = defineEmits<{
  (e: "select-thumbnail", file: File): void;
}>();

const toast = useToast();
const src = ref<string | null | undefined>(props.initialThumbnail);
const newThumbnailSelected = computed(() => props.initialThumbnail === src.value);

const onFileSelect = (event: FileUploadSelectEvent) => {
  const file = event.files[0];

  if (!ALLOWED_TYPES.includes(file.type)) {
    toast.add({
      severity: "error",
      summary: "Fout bij selecteren afbeelding",
      detail: "Ongeldig bestandstype. Gebruik een JPG of PNG.",
      life: 5000,
    });
    return;
  }

  const reader = new FileReader();

  reader.onload = async (e) => {
    src.value = e.target?.result as string;
  };

  reader.readAsDataURL(file);
  emit("select-thumbnail", file);
};
</script>
