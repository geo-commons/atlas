import { ELayerTypes, ILayer, ILayerProperties } from "@/types/layer";
import { getFetchParameters } from "@/utils/auth";
import { IUser } from "@/types/user";
import { IDescribeFeatureTypeResponse } from "@/types/geoserver";

const getWfsOrWFSWMSLayerProperties = async (layer: ILayer, user: IUser): Promise<ILayerProperties> => {
  if (layer.source_type !== ELayerTypes.WFS && layer.source_type !== ELayerTypes.WMS_WFS) {
    throw new Error(
      "We ondersteunen het ophalen van laag-eigenschappen alleen voor lagen met de bron_type WFS of WMS_WFS",
    );
  }

  const params = new URLSearchParams([
    ["service", "WFS"],
    ["version", "1.0.0"],
    ["request", "DescribeFeatureType"],
    ["typename", layer.name],
    ["outputFormat", "application/json"],
  ]);

  try {
    const url = new URL(layer.url);
    url.search = params.toString();

    const result = await fetch(url.toString(), getFetchParameters(layer, user));

    const data: IDescribeFeatureTypeResponse = await result.json();

    return data.featureTypes.length ? data.featureTypes[0].properties : [];
  } catch (e: unknown) {
    if (e instanceof Error) {
      switch (e.name) {
        case "TypeError":
          throw new Error("Er ging iets mis bij het ophalen van de laag-eigenschappen van de server");
        case "SyntaxError":
          throw new Error("GeoServer heeft een ongeldig formaat data voor de laag-eigenschappen gestuurd");
        default:
          throw new Error("Er ging iets mis met het ophalen van de laag-eigenschappen");
      }
    } else {
      throw new Error("Onbekende fout opgetreden");
    }
  }
};

export { getWfsOrWFSWMSLayerProperties };
