export const normalizeUrlValue = (value: unknown): string => {
  if (typeof value !== "string") {
    return "";
  }

  return value.replaceAll(" ", "%20");
};
