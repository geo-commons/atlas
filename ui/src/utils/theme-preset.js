import { definePreset } from "@primevue/themes";
import Aura from "@primevue/themes/aura";
import { generateShades } from "@/utils/generate-shades";

const getCSSVariable = (variable) => getComputedStyle(document.documentElement).getPropertyValue(variable).trim();

const appPrimaryColor = getCSSVariable("--color-primary");
const adminPrimaryColor = getCSSVariable("--color-admin-primary");
const appErrorColor = getCSSVariable("--color-alert");
const appSuccessColor = getCSSVariable("--color-succesful");

const appShades = generateShades(appPrimaryColor);
const adminShades = generateShades(adminPrimaryColor);
const appErrorShades = generateShades(appErrorColor);
const appSuccessShades = generateShades(appSuccessColor);

export const AtlasPresetApp = definePreset(Aura, {
  semantic: {
    primary: appShades,
    red: appErrorShades,
    green: appSuccessShades,
  },
  components: {
    progressspinner: {
      colorScheme: {
        light: {
          colorOne: "{primary.500}",
          colorTwo: "{primary.500}",
          colorThree: "{primary.500}",
          colorFour: "{primary.500}",
        },
      },
    },
  },
});

// Admin preset
export const AtlasPresetAdmin = definePreset(Aura, {
  semantic: {
    primary: adminShades,
    red: appErrorShades,
    green: appSuccessShades,
  },
  components: {
    progressspinner: {
      colorScheme: {
        light: {
          colorOne: "{primary.500}",
          colorTwo: "{primary.500}",
          colorThree: "{primary.500}",
          colorFour: "{primary.500}",
        },
      },
    },
  },
});
