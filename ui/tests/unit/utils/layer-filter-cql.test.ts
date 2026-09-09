import { describe, expect, it } from "vitest";
import { getLayerCqlFilter } from "@/utils/layer-filter-cql";
import { ELayerFilterSource, EPanelFilterOperator } from "@/types/mapStore";
import type { ILayerFilters } from "@/types/mapStore";

describe("getLayerCqlFilter", () => {
  it("returns null when a layer has no filters", () => {
    expect(getLayerCqlFilter({}, "layer-a")).toBeNull();
  });

  it("returns null when a layer has only empty filters", () => {
    const layerFilters: ILayerFilters = {
      "layer-a": {
        filters: {
          status: {
            operator: EPanelFilterOperator.Equals,
            values: [],
            type: "string",
          },
        },
        searchQuery: "",
        legendFilters: [],
        source: ELayerFilterSource.Panel,
      },
    };

    expect(getLayerCqlFilter(layerFilters, "layer-a")).toBeNull();
  });

  it("builds a CQL filter for selected field values", () => {
    const layerFilters: ILayerFilters = {
      "layer-a": {
        filters: {
          status: {
            operator: EPanelFilterOperator.Equals,
            values: ["Active", "Pending"],
            type: "string",
          },
        },
        searchQuery: "",
        legendFilters: [],
        source: ELayerFilterSource.Panel,
      },
    };

    expect(getLayerCqlFilter(layerFilters, "layer-a")).toBe("status IN ('Active','Pending')");
  });

  it("builds a CQL filter for empty text values", () => {
    const layerFilters: ILayerFilters = {
      "layer-a": {
        filters: {
          status: {
            operator: EPanelFilterOperator.Empty,
            values: [],
            type: "string",
          },
        },
        searchQuery: "",
        legendFilters: [],
        source: ELayerFilterSource.Panel,
      },
    };

    expect(getLayerCqlFilter(layerFilters, "layer-a")).toBe("(status IS NULL OR status = '')");
  });

  it("builds equals filters from panel filter rules", () => {
    const layerFilters: ILayerFilters = {
      "layer-a": {
        filters: {
          status: {
            operator: EPanelFilterOperator.Equals,
            values: ["Active"],
            type: "string",
          },
        },
        searchQuery: "",
        legendFilters: [],
        source: ELayerFilterSource.Panel,
      },
    };

    expect(getLayerCqlFilter(layerFilters, "layer-a")).toBe("status = 'Active'");
  });

  it("escapes quotes in text filter values", () => {
    const layerFilters: ILayerFilters = {
      "layer-a": {
        filters: {
          name: {
            operator: EPanelFilterOperator.NotEquals,
            values: ["Bob's tree"],
            type: "string",
          },
        },
        searchQuery: "",
        legendFilters: [],
        source: ELayerFilterSource.Panel,
      },
    };

    expect(getLayerCqlFilter(layerFilters, "layer-a")).toBe("name <> 'Bob''s tree'");
  });

  it("builds numeric comparison filters without quotes", () => {
    const layerFilters: ILayerFilters = {
      "layer-a": {
        filters: {
          height: {
            operator: EPanelFilterOperator.GreaterThanOrEqual,
            values: [10],
            type: "number",
          },
        },
        searchQuery: "",
        legendFilters: [],
        source: ELayerFilterSource.Panel,
      },
    };

    expect(getLayerCqlFilter(layerFilters, "layer-a")).toBe("height >= 10");
  });

  it("builds numeric filters without quotes for GeoServer JSON DescribeFeatureType numeric types", () => {
    const numericTypes = ["xsd:int", "xs:number", "int", "number"];

    numericTypes.forEach((type) => {
      const layerFilters: ILayerFilters = {
        "layer-a": {
          filters: {
            height: {
              operator: EPanelFilterOperator.GreaterThanOrEqual,
              values: [10],
              type,
            },
          },
          searchQuery: "",
          legendFilters: [],
          source: ELayerFilterSource.Panel,
        },
      };

      expect(getLayerCqlFilter(layerFilters, "layer-a")).toBe("height >= 10");
    });
  });

  it("builds boolean filters without quotes for GeoServer DescribeFeatureType boolean types", () => {
    const layerFilters: ILayerFilters = {
      "layer-a": {
        filters: {
          active: {
            operator: EPanelFilterOperator.Equals,
            values: ["true"],
            type: "xsd:boolean",
          },
        },
        searchQuery: "",
        legendFilters: [],
        source: ELayerFilterSource.Panel,
      },
    };

    expect(getLayerCqlFilter(layerFilters, "layer-a")).toBe("active = true");
  });

  it("builds temporal filters without quotes for GeoServer JSON DescribeFeatureType temporal types", () => {
    const layerFilters: ILayerFilters = {
      "layer-a": {
        filters: {
          start_date: {
            operator: EPanelFilterOperator.GreaterThanOrEqual,
            values: ["2024-01-01"],
            type: "date",
          },
          start_time: {
            operator: EPanelFilterOperator.LessThan,
            values: ["12:30:00"],
            type: "time",
          },
          updated_at: {
            operator: EPanelFilterOperator.LessThanOrEqual,
            values: ["2024-01-01T12:30:00"],
            type: "date-time",
          },
        },
        searchQuery: "",
        legendFilters: [],
        source: ELayerFilterSource.Panel,
      },
    };

    expect(getLayerCqlFilter(layerFilters, "layer-a")).toBe(
      "start_date >= 2024-01-01 AND start_time < 12:30:00 AND updated_at <= 2024-01-01T12:30:00",
    );
  });

  it("normalizes prefixed GeoServer DescribeFeatureType text types", () => {
    const layerFilters: ILayerFilters = {
      "layer-a": {
        filters: {
          name: {
            operator: EPanelFilterOperator.Equals,
            values: ["Oak"],
            type: "xsd:string",
          },
        },
        searchQuery: "",
        legendFilters: [],
        source: ELayerFilterSource.Panel,
      },
    };

    expect(getLayerCqlFilter(layerFilters, "layer-a")).toBe("name = 'Oak'");
  });

  it("builds empty and not empty filters for text and numeric fields", () => {
    const layerFilters: ILayerFilters = {
      "layer-a": {
        filters: {
          name: {
            operator: EPanelFilterOperator.Empty,
            values: [],
            type: "string",
          },
          height: {
            operator: EPanelFilterOperator.NotEmpty,
            values: [],
            type: "number",
          },
        },
        searchQuery: "",
        legendFilters: [],
        source: ELayerFilterSource.Panel,
      },
    };

    expect(getLayerCqlFilter(layerFilters, "layer-a")).toBe("(name IS NULL OR name = '') AND height IS NOT NULL");
  });

  it("uses IN for multiple equals values", () => {
    const layerFilters: ILayerFilters = {
      "layer-a": {
        filters: {
          status: {
            operator: EPanelFilterOperator.Equals,
            values: ["Active", "Pending"],
            type: "string",
          },
        },
        searchQuery: "",
        legendFilters: [],
        source: ELayerFilterSource.Panel,
      },
    };

    expect(getLayerCqlFilter(layerFilters, "layer-a")).toBe("status IN ('Active','Pending')");
  });

  it("combines search query and field filters", () => {
    const layerFilters: ILayerFilters = {
      "layer-a": {
        filters: {
          status: {
            operator: EPanelFilterOperator.Equals,
            values: ["Active"],
            type: "string",
          },
        },
        searchQuery: "(name ILIKE '%tree%')",
        legendFilters: [],
        source: ELayerFilterSource.Panel,
      },
    };

    expect(getLayerCqlFilter(layerFilters, "layer-a")).toBe("(name ILIKE '%tree%') AND status = 'Active'");
  });

  it("combines selected bracketed legend CQL filters with OR", () => {
    const layerFilters: ILayerFilters = {
      "layer-a": {
        filters: {},
        searchQuery: "",
        legendFilters: ["[height >= 10]", "[status IN ('Protected','Monument')]"],
        source: ELayerFilterSource.Legend,
      },
    };

    expect(getLayerCqlFilter(layerFilters, "layer-a")).toBe(
      "([height >= 10]) OR ([status IN ('Protected','Monument')])",
    );
  });

  it("ignores legend CQL filters when panel filters are active", () => {
    const layerFilters: ILayerFilters = {
      "layer-a": {
        filters: {
          status: {
            operator: EPanelFilterOperator.Equals,
            values: ["Active"],
            type: "string",
          },
        },
        searchQuery: "",
        legendFilters: ["height >= 10"],
        source: ELayerFilterSource.Panel,
      },
    };

    expect(getLayerCqlFilter(layerFilters, "layer-a")).toBe("status = 'Active'");
  });
});
