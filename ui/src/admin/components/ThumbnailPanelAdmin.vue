<template>
  <AdminSidePanel>
    <template #header>
      <button
        v-tippy="{ placement: 'bottom' }"
        class="iconbutton __normal __outline"
        type="button"
        aria-label="Ga terug"
        content="Terug"
        @click="() => emit('show-form')"
      >
        <ArrowLeftIcon class="icon" />
      </button>
      <h1>
        <ImageIcon class="icon" />
        Thumbnail
      </h1>
    </template>
    <template #default>
      <ConfirmPopup group="templating">
        <template #message="slotProps">
          <div class="tw-px-4">
            <i :class="slotProps.message.icon" class=""></i>
            <p>{{ slotProps.message.message }}</p>
          </div>
        </template>
      </ConfirmPopup>
      <Dialog
        :visible="showDialog"
        :modal="true"
        :closable="true"
        :draggable="false"
        :header="'Upload of wijzig thumbnail'"
        :dismissable-mask="true"
        class="tw-max-w-[90%] sm:tw-max-w-[80%] md:tw-max-w-[70%] tw-px-6"
        @update:visible="closeModal"
      >
        <div class="tw-flex tw-items-start tw-pb-4 tw-gap-10">
          <div v-if="thumbnail" class="tw-flex tw-flex-col tw-gap-2">
            Huidige thumbnail
            <Image
              :src="thumbnail"
              alt="Huidige gekozen thumbnail"
              image-class="tw-rounded-xl tw-border-1 tw-border-solid tw-border-gray-200"
              width="300"
            />
          </div>

          <div class="tw-flex tw-flex-col tw-gap-2">
            <div v-if="newThumbnail && !needsCropping" class="tw-flex tw-flex-col tw-gap-2">
              Geselecteerde thumbnail
              <Image
                :src="newThumbnail.objectURL ? newThumbnail.objectURL : newThumbnail"
                alt="Geselecteerde thumbnail"
                image-class="tw-rounded-xl tw-border-1 tw-border-solid tw-border-gray-200"
                width="300"
              />
            </div>

            <div v-if="newThumbnail && needsCropping" class="tw-flex tw-flex-col tw-gap-2">
              Bijsnijden vereist
              <cropper
                class="cropper"
                :src="newThumbnail.objectURL"
                :stencil-props="{ aspectRatio: 4 / 3 }"
                @change="change"
              />
            </div>

            <FileUploadAdmin :initial-thumbnail="thumbnail" @select-thumbnail="onSelectThumbnail" />
          </div>
        </div>

        <template #footer>
          <Button type="button" outlined class="!tw-font-medium" @click="closeModal">Annuleer</Button>
          <Button :disabled="newThumbnail === null" @click="uploadThumbnail">Selecteer en upload</Button>
        </template>
      </Dialog>

      <div v-if="thumbnail" class="tw-flex tw-flex-col tw-gap-2 tw-w-full tw-px-3">
        <h3 class="tw-mb-2">Geselecteerde thumbnail</h3>
        <Image
          :src="thumbnail"
          alt="Huidige thumbnail"
          image-class="tw-w-full tw-rounded-xl tw-border-1 tw-border-solid tw-border-gray-200"
        />
      </div>
      <div v-else class="tw-font-bold tw-px-3 tw-pt-4">Er is nog geen thumbnail geselecteerd</div>
      <div class="tw-flex tw-flex-col tw-gap-2 tw-px-3 tw-pt-4">
        <Button @click="openModal">
          {{ thumbnail ? "Wijzig thumbnail" : "Selecteer een thumbnail" }}
        </Button>
        <Button v-if="thumbnail" severity="danger" outlined @click="confirmDelete($event)">Verwijder </Button>
      </div>
    </template>
  </AdminSidePanel>
</template>
<script setup lang="ts">
import { ref, watch } from "vue";
import ArrowLeftIcon from "../../assets/icons/arrow-left-icon.svg";
import AdminSidePanel from "@/admin/components/AdminSidePanel.vue";
import FileUploadAdmin from "@/admin/components/FileUploadAdmin.vue";
import ImageIcon from "@/assets/icons/image-icon.svg";
import Cookies from "js-cookie";
import { useRoute } from "@/utils/inertia-routing";
import { Cropper } from "vue-advanced-cropper";
import { useConfirm, useToast } from "primevue";

const emit = defineEmits<{
  (e: "show-form"): void;
  (e: "update-map"): void;
}>();

interface Thumbnail {
  file: File;
  objectURL: string;
}

const props = defineProps<{
  initialThumbnail?: string | null;
}>();

const route = useRoute();
const thumbnail = ref<string | null | undefined>(props.initialThumbnail || null);
const newThumbnail = ref<Thumbnail | null>(null);
const croppedThumbnail = ref<Thumbnail | null>(null);
const showDialog = ref<boolean>(false);
const needsCropping = ref<boolean>(false);
const confirm = useConfirm();
const toast = useToast();

