import { afterEach, describe, expect, it, vi } from "vitest";
import { ETimeSliderDisplayMode, ETimeSliderStepSize } from "@/types/mapStore";
import {
  createOgcCollectionUrl,
  getLayerTimeRange,
  getWfsTimeCqlFilter,
  getWmsTimeParameter,
  parseOgcTimeRange,
} from "@/utils/wms-time";
import { createMapStore } from "../factories/mapStore.factory";
import { createLayer } from "../factories/layer.factory";

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("parseOgcTimeRange", () => {
  it("parses an OGC API temporal interval", () => {
    const range = parseOgcTimeRange({
      extent: {
        temporal: {
          interval: [["1900-06-17T00:00:00Z", "2024-06-18T00:00:00Z"]],
        },
      },
    });

    expect(range?.minDate.toISOString()).toBe("1900-06-17T00:00:00.000Z");
    expect(range?.maxDate.toISOString()).toBe("2024-06-18T00:00:00.000Z");
  });

  it("parses multiple OGC API temporal intervals", () => {
    const range = parseOgcTimeRange({
      extent: {
        temporal: {
          interval: [
            ["2020-01-01T00:00:00Z", "2020-12-31T00:00:00Z"],
            ["2022-01-01T00:00:00Z", "2022-12-31T00:00:00Z"],
          ],
        },
      },
    });

    expect(range?.minDate.toISOString()).toBe("2020-01-01T00:00:00.000Z");
    expect(range?.maxDate.toISOString()).toBe("2022-12-31T00:00:00.000Z");
  });

  it("returns null when no valid OGC API temporal interval exists", () => {
    expect(parseOgcTimeRange({ extent: { temporal: { interval: [[null, null]] } } })).toBeNull();
  });
});

describe("createOgcCollectionUrl", () => {
  it("creates an OGC API collection URL from a GeoServer workspace WMS URL", () => {
    const url = createOgcCollectionUrl(
      createLayer({
        name: "custom:scholen-tijdlijn",
        url: "http://localhost:8080/geoserver/custom/wms?SERVICE=WMS",
      }),
    );

    expect(url.toString()).toBe(
      "http://localhost:8080/geoserver/ogc/maps/v1/collections/custom:scholen-tijdlijn?f=application%2Fjson",
    );
  });

  it("uses an unqualified layer name as the OGC API collection id", () => {
    const url = createOgcCollectionUrl(
      createLayer({ name: "scholen-tijdlijn", url: "http://localhost:8080/geoserver/custom/wms" }),
    );

    expect(url.toString()).toBe(
      "http://localhost:8080/geoserver/ogc/maps/v1/collections/scholen-tijdlijn?f=application%2Fjson",
    );
  });
});

describe("getLayerTimeRange", () => {
  it("uses the OGC API temporal extent when available", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        new Response(
          JSON.stringify({
            extent: {
              temporal: {
                interval: [["1900-06-17T00:00:00Z", "2024-06-18T00:00:00Z"]],
              },
            },
          }),
          { status: 200 },
        ),
      ),
    );

    const range = await getLayerTimeRange(createLayer({ name: "custom:scholen-tijdlijn" }));

    expect(range?.minDate.toISOString()).toBe("1900-06-17T00:00:00.000Z");
    expect(range?.maxDate.toISOString()).toBe("2024-06-18T00:00:00.000Z");
    expect(fetch).toHaveBeenCalledOnce();
  });

  it("returns null when the OGC API collection does not contain a usable range", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValueOnce(new Response(JSON.stringify({}), { status: 200 })));

    await expect(getLayerTimeRange(createLayer({ name: "custom:scholen-tijdlijn" }))).resolves.toBeNull();

    expect(fetch).toHaveBeenCalledOnce();
  });

  it("throws when the OGC API collection cannot be fetched", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValueOnce(new Response("", { status: 500 })));

    await expect(getLayerTimeRange(createLayer({ name: "custom:scholen-tijdlijn" }))).rejects.toThrow(
      "OGC API collectie kon niet opgehaald worden.",
    );

    expect(fetch).toHaveBeenCalledOnce();
  });
});

