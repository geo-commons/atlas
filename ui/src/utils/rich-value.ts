import nunjucks from "nunjucks";

export const normalizeUrlValue = (value: unknown): string => {
  if (typeof value !== "string") {
    return "";
  }

  return nunjucks.renderString("{{ value | replace(' ', '%20') }}", { value });
};
