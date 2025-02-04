<template>
  <Dialog
    :visible="showDialog"
    :modal="true"
    :closable="true"
    :draggable="false"
    :header="'Kaart printen'"
    :dismissable-mask="true"
    class="tw-w-[90%] md:tw-w-[50%]"
    @update:visible="closeModal"
  >
    <form method="POST" class="tw-flex tw-flex-col tw-gap-4" @submit="onSubmit">
      <div class="tw-flex tw-flex-col tw-gap-4 ">
        <div class="tw-flex tw-flex-col">
          <label class="label" for="title">Titel</label>
          <InputText id="title" v-model="title" class="input" name="title" placeholder="Kies optioneel een titel" />
        </div>

        <div class="tw-flex tw-flex-col">
          <label class="label" for="remarks">Opmerkingen</label>
          <Textarea
            id="remarks"
            v-model="remarks"
            class="input"
            name="remarks"
            rows="3"
            auto-resize
            placeholder="Plaats optioneel opmerkingen"
          />
        </div>
      </div>

      <div class="tw-flex tw-flex-col tw-gap-4 tw-w-full">
        <div class="tw-flex tw-flex-col md:tw-grid md:tw-grid-cols-2 tw-gap-4">
        <div class="tw-flex tw-flex-col">
          <label class="label" for="format">Formaat</label>
          <Select
            id="format"
            v-model="format"
            class="tw-w-full"
            name="format"
            :options="availableFormats"
            option-label="label"
            option-value="value"
          />
        </div>

        <div class="tw-flex tw-flex-col">
          <label class="label" for="orientation">Orientatie</label>
          <Select
            id="orientation"
            v-model="orientation"
            class="tw-w-full"
            name="orientation"
            :options="availableOrientations"
            option-label="label"
            option-value="value"
          />
        </div>
      </div>

        <div class="tw-flex tw-gap-2 tw-justify-between tw-w-full tw-mt-4">
          <label class="label" for="showLegend">Toon legenda</label>
          <ToggleSwitch id="showLegend" v-model="showLegend" name="showLegend" />
        </div>

        <div class="tw-flex tw-gap-2 tw-justify-between tw-w-full">
          <label class="label" for="showDateTime">Toon datum/tijd</label>
          <ToggleSwitch id="showDateTime" v-model="showDateTime" name="showDateTime" />
        </div>

        <div class="tw-flex tw-gap-2 tw-justify-between tw-w-full">
          <label class="label" for="showScale">Toon schaal</label>
          <ToggleSwitch id="showScale" v-model="showScale" name="showScale" />
        </div>

        <div class="tw-flex tw-gap-2 tw-justify-between tw-w-full">
          <div class="tw-flex tw-gap-2 tw-items-center">
            <label class="label tw-flex tw-gap-2 tw-items-center" for="showLogo">
              Toon organisatielogo
              <Button
                v-if="!config?.organization_logo"
                type="button"
                icon="pi pi-info-circle"
                variant="text"
                rounded
                class="p-button-plain"
                v-tooltip.top="'Deze optie is beschikbaar wanneer het organisatielogo ingesteld is.'"
              />
            </label>
          </div>
          <ToggleSwitch id="showLogo" class="tw-flex-shrink-0" v-model="showLogo" name="showLogo" :disabled="!config?.organization_logo" />
        </div>

        <div class="tw-flex tw-gap-2 tw-justify-between tw-w-full">
          <label class="label" for="showNorth">Toon noordpijl</label>
          <ToggleSwitch id="showNorth" v-model="showNorth" name="showNorth" />
        </div>
      </div>
    </form>
    <template #footer>
      <Button type="button" outlined class="!tw-font-medium" @click="closeModal">Sluiten</Button>
      <Button type="button" class="!tw-font-medium" :disabled="loading" @click="onSubmit">
          <i v-if="loading" class="pi pi-spin pi-spinner-dotted"></i>
          Afdrukken
      </Button>
    </template>
  </Dialog>
</template>

<script>
import { mapState } from "pinia";
import { useGlobalStore } from "@/stores";

export default {
  name: "PrintModal",
  props: {
    loading: Boolean,
  },
  emits: ["toggle-modal", "print-map-to-pdf"],
  data() {
    return {
      showDialog: true,
      title: "",
      remarks: "",
      format: "a4",
      orientation: "landscape",
      showLegend: true,
      showDateTime: true,
      showScale: true,
      showLogo: false,
      showNorth: true,
      availableFormats: [
        { label: "A4", value: "a4" },
        { label: "A3", value: "a3" },
        { label: "A2", value: "a2" },
        { label: "A1", value: "a1" },
        { label: "A0", value: "a0" },
      ],
      availableOrientations: [
        { label: "Liggend", value: "landscape" },
        { label: "Staand", value: "portrait" },
      ],
    };
  },
  computed: {
    ...mapState(useGlobalStore, ["config"])
  },
  watch: {
    config: {
      immediate: true,
      handler(newConfig) {
        this.showLogo = !!newConfig?.organization_logo;
      }
    }
  },
  methods: {
    closeModal() {
      this.showDialog = false;
      this.$emit("toggle-modal", "");
    },
    onSubmit(e) {
      e.preventDefault();

      this.$emit("print-map-to-pdf", {
        title: this.title,
        remarks: this.remarks,
        format: this.format,
        orientation: this.orientation,
        showLegend: this.showLegend,
        showDateTime: this.showDateTime,
        showScale: this.showScale,
        showLogo: this.showLogo,
        showNorth: this.showNorth,
      });
    },
  },
};
</script>

<style scoped>
.label {
  font-size: var(--font-size-normal);
  font-weight: var(--font-weight-bold);
}

.input {
  width: 100%;
  margin-top: 5px;
  border: 1px solid var(--color-grey-80);
  border-radius: var(--radius-small);
  padding: 10px 15px;
  height: 40px;
  font-family: var(--font-family);
  font-size: var(--font-size-small);
  font-weight: var(--font-weight-normal);
  line-height: 1.5;
}
</style>
