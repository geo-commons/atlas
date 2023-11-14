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
