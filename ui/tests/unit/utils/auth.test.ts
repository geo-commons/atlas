import { describe, expect, it } from "vitest";
import { getFetchParameters, layerRequiresAuthentication } from "@/utils/auth";
import { createLayer } from "../factories/layer.factory";

describe("layerRequiresAuthentication", () => {
  it("returns true when the layer source forwards authentication", () => {
    const layer = createLayer({ source: { authenticate: true }, login_required: false });

    expect(layerRequiresAuthentication(layer)).toBe(true);
  });

  it("returns false when the layer source does not forward authentication", () => {
    const layer = createLayer({ source: { authenticate: false }, login_required: true });

    expect(layerRequiresAuthentication(layer)).toBe(false);
  });
});

describe("getFetchParameters", () => {
  it("returns an authorization header when source authentication is enabled", () => {
    const layer = createLayer({ source: { authenticate: true }, login_required: false });

    expect(getFetchParameters(layer, { token: "test-token" })).toEqual({
      headers: { Authorization: "Bearer test-token" },
    });
  });

  it("returns empty options when source authentication is disabled", () => {
    const layer = createLayer({ source: { authenticate: false }, login_required: true });

    expect(getFetchParameters(layer, { token: "test-token" })).toEqual({});
  });

  it("returns empty options when the user has no token", () => {
    const layer = createLayer({ source: { authenticate: true }, login_required: true });

    expect(getFetchParameters(layer, null)).toEqual({});
  });
});
