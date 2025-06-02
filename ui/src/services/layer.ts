import { ELayerTypes, IFeatureProperties, ILayer } from "@/types/layer";
import { getFetchParameters } from "@/utils/auth";
import { IUser } from "@/types/user";
import { IDescribeFeatureTypeResponse, IFeatureTypes } from "@/types/geoserver";
import Feature from "ol/Feature";
import { WFS } from "ol/format";
import { parseGeoServerWfsTResponse } from "@/utils/parse-geoserver-responses";

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

/*
This function retrieves the geometry field name based on the featureTypes returned
from a DescribeFeatureType request to GeoServer.

If any property in the featureType has a type attribute that starts with "gml",
it indicates that the property is a geometry field.
*/
const getGeometryName = async (featureTypes: IFeatureTypes): Promise<string> => {
  if (!featureTypes || !featureTypes.length) {
    throw new Error("Wij konden de geometry naam niet ophalen");
  }

  const geometryFeatureProperties = featureTypes[0].properties.filter((featureTypeProperty) =>
    featureTypeProperty.type.startsWith("gml"),
  );

  return geometryFeatureProperties.length ? geometryFeatureProperties[0].name : "geometry";
};

const performWfsTransaction = async (
  layer: ILayer,
  features: { toInsert?: Feature[]; toUpdate?: Feature[]; toDelete?: Feature[] },
  featureProperties: IFeatureProperties,
  geometryName: string,
  user: IUser,
) => {
  if (layer.source_type !== ELayerTypes.WFS && layer.source_type !== ELayerTypes.WMS_WFS) {
    throw new Error("We ondersteunen alleen transacties voor lagen met bron_type WFS of WMS_WFS");
  }

  // The writeTransaction() method in OpenLayers (https://openlayers.org/en/latest/apidoc/module-ol_format_WFS-WFS.html)
  // supports multiple transactions at once. However, we have decided to limit it to performing only one operation at a time,
  // whether it's an insert, update, or delete.
  const { toInsert = [], toUpdate = [], toDelete = [] } = features;

  const transactionNode = new WFS().writeTransaction(toInsert, toUpdate, toDelete, {
    featureNS: featureProperties.targetNamespace,
    featurePrefix: featureProperties.targetPrefix,
    featureType: layer.name,
    srsName: layer.projection,
    nativeElements: [],
  });

  const serializer = new XMLSerializer();
  const payload = serializer.serializeToString(transactionNode).replaceAll("geometry", geometryName);
  const { headers: authHeaders } = getFetchParameters(layer, user);

  const response = await fetch(layer.url, {
    method: "POST",
    headers: {
      "Content-Type": "text/xml",
      ...authHeaders,
    },
    body: payload,
  });

  const { errorMessage, success } = await parseGeoServerWfsTResponse(response);

  if (!success) {
    throw new Error(errorMessage);
  }
};

// Performs a WFS-Transaction request to create a specific feature on a layer
const addFeatureOnLayer = async (
  layer: ILayer,
  feature: Feature,
  featureProperties: IFeatureProperties,
  geometryName: string,
  user: IUser
) => {
  await performWfsTransaction(layer, { toInsert: [feature] }, featureProperties, geometryName, user);
};

// Performs a WFS-Transaction request to update a specific feature on a layer
const editFeatureOnLayer = async (
  layer: ILayer,
  feature: Feature,
  featureProperties: IFeatureProperties,
  geometryName: string,
  user: IUser
) => {
  await performWfsTransaction(layer, { toUpdate: [feature] }, featureProperties, geometryName, user);
};

// Performs a WFS-Transaction request to delete a specific feature on a layer
const deleteFeatureOnLayer = async (
  layer: ILayer,
  feature: Feature,
  featureProperties: IFeatureProperties,
  geometryName: string,
  user: IUser
) => {
  await performWfsTransaction(layer, { toDelete: [feature] }, featureProperties, geometryName, user);
};

export {
  getWfsOrWFSWMSLayerFeatureInformation,
  getGeometryName,
  addFeatureOnLayer,
  editFeatureOnLayer,
  deleteFeatureOnLayer,
};
