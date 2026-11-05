import { getAuditActionIndicator, getAuditValueDisplay } from "@/admin/utils/audit-event";
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

describe("getAuditValueDisplay", () => {
  it("formats JSON and Python-style JSON values", () => {
    expect(getAuditValueDisplay('{"layer": 292}')).toEqual({ isJson: true, value: '{\n  "layer": 292\n}' });
    expect(getAuditValueDisplay("[{'layer': 292, 'atlasgroup': 1}]")).toEqual({
      isJson: true,
      value: '[\n  {\n    "layer": 292,\n    "atlasgroup": 1\n  }\n]',
    });
    expect(getAuditValueDisplay("{'gps': True, 'baselayer': False}")).toEqual({
      isJson: true,
      value: '{\n  "gps": true,\n  "baselayer": false\n}',
    });
  });

  it("keeps normal text unchanged", () => {
    expect(getAuditValueDisplay("Plaatsen")).toEqual({ isJson: false, value: "Plaatsen" });
  });
});
