/* AUTO-GENERATED FILE — do not edit, rather run npm install to get the most recent version of the types.
 * Source: 2025-09-17T10:27:52.835Z
 * From: StatusType at build-time
 */
import { Option } from "./Option";

// StatusType
export type StatusTypeId = "completed" | "underDevelopment" | "historicalArchive";

export const statusTypeOptions: Option<StatusTypeId>[] = [
  { id: "completed", label: "Gepubliceerd" },
  { id: "underDevelopment", label: "In ontwikkeling" },
  { id: "historicalArchive", label: "Gearchiveerd" },
];

export const statusTypeLabels: Record<StatusTypeId, string> = {
  completed: "Gepubliceerd",
  underDevelopment: "In ontwikkeling",
  historicalArchive: "Gearchiveerd",
};
