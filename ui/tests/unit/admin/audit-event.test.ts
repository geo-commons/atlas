import { getAuditActionIndicator } from "@/admin/utils/audit-event";
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
