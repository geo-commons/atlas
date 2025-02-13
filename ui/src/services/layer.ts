import { ELayerTypes, IFeatureProperties, ILayer, ILayerProperties } from "@/types/layer";
import { getFetchParameters } from "@/utils/auth";
import { IUser } from "@/types/user";
import { IDescribeFeatureTypeResponse } from "@/types/geoserver";
import Feature from "ol/Feature";
import { WFS } from "ol/format";

const getWfsOrWFSWMSLayerFeatureInformation = async (
  layer: ILayer,
  user: IUser,
): Promise<IDescribeFeatureTypeResponse> => {
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

    return data;
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

const addFeatureToLayer = async (layer: ILayer, feature: Feature, featureProperties: IFeatureProperties) => {
  if (layer.source_type !== ELayerTypes.WFS && layer.source_type !== ELayerTypes.WMS_WFS) {
    throw new Error(
      "We ondersteunen het opslaan van een object op laag alleen voor lagen met bron_type WFS of WMS_WFS",
    );
  }

  const transactionNode = new WFS().writeTransaction([feature], [], [], {
    featureNS: featureProperties.targetNamespace,
    featurePrefix: featureProperties.targetPrefix,
    featureType: layer.name,
    srsName: layer.projection,
    nativeElements: [],
  });

  const serializer = new XMLSerializer();
  const payload = serializer.serializeToString(transactionNode);

  const result = await fetch(layer.url, {
    method: "POST",
    headers: {
      "Content-Type": "text/xml",
    },
    body: payload,
  });

  // TODO: ERROR HANDLING
  console.log(result);
};

export { getWfsOrWFSWMSLayerFeatureInformation, addFeatureToLayer };
