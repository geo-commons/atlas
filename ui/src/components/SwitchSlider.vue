<template>
  <label class="switch">
    <input type="checkbox" @change="() => $emit('toggleSwitch')" />
    <span class="slider round"></span>
  </label>
</template>

<script>
export default {
  name: "SwitchSliderComponent",
  props: {},
  data() {
    return {
      checked: true,
    };
  },
  computed: {},
  mounted() {},
  methods: {},
};
</script>

<style scoped>
.switch {
  position: relative;
  display: inline-block;
  color: var(--color-grey-50);
  width: calc(2 * var(--slider-diameter) + var(--slider-padding));
  height: calc(var(--slider-diameter) + 2 * var(--slider-padding));
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: var(--color-grey-60);
  transition: var(--slider-transition);
}

.slider:before {
  position: absolute;
  content: "";
  height: var(--slider-diameter);
  width: var(--slider-diameter);
  left: var(--slider-padding);
  bottom: var(--slider-padding);
  background-color: var(--color-white);
  transition: var(--slider-transition);
}

input:checked + .slider {
  background-color: var(--color-primary);
}

html.keyboard-user input:focus + .slider {
  box-shadow: 0 0 1px var(--color-primary);
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

input:checked + .slider:before {
  transform: translateX(calc(var(--slider-diameter) - var(--slider-padding)));
}

/* Rounded sliders */
.slider.round {
  border-radius: calc(var(--slider-diameter) + 2 * var(--slider-padding));
}

.slider.round:before {
  border-radius: 50%;
}
</style>
