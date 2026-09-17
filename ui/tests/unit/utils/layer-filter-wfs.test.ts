import { DOMImplementation, XMLSerializer } from "@xmldom/xmldom";
import { beforeAll, describe, expect, it } from "vitest";
import { during, within } from "ol/format/filter";
import Point from "ol/geom/Point";
import { getLayerFilter } from "@/utils/layer-filter-wfs";
import { ELayerFilterSource, EPanelFilterOperator } from "@/types/mapStore";
import type { ILayerFilters } from "@/types/mapStore";

beforeAll(() => {
  Object.assign(globalThis, {
    document: new DOMImplementation().createDocument(null, "document", null),
    XMLSerializer,
  });
});

describe("getLayerFilter", () => {
  it("creates a Filter Encoding 2.0 BBOX filter without layer filters", () => {
    expect(getLayerFilter({}, "layer-a", [1, 2, 3, 4])).toBe(
      '<Filter xmlns="http://www.opengis.net/fes/2.0"><BBOX><ValueReference>geom</ValueReference><Envelope srsName="EPSG:28992" xmlns="http://www.opengis.net/gml/3.2"><lowerCorner>1 2</lowerCorner><upperCorner>3 4</upperCorner></Envelope></BBOX></Filter>',
    );
  });

  it("returns null when there are no active filters", () => {
    expect(getLayerFilter({}, "layer-a")).toBeNull();
  });

  it("builds comparisons directly from panel filter state", () => {
    const layerFilters: ILayerFilters = {
      "layer-a": {
        filters: {
          status: { operator: EPanelFilterOperator.Equals, values: ["Active", "Pending"], type: "string" },
          height: { operator: EPanelFilterOperator.GreaterThanOrEqual, values: [10], type: "number" },
        },
        searchProperties: [],
        searchValue: "",
        legendFilters: [],
        source: ELayerFilterSource.Panel,
      },
    };

    expect(getLayerFilter(layerFilters, "layer-a", [1, 2, 3, 4])).toBe(
      '<Filter xmlns="http://www.opengis.net/fes/2.0"><And><BBOX><ValueReference>geom</ValueReference><Envelope srsName="EPSG:28992" xmlns="http://www.opengis.net/gml/3.2"><lowerCorner>1 2</lowerCorner><upperCorner>3 4</upperCorner></Envelope></BBOX><Or><PropertyIsEqualTo><ValueReference>status</ValueReference><Literal>Active</Literal></PropertyIsEqualTo><PropertyIsEqualTo><ValueReference>status</ValueReference><Literal>Pending</Literal></PropertyIsEqualTo></Or><PropertyIsGreaterThanOrEqualTo><ValueReference>height</ValueReference><Literal>10</Literal></PropertyIsGreaterThanOrEqualTo></And></Filter>',
    );
  });

  it("builds search filters directly from the search value and properties", () => {
    const layerFilters: ILayerFilters = {
      "layer-a": {
        filters: {},
        searchProperties: ["name", "description"],
        searchValue: "tree",
        legendFilters: [],
        source: ELayerFilterSource.Panel,
      },
    };

    expect(getLayerFilter(layerFilters, "layer-a")).toBe(
      '<Filter xmlns="http://www.opengis.net/fes/2.0"><Or><PropertyIsLike wildCard="*" singleChar="." escapeChar="!" matchCase="false"><ValueReference>name</ValueReference><Literal>*tree*</Literal></PropertyIsLike><PropertyIsLike wildCard="*" singleChar="." escapeChar="!" matchCase="false"><ValueReference>description</ValueReference><Literal>*tree*</Literal></PropertyIsLike></Or></Filter>',
    );
  });

  it("creates text empty and not-empty filters with null and empty string checks", () => {
    const layerFilters: ILayerFilters = {
      "layer-a": {
        filters: {
          description: { operator: EPanelFilterOperator.Empty, values: [], type: "string" },
          name: { operator: EPanelFilterOperator.NotEmpty, values: [], type: "xsd:string" },
        },
        legendFilters: [],
        source: ELayerFilterSource.Panel,
      },
    };

    expect(getLayerFilter(layerFilters, "layer-a")).toBe(
      '<Filter xmlns="http://www.opengis.net/fes/2.0"><And><Or><PropertyIsNull><ValueReference>description</ValueReference></PropertyIsNull><PropertyIsEqualTo><ValueReference>description</ValueReference><Literal></Literal></PropertyIsEqualTo></Or><And><Not><PropertyIsNull><ValueReference>name</ValueReference></PropertyIsNull></Not><PropertyIsNotEqualTo><ValueReference>name</ValueReference><Literal></Literal></PropertyIsNotEqualTo></And></And></Filter>',
    );
  });

  it("creates null-only empty filters for non-text properties", () => {
    const layerFilters: ILayerFilters = {
      "layer-a": {
        filters: { height: { operator: EPanelFilterOperator.Empty, values: [], type: "number" } },
        legendFilters: [],
        source: ELayerFilterSource.Panel,
      },
    };

    expect(getLayerFilter(layerFilters, "layer-a")).toBe(
      '<Filter xmlns="http://www.opengis.net/fes/2.0"><PropertyIsNull><ValueReference>height</ValueReference></PropertyIsNull></Filter>',
    );
  });

  it("ignores filters without a selected value", () => {
    const layerFilters: ILayerFilters = {
      "layer-a": {
        filters: { status: { operator: EPanelFilterOperator.Equals, values: [], type: "string" } },
        legendFilters: [],
        source: ELayerFilterSource.Panel,
      },
    };

    expect(getLayerFilter(layerFilters, "layer-a")).toBeNull();
  });

  it("converts legend CQL filters through the GeoStyler parser", () => {
    const layerFilters: ILayerFilters = {
      "layer-a": {
        filters: {},
        legendFilters: ["[status IN ('Protected','Monument')]", "height >= 10"],
        source: ELayerFilterSource.Legend,
      },
    };

    expect(getLayerFilter(layerFilters, "layer-a")).toBe(
      '<Filter xmlns="http://www.opengis.net/fes/2.0"><Or><Or><PropertyIsEqualTo><ValueReference>status</ValueReference><Literal>Protected</Literal></PropertyIsEqualTo><PropertyIsEqualTo><ValueReference>status</ValueReference><Literal>Monument</Literal></PropertyIsEqualTo></Or><PropertyIsGreaterThanOrEqualTo><ValueReference>height</ValueReference><Literal>10</Literal></PropertyIsGreaterThanOrEqualTo></Or></Filter>',
    );
  });

  it("converts ordered comparison operators in legend CQL", () => {
    const layerFilters: ILayerFilters = {
      "layer-a": {
        filters: {},
        legendFilters: ["height >= 10"],
        source: ELayerFilterSource.Legend,
      },
    };

    expect(getLayerFilter(layerFilters, "layer-a")).toBe(
      '<Filter xmlns="http://www.opengis.net/fes/2.0"><PropertyIsGreaterThanOrEqualTo><ValueReference>height</ValueReference><Literal>10</Literal></PropertyIsGreaterThanOrEqualTo></Filter>',
    );
  });

  it("converts negated, LIKE, and nested logical legend CQL", () => {
    const layerFilters: ILayerFilters = {
      "layer-a": {
        filters: {},
        legendFilters: ["NOT status = 'Archived'", "name ILIKE '%oak_%'", "(height >= 10 AND height < 20)"],
        source: ELayerFilterSource.Legend,
      },
    };

    expect(getLayerFilter(layerFilters, "layer-a")).toBe(
      '<Filter xmlns="http://www.opengis.net/fes/2.0"><Or><Not><PropertyIsEqualTo><ValueReference>status</ValueReference><Literal>Archived</Literal></PropertyIsEqualTo></Not><PropertyIsLike wildCard="*" singleChar="." escapeChar="!" matchCase="false"><ValueReference>name</ValueReference><Literal>*oak.*</Literal></PropertyIsLike><And><PropertyIsGreaterThanOrEqualTo><ValueReference>height</ValueReference><Literal>10</Literal></PropertyIsGreaterThanOrEqualTo><PropertyIsLessThan><ValueReference>height</ValueReference><Literal>20</Literal></PropertyIsLessThan></And></Or></Filter>',
    );
  });

  it("combines BBOX, layer, area, and time filters in one AND expression", () => {
    const layerFilters: ILayerFilters = {
      "layer-a": {
        filters: { status: { operator: EPanelFilterOperator.Equals, values: ["Active"], type: "string" } },
        legendFilters: [],
        source: ELayerFilterSource.Panel,
      },
    };
    const areaFilter = within("geom", new Point([120000, 500000]), "EPSG:28992");
    const timeFilter = during("updated_at", "2025-01-01T00:00:00Z", "2025-01-31T23:59:59Z");

    expect(getLayerFilter(layerFilters, "layer-a", [1, 2, 3, 4], [areaFilter, timeFilter])).toBe(
      '<Filter xmlns="http://www.opengis.net/fes/2.0"><And><BBOX><ValueReference>geom</ValueReference><Envelope srsName="EPSG:28992" xmlns="http://www.opengis.net/gml/3.2"><lowerCorner>1 2</lowerCorner><upperCorner>3 4</upperCorner></Envelope></BBOX><Within><ValueReference>geom</ValueReference><Point srsName="EPSG:28992" xmlns="http://www.opengis.net/gml/3.2"><pos srsDimension="2">120000 500000</pos></Point></Within><During><ValueReference>updated_at</ValueReference><TimePeriod xmlns="http://www.opengis.net/gml"><begin><TimeInstant><timePosition>2025-01-01T00:00:00Z</timePosition></TimeInstant></begin><end><TimeInstant><timePosition>2025-01-31T23:59:59Z</timePosition></TimeInstant></end></TimePeriod></During><PropertyIsEqualTo><ValueReference>status</ValueReference><Literal>Active</Literal></PropertyIsEqualTo></And></Filter>',
    );
  });
});
