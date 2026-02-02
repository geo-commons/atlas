import TileWMS from "ol/source/TileWMS";
import Projection from "ol/proj/Projection";
import View from "ol/View";
import { getFetchParameters, layerRequiresAuthentication } from "@/utils/auth";
import { getPointResolution } from "ol/proj";
import { ELayerTypes, ILayer } from "@/types/layer";
import { IUser } from "@/types/user";
import { IPosition } from "@/types/map";

export interface ILegendResult {
  url: string | null;
  error: boolean;
}

/* WMTS Capabilities Parser */
const getWmtsLegendFromCapabilities = async (layer: ILayer, user: IUser): Promise<string | null> => {
  const capabilitiesUrl = `${layer.url}?SERVICE=WMTS&REQUEST=GetCapabilities`;

  const fetchOptions = layerRequiresAuthentication(layer) ? getFetchParameters(layer, user) : undefined;

  const res = await fetch(capabilitiesUrl, fetchOptions);
  if (!res.ok) throw new Error("Failed to fetch WMTS GetCapabilities");

  const xmlText = await res.text();
  const parser = new DOMParser();
  const xml = parser.parseFromString(xmlText, "text/xml");

  const layers = [...xml.getElementsByTagName("Layer")];

  const targetLayer = layers.find((l) => {
    const idNode = l.getElementsByTagName("ows:Identifier")[0];
    return idNode?.textContent === layer.name;
  });

  if (!targetLayer) return null;

  const legendNode =
    targetLayer.getElementsByTagName("LegendURL")[0] || targetLayer.getElementsByTagNameNS("*", "LegendURL")[0];

  if (!legendNode) return null;

  const href =
    legendNode.getAttribute("xlink:href") ||
    legendNode.getAttributeNS("http://www.w3.org/1999/xlink", "href") ||
    legendNode.getElementsByTagName("OnlineResource")[0]?.getAttribute("xlink:href");

  return href || null;
};

export const fetchLegendImage = async (layer: ILayer, position: IPosition, user: IUser): Promise<ILegendResult> => {
  let legendImage: string | null = null;
  let error = false;
  let url: string | null = null;

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

  /* WMS legends */
  if (layer.source_type === ELayerTypes.WMS || layer.source_type === ELayerTypes.WMS_WFS) {
    const wmsSource = new TileWMS({
      url: layer.url,
      serverType: layer.server_type as any,
      params: {
        LAYERS: layer.name,
        TILED: true,
      },
    });

    const params = {
      STYLE: layer.server_style || "",
      LEGEND_OPTIONS: "forceTitles:off;forceLabels:on;fontAntiAliasing:true",
    };

    const resolution = getPointResolution(view.getProjection()!, view.getResolution()!, view.getCenter()!);

    url = wmsSource.getLegendUrl(resolution, params) || null;
  }

  /* WMTS legends */
  if (layer.source_type === ELayerTypes.WMTS) {
    try {
      url = await getWmtsLegendFromCapabilities(layer, user);
      if (!url) error = true;
    } catch {
      error = true;
    }
  }

  if (!layerRequiresAuthentication(layer)) {
    return { url: url, error: error };
  }

  try {
    const result = await fetch(url!, getFetchParameters(layer, user));

    if (result.ok) {
      const blob = await result.blob();
      legendImage = URL.createObjectURL(blob);
    } else {
      error = true;
    }
  } catch {
    error = true;
  }

  return { url: legendImage, error: error };
};
