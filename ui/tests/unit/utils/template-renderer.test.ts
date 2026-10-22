import { describe, expect, it } from "vitest";
import { renderJsonTemplate, renderTemplate } from "@/utils/template-renderer";

describe("renderTemplate", () => {
  it("renders plain and nested values without evaluating JavaScript", () => {
    expect(renderTemplate("{{ city.name }}: {{ postcode }}", { city: { name: "Amsterdam" }, postcode: "1011AB" })).toBe(
      "Amsterdam: 1011AB",
    );
  });

  it("supports replace and replaceAll pipes", () => {
    expect(renderTemplate("{{ value | replace(' ', '-') }}", { value: "a value value" })).toBe("a-value value");
    expect(renderTemplate("{{ postcode | replaceAll(' ', '') }}", { postcode: "AB 12 CD" })).toBe("AB12CD");
  });

  it("preserves quoted commas, parentheses, pipes, and escaped quotes in pipes", () => {
    expect(renderTemplate("{{ value | replaceAll(',', '|') }}", { value: "a,b" })).toBe("a|b");
    expect(renderTemplate("{{ value | replaceAll('(b)', 'c,d|e') }}", { value: "a(b)" })).toBe("ac,d|e");
    expect(renderTemplate("{{ value | replaceAll('|', '(x,y)') }}", { value: "a|b" })).toBe("a(x,y)b");
    expect(renderTemplate("{{ value | replaceAll('it\\'s', 'done') }}", { value: "it's ready" })).toBe("done ready");
  });

  it("renders missing and unsupported expressions as empty strings", () => {
    expect(renderTemplate("before {{ missing.value }} after", {})).toBe("before  after");
    expect(renderTemplate("{{ globalThis.alert('x') }}", {})).toBe("");
    expect(renderTemplate("{{ value.replaceAll(' ', '') }}", { value: "AB 12" })).toBe("");
  });

  it("serializes rendered JSON request bodies", () => {
    const body = renderJsonTemplate('{"name":"{{ name }}","message":"Hello {{ name }}"}', {
      name: 'A "quoted" name',
    });

    expect(JSON.parse(body)).toEqual({
      name: 'A "quoted" name',
      message: 'Hello A "quoted" name',
    });
  });
});
