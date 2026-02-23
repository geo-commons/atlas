import Cookies from "js-cookie";
import { App } from "vue";

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

export enum ApiMethod {
  POST = "POST",
  GET = "GET",
  PUT = "PUT",
  DELETE = "DELETE",
}

class ApiError extends Error {
  constructor(
    message: string,
    public statusCode: number,
    public httpMethod: ApiMethod,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

/**
 * Wrapper around `window.fetch` that adds headers including the CSRF token
 * @param resource - The URL or a RequestInfo object
 * @param method - The HTTP method; defaults to ApiMethod.GET
 * @param data - Data that will be serialized as JSON. If present, the content type header will be set
 * @param options - Any additional options that `fetch` accepts
 */
export async function apiFetch(
  resource: RequestInfo | URL,
  method: ApiMethod = ApiMethod.GET,
  data: object | null = null,
  options: RequestInit = {},
) {
  const headers = new Headers(options.headers);

  // Add content-type header if request has a body
  if (data && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }

  const body = data !== null ? JSON.stringify(data) : options.body;

  // Add CSRF token from cookie
  const token = Cookies.get("csrftoken");
  if (!headers.has("X-CSRFToken") && token) {
    headers.set("X-CSRFToken", token);
  }

  // Add same-origin credentials
  const credentials = options.credentials || "same-origin";

  const newOptions = { ...options, body, headers, credentials, method };
  const response = await fetch(resource, newOptions);
  if (!response.ok) {
    throw new ApiError(response.statusText, response.status, method);
  }

  return response;
}

/**
 * Show an error toast for ApiError. This function will be called by the Pinia Colada hook that handles the error.
 * @param app
 * @param error
 */
export function showApiFetchError(app: App, error: ApiError) {
  let introduction: string;
  let message: string;
  if (error.httpMethod === ApiMethod.GET) {
    introduction = "Opvragen gegevens mislukt: ";
  } else {
    introduction = "Operatie mislukt: ";
  }
  switch (error.statusCode) {
    case 500:
      message = "interne serverfout.";
      break;
    case 401:
    case 403:
      message = "ongeautoriseerd voor operatie. Controleer of u nog bent ingelogd door de pagina te vernieuwen.";
      break;
    default:
      message = error.message;
  }
  app.config.globalProperties.$toast.add({
    severity: "error",
    summary: "Fout",
    detail: introduction + message,
    life: 5000,
  });
}
