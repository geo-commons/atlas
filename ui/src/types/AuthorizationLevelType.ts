/* AUTO-GENERATED FILE — do not edit, rather run npm install to get the most recent version of the types.
 * Source: 2025-09-17T10:27:52.831Z
 * From: AuthorizationLevelType at build-time
 */
import { Option } from "./Option";

// AuthorizationLevelType
export type AuthorizationLevelTypeId = "open_data" | "internal" | "protected";

export const authorizationLevelTypeOptions: Option<AuthorizationLevelTypeId>[] = [
  { id: "open_data", label: "Open" },
  { id: "internal", label: "Intern" },
  { id: "protected", label: "Extra autorisatie" },
];

export const authorizationLevelTypeLabels: Record<AuthorizationLevelTypeId, string> = {
  open_data: "Open",
  internal: "Intern",
  protected: "Extra autorisatie",
};
