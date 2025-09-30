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
    50: chroma.mix(baseColor, "#ffffff", 0.9).hex(),
    100: chroma.mix(baseColor, "#ffffff", 0.75).hex(),
    200: chroma.mix(baseColor, "#ffffff", 0.6).hex(),
    300: chroma.mix(baseColor, "#ffffff", 0.45).hex(),
    400: chroma.mix(baseColor, "#ffffff", 0.3).hex(),
    500: baseColor,
    600: chroma.mix(baseColor, "#000000", 0.2).hex(),
    700: chroma.mix(baseColor, "#000000", 0.35).hex(),
    800: chroma.mix(baseColor, "#000000", 0.5).hex(),
    900: chroma.mix(baseColor, "#000000", 0.7).hex(),
  };
};
