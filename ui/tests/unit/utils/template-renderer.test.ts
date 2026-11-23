import { describe, expect, it } from "vitest";
import { renderCqlTemplate, renderHtmlTemplate, renderJsonTemplate, renderTemplate } from "@/utils/template-renderer";

describe("Liquid templates", () => {
  it("renders nested values and built-in filters", () => {
    expect(
      renderTemplate("{{ city.name }}: {{ postcode | replace: ' ', '' }}", {
        city: { name: "Amsterdam" },
        postcode: "AB 12 CD",
      }),
    ).toBe("Amsterdam: AB12CD");
    expect(renderTemplate("{{ name | upcase }}", { name: "Atlas" })).toBe("ATLAS");
    expect(renderTemplate("before {{ missing.value }} after")).toBe("before  after");
    expect(renderTemplate("{{ fout[0].omschrijving }}", { fout: [{ omschrijving: "Ongeldige postcode" }] })).toBe(
      "Ongeldige postcode",
    );
  });

  it("escapes HTML only for HTML templates", () => {
    expect(renderHtmlTemplate("{{ name }}", { name: "<script>" })).toBe("&lt;script&gt;");
    expect(renderTemplate("{{ name }}", { name: "<script>" })).toBe("<script>");
  });

  it("escapes apostrophes in CQL template values", () => {
    const template = "straatnaam IN ('{{ straatnaam }}')";

    expect(renderCqlTemplate(template, { straatnaam: "O'Brien" })).toBe("straatnaam IN ('O''Brien')");
    expect(renderCqlTemplate(template, { straatnaam: "x') OR INCLUDE OR straatnaam IN ('x" })).toBe(
      "straatnaam IN ('x'') OR INCLUDE OR straatnaam IN (''x')",
    );
  });

  it("serializes rendered JSON request bodies without changing other value types", () => {
    const body = renderJsonTemplate('{"name":"{{ name }}","message":"Hello {{ name }}","limit":2}', {
      name: 'A "quoted" name',
    });

    expect(JSON.parse(body)).toEqual({
      name: 'A "quoted" name',
      message: 'Hello A "quoted" name',
      limit: 2,
    });

    expect(JSON.parse(renderJsonTemplate({ name: "{{ name }}", enabled: true }, { name: 'A "quoted" name' }))).toEqual({
      name: 'A "quoted" name',
      enabled: true,
    });
  });
});
