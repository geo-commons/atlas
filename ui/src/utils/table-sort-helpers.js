/**
 * The sortAlphabetically function is a utility function for sorting two items a and b alphabetically in either
 * ascending or descending order.
 * @param a The first item to compare
 * @param b The second item to compare
 * @param ascending (boolean) for determining the sorting order
 * @returns {number|number} a numeric value that determines the relative order of a and b
 */
export function sortAlphabetically(a, b, ascending) {
  // equal items sort equally
  if (a === b) {
    return 0;
  }

  // nulls and empty strings sort after anything else
  if (a === null || a === "") {
    return 1;
  }
  if (b === null || b === "") {
    return -1;
  }

  // otherwise, if we're ascending, lowest sorts first
  if (ascending) {
    return a < b ? -1 : 1;
  }

  // if descending, highest sorts first
  return a < b ? 1 : -1;
}
