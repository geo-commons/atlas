import { describe, expect, it } from "vitest";
import { ETimeSliderDisplayMode, ETimeSliderStepSize } from "@/types/mapStore";
import { getWfsTimeCqlFilter, getWmsTimeParameter, parseWmsTimeRange } from "@/utils/wms-time";
import { createMapStore } from "../factories/mapStore.factory";
import { createLayer } from "../factories/layer.factory";

describe("parseWmsTimeRange", () => {
  it("parses a WMS time interval", () => {
    const range = parseWmsTimeRange("2020-01-01/2024-12-31/P1D");

    expect(range?.minDate.toISOString()).toBe("2020-01-01T00:00:00.000Z");
    expect(range?.maxDate.toISOString()).toBe("2024-12-31T00:00:00.000Z");
  });

  it("parses comma-separated WMS time instants", () => {
    const range = parseWmsTimeRange("2024-01-01,2020-01-01,2022-01-01");

    expect(range?.minDate.toISOString()).toBe("2020-01-01T00:00:00.000Z");
    expect(range?.maxDate.toISOString()).toBe("2024-01-01T00:00:00.000Z");
  });

  it("parses comma-separated WMS time intervals", () => {
    const range = parseWmsTimeRange("2020-01-01/2020-12-31/P1D,2022-01-01/2022-12-31/P1D");

    expect(range?.minDate.toISOString()).toBe("2020-01-01T00:00:00.000Z");
    expect(range?.maxDate.toISOString()).toBe("2022-12-31T00:00:00.000Z");
  });

  it("returns null when no valid time values exist", () => {
    expect(parseWmsTimeRange("not-a-date/P1D")).toBeNull();
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
