import { describe, expect, it } from "vitest";
import { renderTemplate } from "@/utils/template-renderer";

describe("renderTemplate", () => {
  it("renders plain and nested values without evaluating JavaScript", () => {
    expect(renderTemplate("{{ city.name }}: {{ postcode }}", { city: { name: "Amsterdam" }, postcode: "1011AB" })).toBe(
      "Amsterdam: 1011AB",
    );
  });

  it("supports replace and replaceAll method calls", () => {
    expect(renderTemplate("{{ value.replace(' ', '-') }}", { value: "a value value" })).toBe("a-value value");
    expect(renderTemplate("{{ postcode.replaceAll(' ', '') }}", { postcode: "AB 12 CD" })).toBe("AB12CD");
  });

  it("supports the configured string filters", () => {
    expect(renderTemplate("{{ postcode.replaceAll(' ', '') | lower }}", { postcode: "AB 12 CD" })).toBe("ab12cd");
    expect(renderTemplate("{{ value | replace(' ', '%20') }}", { value: "a value" })).toBe("a%20value");
  });

  it("supports lowercase, uppercase, and trim filters", () => {
    const context = { value: "  Atlas CSP  " };

    expect(renderTemplate("{{ value | lower }}", context)).toBe("  atlas csp  ");
    expect(renderTemplate("{{ value | upper }}", context)).toBe("  ATLAS CSP  ");
    expect(renderTemplate("{{ value | trim }}", context)).toBe("Atlas CSP");
  });

  it("renders missing and unsupported expressions as empty strings", () => {
    expect(renderTemplate("before {{ missing.value }} after", {})).toBe("before  after");
    expect(renderTemplate("{{ globalThis.alert('x') }}", {})).toBe("");
  });
});
