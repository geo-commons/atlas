import { ILayerProperties } from "@/types/layer";

/**
 * GeoServer DescribeFeatureType response body type
 */
export interface IDescribeFeatureTypeResponse {
  elementFormDefault: string;
  featureTypes: Array<{
    properties: ILayerProperties;
    typeName: string;
  }>;
  targetNamespace: string;
  targetPrefix: string;
}
