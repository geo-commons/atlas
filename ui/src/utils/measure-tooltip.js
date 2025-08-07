import Overlay from "ol/Overlay";
import { getArea, getLength } from "ol/sphere";

/**
 * Creates a measurement tooltip for a geometry
 * @param {Object} geometry - OpenLayers geometry object
 * @param {Object} map - OpenLayers map object
 * @param {Object} options - Configuration options
 * @param {boolean} options.isStatic - Whether the tooltip should be static (default: false)
 * @param {Array} options.offset - Tooltip offset [x, y] (default: [0, -15] for dynamic, [0, -7] for static)
 * @param {string} options.className - CSS class name (default: 'ol-tooltip-measure' for dynamic, 'ol-tooltip-static' for static)
 * @returns {Object} The created overlay object
 */
export const createMeasurementTooltip = (geometry, map, options = {}) => {
  const { isStatic = false, offset, className } = options;

  let tooltipCoord;
  let value;

  if (geometry.getType() === "Polygon" || geometry.getType() === "MultiPolygon") {
    tooltipCoord = geometry.getInteriorPoint().getCoordinates();
    value = `${Number(getArea(geometry).toFixed(2))} m²`;
  } else if (geometry.getType() === "LineString" || geometry.getType() === "MultiLineString") {
    tooltipCoord = geometry.getLastCoordinate();
    value = `${Number(getLength(geometry).toFixed(2))} m`;
  } else if (geometry.getType() === "Circle") {
    tooltipCoord = geometry.getCenter();
    value = `Straal: ${Math.round(geometry.getRadius() * 100) / 100} m`;
  } else {
    return null;
  }

  // Create tooltip element
  const measureTooltipElement = document.createElement("div");
  measureTooltipElement.className = `ol-tooltip ${className || (isStatic ? "ol-tooltip-static" : "ol-tooltip-measure")}`;
  measureTooltipElement.innerHTML = value;

  // Create overlay
  const measureTooltip = new Overlay({
    element: measureTooltipElement,
    offset: offset || (isStatic ? [0, -7] : [0, -15]),
    positioning: "bottom-center",
    stopEvent: false,
    insertFirst: false,
  });

  // Add to map
  measureTooltip.setPosition(tooltipCoord);
  map.addOverlay(measureTooltip);

  return measureTooltip;
};

/**
 * Removes all measurement tooltips from the map
 * @param {Object} map - OpenLayers map object
 * @param {Array} tooltips - Array of tooltip overlays to remove (optional)
 */
export const clearMeasurementTooltips = (map, tooltips = []) => {
  // Remove specific tooltips if provided
  tooltips.forEach((tooltip) => {
    if (tooltip) {
      map.removeOverlay(tooltip);
    }
  });

  // Remove tooltips stored on the map object
  if (map.measuredAreaTooltips && Array.isArray(map.measuredAreaTooltips)) {
    map.measuredAreaTooltips.forEach((tooltip) => {
      if (tooltip) {
        map.removeOverlay(tooltip);
      }
    });
    map.measuredAreaTooltips = [];
  }

  // Remove all measurement tooltips from the map
  const overlays = map.getOverlays().getArray();
  overlays.forEach((overlay) => {
    const element = overlay.getElement();
    if (
      element &&
      element.className &&
      (element.className.includes("ol-tooltip-measure") || element.className.includes("ol-tooltip-static"))
    ) {
      map.removeOverlay(overlay);
    }
  });
};
