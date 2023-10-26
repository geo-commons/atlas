/**
 * Debounces a function execution by canceling and scheduling it after a specified delay.
 *
 * This function is used to prevent a function from being executed multiple times in quick succession.
 * It cancels a previously scheduled execution (if any) and schedules the function to be called after
 * a specified delay (in milliseconds).
 *
 * @param {Function} callback - The function to be debounced.
 * @param {number} timeout - The identifier of the previous timeout to be cleared.
 * @param {number} ms - The delay in milliseconds before the function is executed.
 * @returns {number} An identifier for the newly scheduled timeout.
 */
export function debounce(callback, timeout, ms) {
  if (timeout) clearTimeout(timeout);
  return setTimeout(callback, ms);
}
