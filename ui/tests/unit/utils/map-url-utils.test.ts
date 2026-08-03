import { afterEach, describe, expect, it, vi } from "vitest";

import { createLayer } from "../factories/layer.factory";
import { createPosition } from "../factories/position.factory";
import { buildMapStatePath, getMapPositionPath, pushHistoryState } from "@/utils/map-url-utils";

const position = createPosition({
  center: [126910, 505834],
  zoom: 13,
});

const DRAWING_UUID = "83ec9c5f-867f-4c74-96a8-151684e8a0d3";
const POSITION_URL_VALUE = `@${position.center[0].toFixed(2)},${position.center[1].toFixed(2)},${position.zoom}z`;

describe("getMapPositionPath", () => {
  it("formats center coordinates and zoom", () => {
    expect(getMapPositionPath(position)).toBe(POSITION_URL_VALUE);
  });
});

describe("buildMapStatePath", () => {
  it("builds map state paths with optional parameters in URL order", () => {
    const url = buildMapStatePath({
      basePath: "/atlas/maps/afvalbakken/",
      position: createPosition({
        center: [position.center[0], position.center[1]],
        zoom: position.zoom,
        marker: [126911.123, 505835.456],
      }),
      baseLayerId: "topografische-kaart-grijs",
      visibleLayerIds: ["afvalbakken"],
      drawing: DRAWING_UUID,
      isEmbed: true,
    });

    expect(url).toBe(
      `/atlas/maps/afvalbakken/${POSITION_URL_VALUE}/layers=afvalbakken/base=topografische-kaart-grijs/drawing=${DRAWING_UUID}/marker=126911.12,505835.46/is_embed=true`,
    );
  });
});

describe("pushHistoryState", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("preserves the primary map path", () => {
    const replaceState = vi.fn();
    vi.stubGlobal("window", {
      location: {
        pathname: "/atlas/",
      },
      history: {
        replaceState,
      },
    });

    pushHistoryState(
      position,
      createLayer({ id: "topografische-kaart-grijs", is_base: true }),
      [createLayer({ id: "afvalbakken" })],
      DRAWING_UUID,
    );

    expect(replaceState).toHaveBeenCalledWith(
      {},
      "",
      `/atlas/${POSITION_URL_VALUE}/layers=afvalbakken/base=topografische-kaart-grijs/drawing=${DRAWING_UUID}`,
    );
  });

  it("preserves the theme map path", () => {
    const replaceState = vi.fn();
    vi.stubGlobal("window", {
      location: {
        pathname: "/atlas/maps/afvalbakken/",
      },
      history: {
        replaceState,
      },
    });

    pushHistoryState(
      position,
      createLayer({ id: "topografische-kaart-grijs", is_base: true }),
      [createLayer({ id: "afvalbakken" })],
      DRAWING_UUID,
    );

    expect(replaceState).toHaveBeenCalledWith(
      {},
      "",
      `/atlas/maps/afvalbakken/${POSITION_URL_VALUE}/layers=afvalbakken/base=topografische-kaart-grijs/drawing=${DRAWING_UUID}`,
    );
  });
});
