import { describe, expect, it } from "vitest";
import { getLayerCqlFilter } from "@/utils/layer-filter-cql";
import { ELayerFilterSource } from "@/types/mapStore";
import type { ILayerFilters } from "@/types/mapStore";

describe("getLayerCqlFilter", () => {
  it("returns null when a layer has no filters", () => {
    expect(getLayerCqlFilter({}, "layer-a")).toBeNull();
  });

  it("returns null when a layer has only empty filters", () => {
    const layerFilters: ILayerFilters = {
      "layer-a": {
        filters: {
          status: [],
        },
        searchQuery: "",
      },
    };

    expect(getLayerCqlFilter(layerFilters, "layer-a")).toBeNull();
  });

  it("builds a CQL filter for selected field values", () => {
    const layerFilters: ILayerFilters = {
      "layer-a": {
        filters: {
          status: ["Active", "Pending"],
        },
        searchQuery: "",
      },
    };

    expect(getLayerCqlFilter(layerFilters, "layer-a")).toBe("(status IN ('Active','Pending'))");
  });

  it("builds a CQL filter for empty and non-empty selected values", () => {
    const layerFilters: ILayerFilters = {
      "layer-a": {
        filters: {
          status: ["Leeg", "Active"],
        },
        searchQuery: "",
      },
    };

    expect(getLayerCqlFilter(layerFilters, "layer-a")).toBe(
      "((status IS NULL or status = '') OR status IN ('Active'))",
    );
  });

  it("combines search query and field filters", () => {
    const layerFilters: ILayerFilters = {
      "layer-a": {
        filters: {
          status: ["Active"],
        },
        searchQuery: "(name ILIKE '%tree%')",
      },
    };

    expect(getLayerCqlFilter(layerFilters, "layer-a")).toBe("(name ILIKE '%tree%') AND (status IN ('Active'))");
  });

  it("combines selected legend CQL filters with OR", () => {
    const layerFilters: ILayerFilters = {
      "layer-a": {
        filters: {},
        searchQuery: "",
        legendFilters: ["height >= 10", "status IN ('Protected','Monument')"],
        source: ELayerFilterSource.Legend,
      },
    };

    expect(getLayerCqlFilter(layerFilters, "layer-a")).toBe(
      "(height >= 10) OR (status IN ('Protected','Monument'))",
    );
  });

  it("ignores legend CQL filters when panel filters are active", () => {
    const layerFilters: ILayerFilters = {
      "layer-a": {
        filters: {
          status: ["Active"],
        },
        searchQuery: "",
        legendFilters: ["height >= 10"],
        source: ELayerFilterSource.Panel,
      },
    };

    expect(getLayerCqlFilter(layerFilters, "layer-a")).toBe("(status IN ('Active'))");
  });
});
