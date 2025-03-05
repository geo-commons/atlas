import { definePreset } from "@primevue/themes";
import Aura from "@primevue/themes/aura";

export const AtlasPresetApp = definePreset(Aura, {
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
            background: "{primary.700}",
            border: {
              color: "{primary.700}",
            },
            hover: {
              background: "{primary.800}",
              border: {
                color: "{primary.800}",
              },
            },
          },
          outlined: {
            primary: {
              color: "{primary.700}",
              border: {
                color: "{primary.700}",
              },
              hover: {
                background: "{primary.50}",
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
            1: "{primary.700}",
            2: "{primary.700}",
            3: "{primary.700}",
            4: "{primary.700}",
          },
        },
      },
    },
  },
});

// Admin preset
export const AtlasPresetAdmin = definePreset(Aura, {
  semantic: {
    primary: {
      50: "#ecf2ff",
      100: "#dde6ff",
      200: "#c2d1ff",
      300: "#9cb1ff",
      400: "#7586ff",
      500: "#424bff",
      600: "#3c36f5",
      700: "#322ad8",
      800: "#2925ae",
      900: "#262689",
      950: "#181650",
    },
  },
  components: {
    button: {
      colorScheme: {
        light: {
          primary: {
            background: "{primary.500}",
            border: {
              color: "{primary.500}",
            },
            hover: {
              background: "{primary.600}",
              border: {
                color: "{primary.600}",
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
            1: "{primary.500}",
            2: "{primary.500}",
            3: "{primary.500}",
            4: "{primary.500}",
          },
        },
      },
    },
  },
});
