import chroma from "chroma-js";

/**
 * Generates a range of color shades from a given base color.
 *
 * This function uses the Chroma.js library to create a scale of lighter
 * and darker shades based on the provided base color. The shades follow
 * a pattern similar to Tailwind CSS and PrimeVue's styled theming system,
 * where lower values (e.g., 50, 100) are lighter and higher values
 * (e.g., 900, 950) are darker.
 *
 * @param {string} baseColor - The base color in hex format.
 * @returns {Object} An object containing shades from 50 to 950.
 *
 * Reference: https://primevue.org/theming/styled/
 */
export const generateShades = (baseColor: string) => {
  return {
    50: chroma(baseColor).brighten(3).hex(),
    100: chroma(baseColor).brighten(2.5).hex(),
    200: chroma(baseColor).brighten(2).hex(),
    300: chroma(baseColor).brighten(1.5).hex(),
    400: chroma(baseColor).brighten(1).hex(),
    500: baseColor,
    600: chroma(baseColor).darken(0.5).hex(),
    700: chroma(baseColor).darken(1).hex(),
    800: chroma(baseColor).darken(1.5).hex(),
    900: chroma(baseColor).darken(2).hex(),
    950: chroma(baseColor).darken(3).hex(),
  };
};
