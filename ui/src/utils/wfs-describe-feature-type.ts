export type TWfsFilterPropertyType = "int" | "number" | "date" | "date-time" | "time" | "string";

export interface IWfsFeatureProperty {
  name: string;
  type: TWfsFilterPropertyType;
}

/**
 * Converts an XML Schema property type to the filter type used by the table controls.
 * @param type - The XML Schema type from a DescribeFeatureType element.
 * @returns The matching table filter type.
 */
const getWfsFilterPropertyType = (type: string): TWfsFilterPropertyType => {
  const normalizedType = type.toLowerCase().replace(/^(xsd|xs):/, "");
  if (["byte", "short", "int", "integer", "long"].includes(normalizedType)) return "int";
  if (["decimal", "double", "float"].includes(normalizedType)) return "number";
  if (normalizedType === "date") return "date";
  if (normalizedType === "datetime") return "date-time";
  if (normalizedType === "time") return "time";
  return "string";
};

/**
 * Parses a WFS DescribeFeatureType XML response for a specific feature type.
 * @param layerName - The WFS feature type name, optionally including its namespace prefix.
 * @param xml - The DescribeFeatureType XML response body.
 * @returns The non-geometry properties and their table filter types.
 */
export const parseWfsDescribeFeatureType = (layerName: string, xml: string): IWfsFeatureProperty[] => {
  const schema = new DOMParser().parseFromString(xml, "application/xml");
  const typeName = layerName.split(":").pop();
  const complexType = Array.from(schema.getElementsByTagNameNS("*", "complexType")).find(
    (element) => element.getAttribute("name") === `${typeName}Type`,
  );
  if (!complexType) return [];

  return Array.from(complexType.getElementsByTagNameNS("*", "element"))
    .map((element) => ({ name: element.getAttribute("name"), type: element.getAttribute("type") || "string" }))
    .filter(
      (property): property is { name: string; type: string } =>
        property.name !== null && !property.type.startsWith("gml:"),
    )
    .map(({ name, type }) => ({ name, type: getWfsFilterPropertyType(type) }));
};
