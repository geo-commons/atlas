/**
 * Capitalizes the first letter of a given string.
 *
 * This function takes a string input and returns a new string
 * with the first letter converted to uppercase. If the input is
 * not a string or is an empty string, the function returns the input as is.
 *
 * @param {string} string - The input string to be capitalized.
 * @returns {string} - The capitalized string, or the original input if it is not a string or is empty.
 */
export function capitalizeFirstLetter(string) {
  if (typeof string !== "string" || !string) return string; // Check for non-strings and empty strings
  return string.charAt(0).toUpperCase() + string.slice(1);
}

/**
 * Formats a raw input string by replacing underscores with spaces,
 * trimming leading and trailing whitespace, and capitalizing the first letter.
 *
 * This function is designed to take a raw string input, typically from
 * a database or user input, and clean it up for better readability
 * and presentation. The function performs the following transformations:
 * - Replaces all underscores (_) with spaces.
 * - Trims leading and trailing whitespace.
 * - Capitalizes the first letter of the resulting string.
 *
 * @param {string} string - The raw input string to be formatted.
 * @returns {string} - The cleaned and formatted string. If the input is not a string or is empty, it returns the input as is.
 */
export function formatRawString(string) {
  if (typeof string !== "string" || !string) return string; // Check for non-strings and empty strings

  return capitalizeFirstLetter(string.replace(/_/g, " ").trim());
}
