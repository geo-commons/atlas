import { getAuditActionIndicator, getAuditDetails, getAuditValueDisplay } from "@/admin/utils/audit-event";
import { describe, expect, it } from "vitest";

describe("getAuditActionIndicator", () => {
  it.each([
    ["+", "Toegevoegd", "success"],
    ["-", "Verwijderd", "danger"],
    ["~", "Gewijzigd", "info"],
  ] as const)("returns the correct indicator for %s", (actionId, label, severity) => {
    expect(getAuditActionIndicator(actionId)).toMatchObject({ label, severity });
  });
});

describe("getAuditDetails", () => {
  it("splits grouped changes into clear change cards", () => {
    expect(getAuditDetails("Naam\nPlaatsen → Plaatse\n\nGerelateerde tabel gewijzigd\nDSO\nVolgorde\n0 → 1")).toEqual([
      { field: "Naam", oldValue: "Plaatsen", newValue: "Plaatse" },
      { context: "Gerelateerde tabel · DSO", field: "Volgorde", oldValue: "0", newValue: "1" },
    ]);
  });

  it("keeps simple audit details readable", () => {
    expect(getAuditDetails("Nieuw object")).toEqual([{ value: "Nieuw object" }]);
  });

  it("splits multiple fields from one related object", () => {
    expect(getAuditDetails("Kaartlaag gewijzigd\nRoad works\nCategorie\nOld → New\nPositie\n0 → 1")).toEqual([
      { context: "Kaartlaag · Road works", field: "Categorie", oldValue: "Old", newValue: "New" },
      { context: "Kaartlaag · Road works", field: "Positie", oldValue: "0", newValue: "1" },
    ]);
  });
});

describe("getAuditValueDisplay", () => {
  it("formats JSON and Python-style JSON values", () => {
    expect(getAuditValueDisplay('{"layer": 292}')).toEqual({ isJson: true, value: '{\n  "layer": 292\n}' });
    expect(getAuditValueDisplay("[{'layer': 292, 'atlasgroup': 1}]")).toEqual({
      isJson: true,
      value: '[\n  {\n    "layer": 292,\n    "atlasgroup": 1\n  }\n]',
    });
  });

  it("keeps normal text unchanged", () => {
    expect(getAuditValueDisplay("Plaatsen")).toEqual({ isJson: false, value: "Plaatsen" });
  });
});
