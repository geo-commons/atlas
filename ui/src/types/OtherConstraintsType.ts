/* AUTO-GENERATED FILE — do not edit, rather run npm install to get the most recent version of the types.
   * Source: 2025-09-17T10:27:52.843Z
   * From: OtherConstraintsType at build-time
   */
import { Option } from "./Option";

// OtherConstraintsType
export type OtherConstraintsTypeId = "publicdomain-mark" | "publicdomain-zero" | "licenses-by" | "licenses-by-sa" | "licenses-by-nc" | "licenses-by-nc-sa" | "licenses-by-nd" | "licenses-by-nc-nd" | "custom";

export const otherConstraintsTypeOptions: Option<OtherConstraintsTypeId>[] = [
  { id: "publicdomain-mark", label: "Open data (publiek)" },
  { id: "publicdomain-zero", label: "Open data (CC0)" },
  { id: "licenses-by", label: "Open data (CC-BY)" },
  { id: "licenses-by-sa", label: "Open data (CC-BY-SA)" },
  { id: "licenses-by-nc", label: "Open data (CC-BY-NC)" },
  { id: "licenses-by-nc-sa", label: "Gebruiksvoorwaarden (CC-by-nc-sa)" },
  { id: "licenses-by-nd", label: "Gebruiksvoorwaarden (CC-by-nd)" },
  { id: "licenses-by-nc-nd", label: "Gebruiksvoorwaarden (CC-by-nc-nd)" },
  { id: "custom", label: "Gebruiksvoorwaarden Geogedeeld" }
];

export const otherConstraintsTypeLabels: Record<OtherConstraintsTypeId, string> = {
  "publicdomain-mark": "Open data (publiek)",
  "publicdomain-zero": "Open data (CC0)",
  "licenses-by": "Open data (CC-BY)",
  "licenses-by-sa": "Open data (CC-BY-SA)",
  "licenses-by-nc": "Open data (CC-BY-NC)",
  "licenses-by-nc-sa": "Gebruiksvoorwaarden (CC-by-nc-sa)",
  "licenses-by-nd": "Gebruiksvoorwaarden (CC-by-nd)",
  "licenses-by-nc-nd": "Gebruiksvoorwaarden (CC-by-nc-nd)",
  "custom": "Gebruiksvoorwaarden Geogedeeld"
};
