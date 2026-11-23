import { describe, expect, it } from "vitest";
import { getRelationLinks } from "@/admin/utils/relation-links";

describe("getRelationLinks", () => {
  it("uses the selected option label for a single relation", () => {
    expect(getRelationLinks(4, [{ id: 4, label: "Basisregistratie" }])).toEqual([
      { id: 4, label: "Basisregistratie" },
    ]);
  });

  it("uses only the selected side of a picklist", () => {
    expect(
      getRelationLinks([
        [{ id: 1, name: "Niet geselecteerd" }],
        [{ id: 2, name: "Redactie" }],
      ]),
    ).toEqual([{ id: 2, label: "Redactie" }]);
  });

  it("deduplicates multi-value relations", () => {
    expect(
      getRelationLinks(
        [1, "1", 2],
        [
          { id: 1, label: "Kaart A" },
          { id: 2, label: "Kaart B" },
        ],
      ),
    ).toEqual([
      { id: 1, label: "Kaart A" },
      { id: 2, label: "Kaart B" },
    ]);
  });
});
