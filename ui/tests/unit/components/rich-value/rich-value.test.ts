import { describe, expect, it } from "vitest";
import { normalizeUrlValue } from "@/utils/rich-value";

describe("RichValue", () => {
  it("normalizes spaces in URL values for href/src", () => {
    const normalizedUrl = normalizeUrlValue("https://example.com/some path/file name?q=hello world");

    expect(normalizedUrl).toBe("https://example.com/some%20path/file%20name?q=hello%20world");
  });

  it("leaves URLs without spaces unchanged", () => {
    const normalizedUrl = normalizeUrlValue("https://example.com/path?q=value");

    expect(normalizedUrl).toBe("https://example.com/path?q=value");
  });

  it("normalizes image URLs with spaces", () => {
    const normalizedUrl = normalizeUrlValue("https://example.com/images/my photo.jpg");

    expect(normalizedUrl).toBe("https://example.com/images/my%20photo.jpg");
  });

  it("returns empty string for non-string values", () => {
    expect(normalizeUrlValue(null)).toBe("");
    expect(normalizeUrlValue(123)).toBe("");
    expect(normalizeUrlValue({})).toBe("");
  });
});
