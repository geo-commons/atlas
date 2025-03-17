import { ILayerProperties } from "@/types/layer";

/**
 * GeoServer DescribeFeatureType response body type
 */
export interface IDescribeFeatureTypeResponse {
  elementFormDefault: string;
  featureTypes: IFeatureTypes;
  targetNamespace: string;
  targetPrefix: string;
}

export type IFeatureTypes = Array<{
  properties: ILayerProperties;
  typeName: string;
}>;