watch(
  () => props.initialThumbnail,
  (newVal) => {
    thumbnail.value = newVal || null;
  },
  { immediate: true },
);

const onSelectThumbnail = async (file: File | null) => {
  if (!file) return;

  newThumbnail.value = {
    file,
    objectURL: URL.createObjectURL(file),
  };

  // Check image aspect ratio before proceeding
  const { width, height } = await getImageDimensions(newThumbnail.value.file);
  const aspectRatio = width / height;
  const requiredRatio = 4 / 3;

  // Allow slight tolerance
  needsCropping.value = Math.abs(aspectRatio - requiredRatio) > 0.01;
};

const getImageDimensions = async (file: File): Promise<{ width: number; height: number }> => {
  const bitmap = await createImageBitmap(file);
  return { width: bitmap.width, height: bitmap.height };
};

const change = ({ canvas }: { canvas: HTMLCanvasElement | null }) => {
  if (!canvas) return;

  canvas.toBlob((blob) => {
    if (blob) {
      const file = new File([blob], "cropped-thumbnail.png", { type: "image/png" });
      croppedThumbnail.value = {
        file,
        objectURL: URL.createObjectURL(file), // Create an object URL
      };
    }
  }, "image/png"); // Save cropped image
};

const uploadThumbnail = async (): Promise<void> => {
  try {
    if (needsCropping.value && croppedThumbnail.value) {
      newThumbnail.value = croppedThumbnail.value;
    }

    if (!newThumbnail.value) return;

    const formData = new FormData();
    formData.append("file", newThumbnail.value.file);

    const headers = new Headers();
    headers.append("X-CSRFToken", Cookies.get("csrftoken") || "");

    const response = await fetch(`/atlas/api/v1/maps/${route.params.id}/upload_thumbnail/`, {
      method: "POST",
      credentials: "same-origin",
      headers: headers,
      body: formData,
    });

    if (!response.ok) {
      throw new Error("Upload failed");
    }

    toast.add({
      severity: "success",
      summary: "Thumbnail succesvol geüpload",
      detail: "Het uploaden van de thumbnail is succesvol afgerond",
      life: 5000,
    });

    emit("update-map");
    closeModal();
  } catch (error) {
    // todo: add more error details for the user
    console.error("Upload error:", error);
    toast.add({
      severity: "error",
      summary: "Fout bij uploaden",
      detail: "Er is iets misgegaan bij het uploaden van de thumbnail.",
      life: 5000,
    });
  }
};

const deleteThumbnail = async (): Promise<void> => {
  try {
    const headers = new Headers();
    headers.append("X-CSRFToken", Cookies.get("csrftoken") || "");
    const result = await fetch(`/atlas/api/v1/maps/${route.params.id}/delete_thumbnail/`, {
      method: "DELETE",
      credentials: "same-origin",
      headers: headers,
    });

    if (!result.ok) {
      console.error("Er is iets fout gegaan bij het verwijderen van de thumbnail");
    } else {
      toast.add({
        severity: "success",
        summary: "Thumbnail succesvol verwijderd",
        detail: `Het verwijderen van de thumbnail op de kaart is gelukt`,
        life: 5000,
      });
      emit("update-map");
    }
  } catch (error) {
    console.error("Delete error:", error);
    toast.add({
      // todo: add more error details for the user
      severity: "error",
      summary: "Fout bij verwijderen",
      detail: "Er is iets misgegaan bij het verwijderen van de thumbnail.",
      life: 5000,
    });
  }
};

const confirmDelete = (event: MouseEvent) => {
  if (!event) {
    return;
  }

  confirm.require({
    target: event.target as HTMLElement,
    group: "templating",
    message: `Weet u zeker dat u de geselecteerde thumbnail wilt verwijderen?`,
    rejectProps: {
      icon: "pi pi-times",
      label: "Annuleer",
      outlined: true,
    },
    acceptProps: {
      icon: "pi pi-trash",
      label: "Verwijder",
    },
    accept: () => {
      deleteThumbnail();
    },
    reject: () => {},
  });
};

const openModal = () => {
  showDialog.value = true;
};

const closeModal = () => {
  if (newThumbnail.value?.objectURL) {
    URL.revokeObjectURL(newThumbnail.value.objectURL);
  }
  if (croppedThumbnail.value?.objectURL) {
    URL.revokeObjectURL(croppedThumbnail.value.objectURL);
  }

  newThumbnail.value = null;
  croppedThumbnail.value = null;
  needsCropping.value = false;
  showDialog.value = false;
};
</script>

<style scoped>
.cropper {
  height: 400px;
  width: 400px;
  background: #ddd;
}

@media (min-width: 1200px) {
  .cropper {
    height: 450px;
    width: 600px;
  }
}

@media (min-width: 1660px) {
  .cropper {
    height: 600px;
    width: 750px;
  }
}
</style>
