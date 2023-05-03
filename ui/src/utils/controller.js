import Map from "ol/Map";
import View from "ol/View";
import TileLayer from "ol/layer/Tile";
import TileWMS from "ol/source/TileWMS";
import WMTSSource from "ol/source/WMTS";
import WMTSTileGrid from "ol/tilegrid/WMTS";
import {
  defaults as defaultInteractions,
  DragRotateAndZoom,
} from "ol/interaction";
import Projection from "ol/proj/Projection";
import { getTopLeft } from "ol/extent.js";

const rdProjection = new Projection({
  code: "EPSG:28992",
  extent: [-285401.92, 22598.08, 595401.92, 903401.92],
});

// can be calculated based on resolution z0, written out for clarity
// see https://www.geonovum.nl/uploads/standards/downloads/nederlandse_richtlijn_tiling_-_versie_1.1.pdf
const resolutions = [
  3440.64, 1720.32, 860.16, 430.08, 215.04, 107.52, 53.76, 26.88, 13.44, 6.72,
  3.36, 1.68, 0.84, 0.42, 0.21,
];

const matrixIds = new Array(15);
for (var i = 0; i < 15; ++i) {
  matrixIds[i] = i;
}

class MapController {
  constructor(settings) {
    this.settings = settings;
    this.layers = [];
  }

  addLayers(layers) {
    layers.forEach((layer) => {
      this.addLayer(layer);
    });
  }

  addLayer(layer) {
    let tileLayer;
    if (layer.source_type === "WMTS") {
      tileLayer = new TileLayer({
        id: layer.id,
        visible:
          layer.is_visible === true ||
          this.settings.visibleLayers.includes(layer.id),
        layerName: layer.name,
        opacity: layer.opacity,
        extent: rdProjection.extent,
        source: new WMTSSource({
          url: layer.url,
          layer: layer.name,
          matrixSet: layer.projection,
          format: "image/png",
          projection: rdProjection,
          tileGrid: new WMTSTileGrid({
            origin: getTopLeft(rdProjection.getExtent()),
            resolutions,
            matrixIds,
          }),
        }),
      });
    } else {
      tileLayer = new TileLayer({
        id: layer.id,
        visible:
          layer.is_visible === true ||
          this.settings.visibleLayers.includes(layer.id),
        layerName: layer.name,
        opacity: layer.opacity,
        source: new TileWMS({
          projection: "EPSG:28992",
          url: layer.url,
          servertype: layer.server_type,
          params: { layers: layer.name },
        }),
      });
    }

    this.layers = [...this.layers, tileLayer];
  }

  render(targetId) {
    return new Map({
      interactions: defaultInteractions().extend([new DragRotateAndZoom()]),
      layers: this.layers,
      target: targetId,
      view: new View({
        projection: "EPSG:28992",
        center: this.settings.position.center,
        zoom: this.settings.position.zoom,
      }),
    });
  }
}

export default MapController;
