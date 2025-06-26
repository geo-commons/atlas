import Draw from "ol/interaction/Draw";
import VectorSource from "ol/source/Vector";
import { Circle, Fill, Stroke, Style } from "ol/style";
import { createMeasurementTooltip } from "./measure-tooltip";

const source = new VectorSource();

const constructDraw = (measure, map, onDrawStart, onDrawEnd, color, strokeWidth, fontSize) => {
  const mapping = {
    MEASURE_AREA: "Polygon",
    SELECT_AREA: "Polygon",
    SELECT_CIRCLE: "Circle",
    MEASURE_LINE: "LineString",
    DRAW_POINT: "Point",
    DRAW_LINE: "LineString",
    DRAW_POLYGON: "Polygon",
    DRAW_LABEL: "Point",
    DRAW_COORDINATE: "Point",
    Point: "Point",
    LineString: "LineString",
    LinearRing: "LinearRing",
    Polygon: "Polygon",
    MultiPoint: "MultiPoint",
    MultiLineString: "MultiLineString",
    MultiPolygon: "MultiPolygon",
    Circle: "Circle",
  };

  const draw = new Draw({
    source: source,
    type: mapping[measure],
    style: new Style({
      fill: new Fill({
        color: "rgba(255, 255, 255, 0.2)",
      }),
      stroke: new Stroke({
        color:
          measure === "MEASURE_LINE" ||
          measure === "MEASURE_AREA" ||
          measure === "SELECT_CIRCLE" ||
          measure === "SELECT_AREA"
            ? "rgba(0, 102, 255, 0.5)"
            : `rgba(${color.red}, ${color.green}, ${color.blue}, 0.5)`,
        lineDash: [10, 10],
        width: 2,
      }),
      image: new Circle({
        radius: 5,
        stroke: new Stroke({
          color: "rgba(0, 0, 0, 0.7)",
        }),
        fill: new Fill({
          color: "rgba(255, 255, 255, 0.2)",
        }),
      }),
    }),
  });

  // Complete drawing on escape or enter touch
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" || event.key === "Enter") {
      event.preventDefault();

      draw.finishDrawing();
    }
  });

  // Test to removeLastPoint
  document.addEventListener("keydown", (event) => {
    if (event.key === "Backspace" || event.key === "Delete") {
      draw.removeLastPoint();
    }
  });

  let measureTooltip;

  let sketch;
  draw.on("drawstart", (e) => {
    sketch = e.feature;

    if (!measure.startsWith("EDIT")) {
      sketch.setProperties({
        color: color,
        strokeWidth: strokeWidth,
        fontSize: fontSize,
      });
    }

    onDrawStart();

    map.removeOverlay(measureTooltip);

    if (
      measure === "MEASURE_LINE" ||
      measure === "MEASURE_AREA" ||
      measure === "SELECT_CIRCLE" ||
      measure === "SELECT_AREA"
    ) {
      sketch.getGeometry().on("change", () => {
        // Remove the old overlay from the map
        if (measureTooltip) {
          map.removeOverlay(measureTooltip);
        }

        // Create a new overlay
        measureTooltip = createMeasurementTooltip(sketch.getGeometry(), map, {
          isStatic: false,
          offset: [0, -15],
          className: "ol-tooltip-measure",
        });

        if (measureTooltip) {
          draw.measureTooltip = measureTooltip;
        }
      });
    }
  });

  draw.on("drawend", (evt) => {
    if (measure === "DRAW_LABEL") {
      const result = prompt("Voer het tekstlabel in");
      sketch.setProperties({
        label: result,
      });
    }

    if (measure === "DRAW_COORDINATE") {
      sketch.setProperties({
        xCoordinate: evt.feature.getGeometry().getCoordinates()[0],
        yCoordinate: evt.feature.getGeometry().getCoordinates()[1],
      });
    }

    if (measure === "MEASURE_LINE" || measure === "MEASURE_AREA") {
      // Remove the old overlay from the map
      if (draw.measureTooltip) {
        map.removeOverlay(draw.measureTooltip);
      }

      // Create static tooltip and track it
      const staticTooltip = createMeasurementTooltip(sketch.getGeometry(), map, {
        isStatic: true,
        offset: [0, -7],
        className: "ol-tooltip-static",
      });

      // Store the static tooltip for later cleanup
      if (staticTooltip && !map.measuredAreaTooltips) {
        map.measuredAreaTooltips = [];
      }
      if (staticTooltip) {
        map.measuredAreaTooltips.push(staticTooltip);
      }

      measureTooltip = null;
    }

    onDrawEnd(sketch);
  });

  return draw;
};

export default constructDraw;
