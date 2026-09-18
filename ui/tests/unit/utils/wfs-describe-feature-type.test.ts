import { DOMParser } from "@xmldom/xmldom";
import { beforeAll, describe, expect, it } from "vitest";
import { parseWfsDescribeFeatureType } from "@/utils/wfs-describe-feature-type";

beforeAll(() => {
  Object.assign(globalThis, { DOMParser });
});

describe("parseWfsDescribeFeatureType", () => {
  it("extracts filterable properties and converts their XML Schema types", () => {
    const properties = parseWfsDescribeFeatureType(
      "bag:pand",
      `<schema xmlns="http://www.w3.org/2001/XMLSchema" xmlns:gml="http://www.opengis.net/gml/3.2">
        <complexType name="pandType"><sequence>
          <element name="geom" type="gml:GeometryPropertyType" />
          <element name="bouwjaar" type="long" />
          <element name="registratiedatum" type="dateTime" />
          <element name="status" type="string" />
        </sequence></complexType>
      </schema>`,
    );

    expect(properties).toEqual([
      { name: "bouwjaar", type: "int" },
      { name: "registratiedatum", type: "date-time" },
      { name: "status", type: "string" },
    ]);
  });

  it("returns no properties when the feature type is absent from the schema", () => {
    expect(parseWfsDescribeFeatureType("bag:pand", "<schema />")).toEqual([]);
  });
});
