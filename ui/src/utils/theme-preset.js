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
          root: {
            colorOne: "{primary.500}",
            colorTwo: "{primary.500}",
            colorThree: "{primary.500}",
            colorFour: "{primary.500}",
          },
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
          root: {
            colorOne: "{primary.500}",
            colorTwo: "{primary.500}",
            colorThree: "{primary.500}",
            colorFour: "{primary.500}",
          },
        },
      },
    },
  },
});

export const createAtlasPresetPortal = (primaryColor, primaryTextColor, secondaryTextColor) => {
  const portalShades = generateShades(primaryColor);

  return definePreset(Aura, {
    semantic: {
      primary: portalShades,
      red: appErrorShades,
      green: appSuccessShades,
    },
    components: {
      progressspinner: {
        colorScheme: {
          light: {
            root: {
              colorOne: "{primary.500}",
              colorTwo: "{primary.500}",
              colorThree: "{primary.500}",
              colorFour: "{primary.500}",
            },
          },
        },
      },
      accordion: {
        colorScheme: {
          light: {
            header: {
              color: "{atlas.text.primary}",
              hoverColor: "{atlas.text.primary}",
              activeColor: "{atlas.text.primary}",
              activeHoverColor: "{atlas.text.primary}",
            },
            content: {
              color: "{atlas.text.secondary}",
            },
          },
        },
      },
    },
    extend: {
      atlas: {
        text: {
          primary: primaryTextColor,
          secondary: secondaryTextColor,
        },
      },
    },

    css: ({ dt }) => `
      html, body {
        color: ${dt("atlas.text.secondary")};
      }

      h1,h2,h3,h4,h5,h6 {
        color: ${dt("atlas.text.primary")};
      }

      p, span, label, small, div {
        color: inherit;
      }

      .p-component {
        color: ${dt("atlas.text.secondary")};
      }

      .p-dialog-title,
      .p-drawer-title,
      .p-card-title,
      .p-panel-title {
        color: ${dt("atlas.text.primary")};
      }

      .p-card-subtitle {
        color: ${dt("atlas.text.secondary")};
      }

      .p-datatable thead th {
        color: ${dt("atlas.text.primary")};
      }
      .p-datatable tbody td {
        color: ${dt("atlas.text.secondary")};
      }

      .p-drawer .p-drawer-content {
        color: ${dt("atlas.text.secondary")};
      }

      .p-drawer .p-drawer-content .header {
        color: ${dt("atlas.text.primary")};
      }
    `,
  });
};
