// GeoServer always responds with an OK status, even when an error occurs.
// This function is designed to determine whether a GeoServer WFS-Transaction
// request succeeded or failed. If an error occurred, it returns the specific GeoServer error;
// otherwise, it returns "success" as true.
const parseGeoServerWfsTResponse = async (response: Response): Promise<{ errorMessage: string; success: boolean }> => {
  let errorMessage: string = "";
  let success: boolean = false;

  if (response.ok) {
    const responseText = await response.text();

    // If the response body contains an <ows:ExceptionReport> tag, it indicates that GeoServer responded with an error.
    if (responseText.includes("<ows:ExceptionReport")) {
      errorMessage = parseGeoServerError(responseText);
    } else {
      success = true;
    }
  } else {
    errorMessage = "Request naar GeoServer is mislukt met status: " + response.status;
  }

  return { errorMessage, success };
};

const parseGeoServerError = (geoServerError: string): string => {
  const parser = new DOMParser();
  const xmlDoc = parser.parseFromString(geoServerError, "text/xml");
  // The error details in a GeoServer response are always provided within the <ExceptionText> element.
  const exceptionText = xmlDoc.querySelector("ExceptionText");
  return exceptionText ? (exceptionText.textContent as string) : "Onbekende fout opgetreden";
};

export { parseGeoServerWfsTResponse };
