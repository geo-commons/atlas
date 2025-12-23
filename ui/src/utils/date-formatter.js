const defaultOptions = { year: "numeric", month: "numeric", day: "numeric", hour: "numeric", minute: "numeric" };

/**
 * Formats a given date string into a localized date and time string.
 *
 * This function takes a date string, creates a Date object, and formats it into a string
 * representing the date and time in the Dutch (Netherlands) locale. The formatting options
 * include the year, month, day, hour, and minute.
 *
 * Note: if dateString is null we return "-"
 *
 * @param {string} dateString - The date string to be formatted.
 * @param customOptions - optional options object for deviating formatting.
 * @returns {string} A formatted date and time string in the "nl-NL" locale.
 */
export function formatDateValue(dateString, customOptions = null) {
  if (!dateString) {
    return "-";
  }

  const date = new Date(dateString);
  const options = customOptions ? customOptions : defaultOptions;

  return date.toLocaleDateString("nl-NL", options);
}

/**
 * Returns a date string representing the current date with the specified delimiter.
 *
 * @param {string} delimiter - The delimiter used to separate date components in the date string. Default is "-".
 * @returns {string} The date string in the format "YYYY-MM-DD" with the specified delimiter.
 */
export function getDateString(delimiter = "_") {
  // Get the current date
  const currentDate = new Date();

  // Extract the year, month, and day components
  const year = currentDate.getFullYear();
  const month = String(currentDate.getMonth() + 1).padStart(2, "0"); // Month is zero-indexed, so we add 1
  const day = String(currentDate.getDate()).padStart(2, "0");

  // Construct the date string with the specified delimiter
  return `${year}${delimiter}${month}${delimiter}${day}`;
}

/**
 * Converts a date string or Date object to YYYY-MM-DD format for HTML date inputs.
 *
 * @param {string|Date|null|undefined} dateValue - The date value to format (ISO string, Date object, null, or undefined)
 * @returns {string} Date string in YYYY-MM-DD format, or empty string if input is null/undefined
 */
export function formatDateForInput(dateValue) {
  if (!dateValue) {
    return "";
  }

  // If it's already a string, try to parse it as Date
  // If it's a Date object, use it directly
  const date = dateValue instanceof Date ? dateValue : new Date(dateValue);

  // Check if the date is valid
  if (isNaN(date.getTime())) {
    return "";
  }

  // Use local date methods to avoid timezone conversion issues
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}
