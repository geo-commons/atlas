/**
 * Modifies the given URL to include a `page_size` query parameter, which controls
 * the number of objects to be retrieved in an API call. If the `page_size` parameter
 * already exists in the URL, it will be overridden with the provided or default value.
 *
 * @param {string} url - The API endpoint URL to which the `page_size` will be appended or modified.
 * @param {number} [maxPageSize=10000] - The maximum number of objects to retrieve. Defaults to 10000 if not specified.
 *
 * @returns {string} - The modified URL containing the updated `page_size` query parameter.
 */
export function getAllObjects(url: string, maxPageSize: number = 10000): string {
  // Parse the input URL into a URL object
  // const allObjectsUrl = new URL(url);

  // Extract the current query parameters from the URL
  const params = new URLSearchParams();

  // Set or override the 'page_size' parameter with the provided or default value
  params.set("page_size", maxPageSize.toString());

  // Return the updated URL as a string
  return `${url}?${params.toString()}`;
}