describe("getWmsTimeParameter", () => {
  it("does not add TIME for layers without time support", () => {
    expect(getWmsTimeParameter(createMapStore(), "layer-a", false)).toBeNull();
  });

  it("does not add TIME for time-enabled layers when the time slider does not target the layer", () => {
    expect(getWmsTimeParameter(createMapStore({ selectedTimeSliderLayerId: "layer-b" }), "layer-a", true)).toBeNull();
  });

  it("formats the selected period as a WMS time interval", () => {
    expect(getWmsTimeParameter(createMapStore({ selectedTimeSliderLayerId: "layer-a" }), "layer-a", true)).toBe(
      "2020-01-01T00:00:00.000Z/2024-12-31T23:59:59.999Z",
    );
  });

  it("formats the selected reference year as a WMS time instant", () => {
    expect(
      getWmsTimeParameter(
        createMapStore({
          selectedTimeSliderLayerId: "layer-a",
          timeSliderDisplayMode: ETimeSliderDisplayMode.ReferenceDate,
        }),
        "layer-a",
        true,
      ),
    ).toBe("2024-01-01T00:00:00.000Z");
  });

  it("formats the selected reference month as a WMS time instant", () => {
    expect(
      getWmsTimeParameter(
        createMapStore({
          selectedTimeSliderLayerId: "layer-a",
          timeSliderDisplayMode: ETimeSliderDisplayMode.ReferenceDate,
          timeSliderStepSize: ETimeSliderStepSize.Month,
        }),
        "layer-a",
        true,
      ),
    ).toBe("2024-06-01T00:00:00.000Z");
  });

  it("formats the selected reference day as a WMS time instant", () => {
    expect(
      getWmsTimeParameter(
        createMapStore({
          selectedTimeSliderLayerId: "layer-a",
          timeSliderDisplayMode: ETimeSliderDisplayMode.ReferenceDate,
          timeSliderStepSize: ETimeSliderStepSize.Day,
        }),
        "layer-a",
        true,
      ),
    ).toBe("2024-06-15T00:00:00.000Z");
  });
});

describe("getWfsTimeCqlFilter", () => {
  it("does not add a CQL filter for layers without time support", () => {
    expect(
      getWfsTimeCqlFilter(
        createMapStore({ selectedTimeSliderLayerId: "layer-a" }),
        createLayer({ is_time_enabled: false }),
      ),
    ).toBeNull();
  });

  it("does not add a CQL filter when the time slider does not target the layer", () => {
    expect(getWfsTimeCqlFilter(createMapStore({ selectedTimeSliderLayerId: "layer-b" }), createLayer())).toBeNull();
  });

  it("does not add a CQL filter when the layer start time field is missing", () => {
    expect(
      getWfsTimeCqlFilter(
        createMapStore({ selectedTimeSliderLayerId: "layer-a" }),
        createLayer({ time_slider_start_field: null }),
      ),
    ).toBeNull();
  });

  it("creates a period overlap CQL filter", () => {
    expect(getWfsTimeCqlFilter(createMapStore({ selectedTimeSliderLayerId: "layer-a" }), createLayer())).toBe(
      "(valid_from <= '2024-12-31T23:59:59.999Z' AND valid_to >= '2020-01-01T00:00:00.000Z')",
    );
  });

  it("creates a reference date CQL filter", () => {
    expect(
      getWfsTimeCqlFilter(
        createMapStore({
          selectedTimeSliderLayerId: "layer-a",
          timeSliderDisplayMode: ETimeSliderDisplayMode.ReferenceDate,
        }),
        createLayer(),
      ),
    ).toBe("(valid_from <= '2024-01-01T00:00:00.000Z' AND valid_to >= '2024-01-01T00:00:00.000Z')");
  });

  it("creates a period filter when no end time field is configured", () => {
    expect(
      getWfsTimeCqlFilter(
        createMapStore({ selectedTimeSliderLayerId: "layer-a" }),
        createLayer({ time_slider_end_field: null }),
      ),
    ).toBe("(valid_from >= '2020-01-01T00:00:00.000Z' AND valid_from <= '2024-12-31T23:59:59.999Z')");
  });

  it("creates a reference date CQL filter when no end time field is configured", () => {
    expect(
      getWfsTimeCqlFilter(
        createMapStore({
          selectedTimeSliderLayerId: "layer-a",
          timeSliderDisplayMode: ETimeSliderDisplayMode.ReferenceDate,
          timeSliderStepSize: ETimeSliderStepSize.Day,
        }),
        createLayer({ time_slider_end_field: null }),
      ),
    ).toBe("valid_from = '2024-06-15T00:00:00.000Z'");
  });
});
