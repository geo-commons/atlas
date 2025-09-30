/* AUTO-GENERATED FILE — do not edit, rather run npm install to get the most recent version of the types.
   * Source: 2025-09-17T10:27:52.839Z
   * From: AccessConstraintsType at build-time
   */
import { Option } from "./Option";

// AccessConstraintsType
export type AccessConstraintsTypeId = "license" | "intellectualPropertyRights" | "restricted" | "otherRestrictions";

export const accessConstraintsTypeOptions: Option<AccessConstraintsTypeId>[] = [
  {
    id: "license",
    label: "Licentie - Formele toestemming om iets te doen met de data.",
  },
  {
    id: "intellectualPropertyRights",
    label:
      "Intellectuele eigendomsrechten - Recht op een financieel voordeel van en controle hebben op de distributie een niet tastbaar eigendom wat het resultaat is van creativiteit.",
  },
  {
    id: "restricted",
    label: "Beperkt - Verbod op distributie en gebruik.",
  },
  {
    id: "otherRestrictions",
    label: "Overige beperkingen - Restrictie niet opgenomen in lijst.",
  }
];

export const accessConstraintsTypeLabels: Record<AccessConstraintsTypeId, string> = {
  "license": "Licentie",
  "intellectualPropertyRights": "Intellectuele eigendomsrechten",
  "restricted": "Beperkt",
  "otherRestrictions": "Overige beperkingen"
};
