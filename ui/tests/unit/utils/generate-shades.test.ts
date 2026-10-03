import { describe, expect, it } from "vitest";

import { generateShades } from "@/utils/generate-shades";

describe("generateShades", () => {
  it.each(["", "!NOT_A_VALID_COLOR!"])("uses the default color for invalid input %j", (color) => {
    expect(generateShades(color)).toEqual(generateShades("#000000"));
  });

  it("preserves a valid base color", () => {
    expect(generateShades("#12aBcD")[500]).toBe("#12aBcD");
  });
});
