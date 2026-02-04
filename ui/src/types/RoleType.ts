/* AUTO-GENERATED FILE — do not edit, rather run npm install to get the most recent version of the types.
 * Source: 2025-09-17T10:27:52.827Z
 * From: RoleType at build-time
 */
import { Option } from "./Option";

// RoleType
export type RoleTypeId =
  | "resourceProvider"
  | "custodian"
  | "owner"
  | "user"
  | "distributor"
  | "originator"
  | "pointOfContact"
  | "principalInvestigator"
  | "processor"
  | "publisher"
  | "author";

export const roleTypeOptions: Option<RoleTypeId>[] = [
  { id: "resourceProvider", label: "Data verstrekker" },
  { id: "custodian", label: "Beheerder" },
  { id: "owner", label: "Eigenaar" },
  { id: "user", label: "Gebruiker" },
  { id: "distributor", label: "Distributeur" },
  { id: "originator", label: "Maker" },
  { id: "pointOfContact", label: "Contactpunt" },
  { id: "principalInvestigator", label: "Onderzoeksleider" },
  { id: "processor", label: "Bewerker" },
  { id: "publisher", label: "Uitgever" },
  { id: "author", label: "Auteur" },
];

export const roleTypeLabels: Record<RoleTypeId, string> = {
  resourceProvider: "Data verstrekker",
  custodian: "Beheerder",
  owner: "Eigenaar",
  user: "Gebruiker",
  distributor: "Distributeur",
  originator: "Maker",
  pointOfContact: "Contactpunt",
  principalInvestigator: "Onderzoeksleider",
  processor: "Bewerker",
  publisher: "Uitgever",
  author: "Auteur",
};
