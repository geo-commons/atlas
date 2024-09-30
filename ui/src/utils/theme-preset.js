import { definePreset } from "@primevue/themes";
import Aura from "@primevue/themes/aura";

export const AtlasPreset = definePreset(Aura, {
  semantic: {
    primary: {
      50: "#EDF8FF",
      100: "#D6EFFF",
      200: "#B5E4FF",
      300: "#83D5FF",
      400: "#48BCFF",
      500: "#1E9AFF",
      600: "#067AFF",
      700: "#0066FF",
      800: "#084EC5",
      900: "#0D469B",
      950: "#0E2B5D",
    },
  },
  components: {
    button: {
      colorScheme: {
        light: {
          primary: {
            background: "{blue.600}",
            border: {
              color: "{blue.600}",
            },
            hover: {
              background: "{blue.700}",
              border: {
                color: "{blue.700}",
              },
            },
          },
          outlined: {
            primary: {
              color: "{blue.600}",
              border: {
                color: "{blue.600}",
              },
              hover: {
                background: "{blue.50}",
              },
            },
          },
        },
      },
    },
    progressspinner: {
      colorScheme: {
        light: {
          color: {
            1: "{blue.600}",
            2: "{blue.600}",
            3: "{blue.600}",
            4: "{blue.600}",
          },
        },
      },
    },
  },
});
