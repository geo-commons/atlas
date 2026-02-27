import { describe, expect, it } from "vitest";
import { pickTemplateValues } from "@/components/related-tables/utils";

describe("pickTemplateValues", () => {
  it("extracts plain and dot-notation template variables", () => {
    const template = "http://url.com/{{kvkNummer}}?foo={{user.id}}";
    const values = {
      kvkNummer: "123",
      user: { id: 5 },
    };

    expect(pickTemplateValues(template, values)).toEqual({
      kvkNummer: "123",
      "user.id": 5,
    });
  });

  it("supports whitespace and ignores nunjucks filters in lookups", () => {
    const template = "{{  foo   | lower }} {{ user.name | trim }}";
    const values = {
      foo: "HELLO",
      user: { name: "  John  " },
    };

    expect(pickTemplateValues(template, values)).toEqual({
      foo: "HELLO",
      "user.name": "  John  ",
    });
  });

  it("returns undefined for missing keys", () => {
    const template = "{{does.not.exist}}";
    const values = {
      user: { id: 1 },
    };

    expect(pickTemplateValues(template, values)).toEqual({
      "does.not.exist": undefined,
    });
  });

  it("returns an empty object when no template variables are present", () => {
    const template = "https://example.com/static/path";

    expect(pickTemplateValues(template, { foo: "bar" })).toEqual({});
  });
});
