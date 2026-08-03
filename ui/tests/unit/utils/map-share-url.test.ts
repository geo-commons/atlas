import { describe, expect, it } from "vitest";

import { createLayer } from "../factories/layer.factory";
import { createPosition } from "../factories/position.factory";
import { getMapShareUrl } from "@/utils/map-share-url";

const position = createPosition({
  center: [126910, 505834],
  zoom: 13,
});

const layers = [
  createLayer({ id: "topografische-kaart-grijs", is_base: true }),
  createLayer({ id: "afvalbakken" }),
  createLayer({ id: "verborgen-laag", is_visible: false }),
];

describe("getMapShareUrl", () => {
  it("builds drawing URLs for the primary map", () => {
    const url = getMapShareUrl({
      origin: "http://localhost:8000",
      mapId: "primary",
      position,
      layers,
      drawing: "83ec9c5f-867f-4c74-96a8-151684e8a0d3",
    });

    expect(url).toBe(
      "http://localhost:8000/atlas/@126910.00,505834.00,13z/layers=afvalbakken/base=topografische-kaart-grijs/drawing=83ec9c5f-867f-4c74-96a8-151684e8a0d3",
    );
  });

  it("builds drawing URLs for theme maps", () => {
    const url = getMapShareUrl({
      origin: "http://localhost:8000",
      mapId: "afvalbakken",
      position,
      layers,
      drawing: "83ec9c5f-867f-4c74-96a8-151684e8a0d3",
    });

    expect(url).toBe(
      "http://localhost:8000/atlas/maps/afvalbakken/@126910.00,505834.00,13z/layers=afvalbakken/base=topografische-kaart-grijs/drawing=83ec9c5f-867f-4c74-96a8-151684e8a0d3",
    );
  });

  it("can build embed URLs", () => {
    const url = getMapShareUrl({
      origin: "http://localhost:8000",
      mapId: "afvalbakken",
      position,
      layers,
      isEmbed: true,
    });

    expect(url).toBe(
      "http://localhost:8000/atlas/maps/afvalbakken/@126910.00,505834.00,13z/layers=afvalbakken/base=topografische-kaart-grijs/is_embed=true",
    );
  });
});
