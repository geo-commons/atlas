import { definePreset } from "@primevue/themes";
import Aura from "@primevue/themes/aura";
import { generateShades } from "@/utils/generate-shades";

const getCSSVariable = (variable) => getComputedStyle(document.documentElement).getPropertyValue(variable).trim();

const appPrimaryColor = getCSSVariable("--color-primary");
const appErrorColor = getCSSVariable("--color-alert");
const appSuccessColor = getCSSVariable("--color-succesful");

export const AtlasPreset = (
  primaryColor = appPrimaryColor,
  primaryTextColor = "black",
  secondaryTextColor = "black",
) => {
  return definePreset(Aura, {
    semantic: {
      primary: generateShades(primaryColor),
      red: generateShades(appErrorColor),
      green: generateShades(appSuccessColor),
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
