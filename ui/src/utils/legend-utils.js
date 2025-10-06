import TileWMS from "ol/source/TileWMS";
import Projection from "ol/proj/Projection";
import View from "ol/View";
import { getFetchParameters, layerRequiresAuthentication } from "@/utils/auth";
import { getPointResolution } from "ol/proj";

export const fetchLegendImage = async (layer, position, user) => {
  let legendImage;
  let error = false;
  const wmsSource = new TileWMS({
    url: layer.url,
    servertype: layer.server_type,
    params: {
      LAYERS: layer.name,
      TILED: true,
    },
  });

  const rdProjection = new Projection({
    code: "EPSG:28992",
    units: "m",
  });

  const view = new View({
    projection: rdProjection,
    enableRotation: false,
    center: position.center,
    zoom: position.zoom,
  });

  const params = {
    STYLE: layer.server_style ? layer.server_style : "",
    LEGEND_OPTIONS: "forceTitles:off;forceLabels:on;fontAntiAliasing:true",
  };

  const resolution = getPointResolution(view.getProjection(), view.getResolution(), view.getCenter());
  const url = wmsSource.getLegendUrl(resolution, params);

  if (!layerRequiresAuthentication(layer)) {
    return { url: url, error: error };
  }

  try {
    const result = await fetch(url, getFetchParameters(layer, user));

    if (result.ok) {
      const blob = await result.blob();
      legendImage = URL.createObjectURL(blob);
    } else {
      error = true;
    }
  } catch (e) {
    error = true;
  }

  return { url: legendImage, error: error };
};
