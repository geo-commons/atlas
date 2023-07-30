<template>
  <div class="overlay">
    <button class="background" @click="closeModal" />
    <div class="modal">
      <form method="POST" @submit="onSubmit">
        <div class="input-container">
          <label class="label" for="title">Titel</label>
          <input
            id="title"
            v-model="title"
            class="input"
            name="title"
            placeholder="Kies optioneel een titel"
          />
        </div>
        <div class="input-container">
          <label class="label" for="remarks">Opmerkingen</label>
          <textarea
            id="remarks"
            v-model="remarks"
            class="input"
            name="remarks"
            placeholder="Plaats optioneel opmerkingen"
          />
        </div>
        <div class="input-container">
          <label class="label" for="format">Formaat</label>
          <select id="format" v-model="format" class="select" name="format">
            <option value="a0">A0</option>
            <option value="a1">A1</option>
            <option value="a2">A2</option>
            <option value="a3">A3</option>
            <option value="a4">A4</option>
          </select>
        </div>

        <div class="input-container">
          <label class="label" for="orientation">Orientatie</label>
          <select
            id="orientation"
            v-model="orientation"
            class="select"
            name="orientation"
          >
            <option value="landscape">Liggend</option>
            <option value="portrait">Staand</option>
          </select>
        </div>

        <div class="input-container">
          <label class="label" for="showLegend">Toon legenda</label>
          <select
            id="showLegend"
            v-model="showLegend"
            class="select"
            name="showLegend"
          >
            <option :value="true">Ja</option>
            <option :value="false">Nee</option>
          </select>
        </div>

        <div class="input-container">
          <label class="label" for="showLegend">Toon datum/tijd</label>
          <select
            id="showDateTime"
            v-model="showDateTime"
            class="select"
            name="showDateTime"
          >
            <option :value="true">Ja</option>
            <option :value="false">Nee</option>
          </select>
        </div>

        <div class="input-container">
          <label class="label" for="showLegend">Toon schaal</label>
          <select
            id="showScale"
            v-model="showScale"
            class="select"
            name="showScale"
          >
            <option :value="true">Ja</option>
            <option :value="false">Nee</option>
          </select>
        </div>

        <button type="submit" class="button __primary">Afdrukken</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: "PrintModal",
  data() {
    return {
      title: "",
      remarks: "",
      format: "a4",
      orientation: "landscape",
      showLegend: true,
      showDateTime: true,
      showScale: true,
    };
  },
  methods: {
    closeModal() {
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
      });
    },
  },
};
</script>

<style scoped>
.overlay {
  position: fixed;
  z-index: 10;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow-y: auto;
}

.background {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.4);
}

.buttons {
  position: absolute;
  top: calc((var(--width-button-normal) + 8px) * -1);
  right: -8px;
  padding: 8px 8px 0;
  overflow: hidden;
}

.iconbutton {
  width: var(--width-button-normal);
  height: var(--width-button-normal);
  border-top-left-radius: var(--radius-normal);
  border-top-right-radius: var(--radius-normal);
  background: white;
  box-shadow: var(--shadow-normal);
}

.modal {
  position: relative;
  padding: var(--padding-screen);
  margin-bottom: 41px;
  background-color: white;
  border-radius: var(--radius-normal);
  box-shadow: var(--shadow-normal);
  width: 600px;
  max-width: 100%;
  overflow: hidden;
}

.input-container {
  margin-bottom: 20px;
}

.label {
  width: 100%;
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
  font-family: "Roboto", sans-serif;
  font-size: var(--font-size-small);
  font-weight: var(--font-weight-normal);
  line-height: 1.5;
}

.select {
  display: block;
  margin-top: 5px;
  border: 1px solid var(--color-grey-80);
  border-radius: var(--radius-small);
  padding: 0 16px;
  height: 40px;
}

.button:before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.button {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 40px;
  padding: 0 20px;
  border-radius: var(--radius-normal);
  line-height: 1;
  font-size: var(--font-size-normal);
  font-weight: var(--font-weight-bold);
  text-decoration: none;
  overflow: hidden;
}

.button.__primary {
  background: var(--color-primary);
  color: white;
}
</style>
