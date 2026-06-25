/* AUTO-GENERATED FILE — do not edit, rather run pnpm install to get the most recent version of the types.
 * Source: 2025-09-17T10:27:52.829Z
 * From: UpdateMethodType at build-time
 */
import { Option } from "./Option";

// UpdateMethodType
export type UpdateMethodTypeId = "manual" | "automatic" | "automatic_script" | "manual_script";

export const updateMethodTypeOptions: Option<UpdateMethodTypeId>[] = [
  { id: "manual", label: "Manueel" },
  { id: "automatic", label: "Automatisch (API)" },
  { id: "automatic_script", label: "Automatisch (script)" },
  { id: "manual_script", label: "Manueel (script)" },
];

export const updateMethodTypeLabels: Record<UpdateMethodTypeId, string> = {
  manual: "Manueel",
  automatic: "Automatisch (API)",
  automatic_script: "Automatisch (script)",
  manual_script: "Manueel (script)",
};
