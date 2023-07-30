import Draw from "ol/interaction/Draw";
import VectorSource from "ol/source/Vector";
import Overlay from "ol/Overlay";
import { getArea, getLength } from "ol/sphere";
import { Circle, Fill, Stroke, Style } from "ol/style";

const source = new VectorSource();

const constructDraw = (measure, map, onDrawStart, onDrawEnd) => {
  const mapping = {
    MEASURE_AREA: "Polygon",
    SELECT_AREA: "Polygon",
    MEASURE_LINE: "LineString",
    DRAW_POINT: "Point",
    DRAW_LINE: "LineString",
    DRAW_POLYGON: "Polygon",
    DRAW_LABEL: "Point",
  };

  const draw = new Draw({
    source: source,
    type: mapping[measure],
    style: new Style({
      fill: new Fill({
        color: "rgba(255, 255, 255, 0.2)",
      }),
      stroke: new Stroke({
        color: "rgba(0, 0, 0, 0.5)",
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

  let measureTooltipElement;
  let measureTooltip;

  let sketch;
  draw.on("drawstart", (e) => {
    sketch = e.feature;

    onDrawStart();

    map.removeOverlay(measureTooltip);

    if (measure === "MEASURE_LINE" || measure === "MEASURE_AREA") {
      sketch.getGeometry().on("change", (e) => {
        const geom = e.target;

        let tooltipCoord;
        if (measure === "MEASURE_LINE") {
          tooltipCoord = geom.getLastCoordinate();
        } else if (measure === "MEASURE_AREA") {
          tooltipCoord = geom.getInteriorPoint().getCoordinates();
        }

        if (measureTooltipElement) {
          measureTooltipElement.parentNode.removeChild(measureTooltipElement);
        }

        measureTooltipElement = document.createElement("div");
        measureTooltipElement.className = "ol-tooltip ol-tooltip-measure";
        measureTooltip = new Overlay({
          element: measureTooltipElement,
          offset: [0, -15],
          positioning: "bottom-center",
          stopEvent: false,
          insertFirst: false,
        });

        map.addOverlay(measureTooltip);
        draw.measureTooltip = measureTooltip;

        let measureResult;
        if (measure === "MEASURE_LINE") {
          measureResult = getLength(sketch.getGeometry());
          measureTooltipElement.innerHTML = `${
            Math.round(measureResult * 100) / 100
          } m`;
        } else if (measure === "MEASURE_AREA") {
          measureResult = getArea(sketch.getGeometry());
          measureTooltipElement.innerHTML = `${
            Math.round(measureResult * 100) / 100
          } m2`;
        }

        measureTooltip.setPosition(tooltipCoord);
      });
    }
  });

  draw.on("drawend", () => {
    if (measure === "DRAW_LABEL") {
      const result = prompt("Voer het tekstlabel in");
      sketch.setProperties({
        label: result,
      });
    }

    if (measure === "MEASURE_LINE" || measure === "MEASURE_AREA") {
      measureTooltipElement.className = "ol-tooltip ol-tooltip-static";
      measureTooltip.setOffset([0, -7]);
      measureTooltipElement = null;
    }

    onDrawEnd(sketch);
  });

  return draw;
};

export default constructDraw;
