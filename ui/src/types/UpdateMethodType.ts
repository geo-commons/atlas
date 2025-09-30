/* AUTO-GENERATED FILE — do not edit, rather run npm install to get the most recent version of the types.
   * Source: 2025-09-17T10:27:52.829Z
   * From: UpdateMethodType at build-time
   */
import { Option } from "./Option";

// UpdateMethodType
export type UpdateMethodTypeId = "manual" | "automatic";

export const updateMethodTypeOptions: Option<UpdateMethodTypeId>[] = [
  { id: "manual", label: "Manueel" },
  { id: "automatic", label: "Automatisch (via API)" }
];

export const updateMethodTypeLabels: Record<UpdateMethodTypeId, string> = {
  "manual": "Manueel",
  "automatic": "Automatisch (via API)"
};
