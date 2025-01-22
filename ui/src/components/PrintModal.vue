<template>
  <Dialog
    :visible="showDialog"
    :modal="true"
    :closable="true"
    :draggable="false"
    :header="'Kaart printen'"
    :dismissable-mask="true"
    class="tw-w-[60%]"
    @update:visible="closeModal"
  >
    <form method="POST" class="tw-flex tw-flex-col tw-gap-4" @submit="onSubmit">
      <div class="tw-flex tw-flex-col tw-gap-4 tw-w-[50%]">
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

      <div class="tw-flex tw-flex-col tw-gap-4 tw-w-full md:tw-w-56">
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
          <label class="label" for="showLogo">Toon organisatielogo</label>
          <ToggleSwitch id="showLogo" v-model="showLogo" name="showLogo" />
        </div>

        <div class="tw-flex tw-gap-2 tw-justify-between tw-w-full">
          <label class="label" for="showNorth">Toon noordpijl</label>
          <ToggleSwitch id="showNorth" v-model="showNorth" name="showNorth" />
        </div>
      </div>
      <div class="tw-flex tw-gap-2 tw-mt-4">
        <Button type="submit" class="!tw-font-medium" :disabled="loading">
          <i v-if="loading" class="pi pi-spin pi-spinner-dotted"></i>
          Afdrukken
        </Button>
        <Button type="button" outlined class="!tw-font-medium" @click="closeModal">Sluit</Button>
      </div>
    </form>
  </Dialog>
</template>

<script>
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
      showLogo: true,
      showNorth: true,
      availableFormats: [
        { label: "A4", value: "a4" },
        { label: "A3", value: "a3" },
        { label: "A2", value: "a2" },
        { label: "A1", value: "a1" },
        { label: "A0", value: "a0" },
      ],
      availableOrientations: [
        { label: "Staand", value: "landscape" },
        { label: "Liggend", value: "portrait" },
      ],
    };
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
