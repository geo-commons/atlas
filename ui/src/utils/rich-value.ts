import { renderTemplate } from "@/utils/template-renderer";

export const normalizeUrlValue = (value: unknown): string => {
  if (typeof value !== "string") {
    return "";
  }

  return renderTemplate("{{ value | replace(' ', '%20') }}", { value });
};
