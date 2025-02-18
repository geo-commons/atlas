const parseGeoServerWfsTResponse = async (response: Response): Promise<{ errorMessage: string; success: boolean }> => {
  let errorMessage: string = "";
  let success: boolean = false;

  if (response.ok) {
    const responseText = await response.text();

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
  const exceptionText = xmlDoc.querySelector("ExceptionText");
  return exceptionText ? (exceptionText.textContent as string) : "Onbekende fout opgetreden";
};

export { parseGeoServerWfsTResponse };
