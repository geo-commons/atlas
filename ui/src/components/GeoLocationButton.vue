<template>
  <div class="wrapper">
    <button
      v-tippy="{ placement: 'left' }"
      class="iconbutton"
      content="Toon GPS locatie"
      aria-label="Toon GPS locatie"
      @click="retrieveLocation"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        height="17px"
        viewBox="0 0 24 24"
        width="17px"
        fill="currentColor"
        :class="{ blink: isLoading }"
      >
        <path d="M0 0h24v24H0V0z" fill="none" />
        <path
          d="M12 8c-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4-1.79-4-4-4zm8.94 3c-.46-4.17-3.77-7.48-7.94-7.94V1h-2v2.06C6.83 3.52 3.52 6.83 3.06 11H1v2h2.06c.46 4.17 3.77 7.48 7.94 7.94V23h2v-2.06c4.17-.46 7.48-3.77 7.94-7.94H23v-2h-2.06zM12 19c-3.87 0-7-3.13-7-7s3.13-7 7-7 7 3.13 7 7-3.13 7-7 7z"
        />
      </svg>
    </button>
  </div>
</template>

<script>
import { getDefinitions } from "../utils/projections";
import { register } from "ol/proj/proj4";
import { transform } from "ol/proj";

// Register EPSG:28992 projection
register(getDefinitions());

export default {
  name: "GeoLocationButton",
  props: {
    position: Object,
  },
  data() {
    return {
      isLoading: false,
    };
  },
  methods: {
    retrieveLocation(e) {
      e.preventDefault();

      const options = {
        enableHighAccuracy: true,
        timeout: 5000,
        maximumAge: 0,
      };

      const onSuccess = (position) => {
        const convertedPosition = transform(
          [position.coords.longitude, position.coords.latitude],
          "EPSG:4326",
          "EPSG:28992"
        );

        this.$emit("set-position", {
          ...this.position,
          center: convertedPosition,
          geolocation: convertedPosition,
          zoom: 19,
        });

        this.isLoading = false;
      };

      const onError = () => {
        this.$store.commit(
          "setAlert",
          "Er is een fout opgetreden tijdens het ophalen van de geolocatie. Controleer de permissies en probeer het opnieuw."
        );
        this.isLoading = false;
      };

      if (navigator.geolocation) {
        this.isLoading = true;
        navigator.geolocation.getCurrentPosition(onSuccess, onError, options);
      } else {
        this.$store.commit(
          "setAlert",
          "Geolocatie wordt niet ondersteund door de browser."
        );
      }
    },
  },
};
</script>

<style scoped>
.wrapper {
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: var(--radius-normal);
  overflow: hidden;
  box-shadow: var(--shadow-normal);
}

.iconbutton {
  width: var(--width-button-normal);
  height: var(--width-button-normal);
}

.blink {
  color: var(--color-primary);
  animation: blinker 1s ease infinite;
}

@keyframes blinker {
  50% {
    opacity: 0;
  }
}
</style>
