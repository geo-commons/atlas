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

/**
 * Resolves the logical property key from a dot/bracket notation path.
 *
 * Rules:
 * - If the path ends with an array index (e.g. "items[0]"),
 *   the array name is returned ("items").
 * - If the path ends with a property (e.g. "items[0].type"),
 *   the property name is returned ("type").
 *
 * This function does not inspect the target object; it operates
 * purely on the path string.
 *
 @param {string} path - The raw path string to be formatted.
 */
export function getResolvedKey(path) {
  // Match ending like [0], [12], etc.
  const arrayEndMatch = path.match(/^(.*)\[\d+\]$/);

  if (arrayEndMatch) {
    // Path ends with an array index → return the array key
    return arrayEndMatch[1].split(".").pop();
  }

  // Normal property path
  return path.split(".").pop();
}
