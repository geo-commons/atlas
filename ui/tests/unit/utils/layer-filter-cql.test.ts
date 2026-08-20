import { describe, expect, it } from "vitest";
import { getLayerCqlFilter, getLayerPropertyCqlFilter } from "@/utils/layer-filter-cql";
import { ELayerFilterOperator, type ILayerFilters } from "@/types/mapStore";

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

  it("escapes selected field values", () => {
    const layerFilters: ILayerFilters = {
      "layer-a": {
        filters: {
          status: ["Owner's choice"],
        },
        searchQuery: "",
      },
    };

    expect(getLayerCqlFilter(layerFilters, "layer-a")).toBe("(status IN ('Owner''s choice'))");
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

  it("combines raw CQL legend filters with OR", () => {
    const layerFilters: ILayerFilters = {
      "layer-a": {
        filters: {},
        rawCqlFilters: {
          ruleOne: "height > 10",
          ruleTwo: "status IS NULL",
        },
        searchQuery: "",
      },
    };

    expect(getLayerCqlFilter(layerFilters, "layer-a")).toBe("((height > 10) OR (status IS NULL))");
  });

  it("combines search query, raw CQL filters, and field filters", () => {
    const layerFilters: ILayerFilters = {
      "layer-a": {
        filters: {
          status: ["Active"],
        },
        rawCqlFilters: {
          ruleOne: "height > 10",
        },
        searchQuery: "(name ILIKE '%tree%')",
      },
    };

    expect(getLayerCqlFilter(layerFilters, "layer-a")).toBe(
      "(name ILIKE '%tree%') AND ((height > 10)) AND (status IN ('Active'))",
    );
  });
});

describe("getLayerPropertyCqlFilter", () => {
  it("builds a greater than filter", () => {
    expect(
      getLayerPropertyCqlFilter("height", {
        operator: ELayerFilterOperator.GreaterThan,
        values: ["10"],
      }),
    ).toBe("height > 10");
  });

  it("builds an ILIKE filter", () => {
    expect(
      getLayerPropertyCqlFilter("name", {
        operator: ELayerFilterOperator.ILike,
        values: ["tree"],
      }),
    ).toBe("name ILIKE '%tree%'");
  });

  it("builds an IS NULL filter", () => {
    expect(
      getLayerPropertyCqlFilter("name", {
        operator: ELayerFilterOperator.IsNull,
        values: [],
      }),
    ).toBe("(name IS NULL or name = '')");
  });
});
