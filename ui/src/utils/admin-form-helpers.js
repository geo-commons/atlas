/**
 * Update a multi-line field in an object by splitting the value by newline characters and filtering out empty lines.
 * @param {Object} object - The object containing the field to be updated.
 * @param {string} field - The field in the object to be updated.
 * @param {string} value - The new value for the multi-line field.
 */
export function updateMultiLineField(object, field, value) {
  if (!object || !field) {
    console.error(`Either object: ${object} or field: ${field} is not defined`);
    return;
  }

  object[field] = value
    .split("\n")
    .filter((value) => value.trim() !== "")
    .map((value) => value.trim());
}
