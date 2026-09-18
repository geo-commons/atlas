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

  it("parses the PDOK BAG pand schema and excludes its geometry property", () => {
    const properties = parseWfsDescribeFeatureType(
      "bag:pand",
      `<?xml version="1.0" encoding="UTF-8" ?>
      <schema
        targetNamespace="http://bag.geonovum.nl"
        xmlns:bag="http://bag.geonovum.nl"
        xmlns:xsd="http://www.w3.org/2001/XMLSchema"
        xmlns="http://www.w3.org/2001/XMLSchema"
        xmlns:gml="http://www.opengis.net/gml/3.2"
        elementFormDefault="qualified"
        version="0.1"
      >
        <import
          namespace="http://www.opengis.net/gml/3.2"
          schemaLocation="http://schemas.opengis.net/gml/3.2.1/gml.xsd"
        />
        <element name="pand" type="bag:pandType" substitutionGroup="gml:AbstractFeature" />
        <complexType name="pandType">
          <complexContent>
            <extension base="gml:AbstractFeatureType">
              <sequence>
                <element name="geom" type="gml:GeometryPropertyType" minOccurs="0" maxOccurs="1" />
                <element name="identificatie" minOccurs="0" type="string" />
                <element name="rdf_seealso" minOccurs="0" type="string" />
                <element name="bouwjaar" minOccurs="0" type="long" />
                <element name="status" minOccurs="0" type="string" />
                <element name="gebruiksdoel" minOccurs="0" type="string" />
                <element name="oppervlakte_min" minOccurs="0" type="long" />
                <element name="oppervlakte_max" minOccurs="0" type="long" />
                <element name="aantal_verblijfsobjecten" minOccurs="0" type="long" />
                <element name="fuuid" minOccurs="0" type="string" />
              </sequence>
            </extension>
          </complexContent>
        </complexType>
      </schema>`,
    );

    expect(properties).toEqual([
      { name: "identificatie", type: "string" },
      { name: "rdf_seealso", type: "string" },
      { name: "bouwjaar", type: "int" },
      { name: "status", type: "string" },
      { name: "gebruiksdoel", type: "string" },
      { name: "oppervlakte_min", type: "int" },
      { name: "oppervlakte_max", type: "int" },
      { name: "aantal_verblijfsobjecten", type: "int" },
      { name: "fuuid", type: "string" },
    ]);
  });

  it("parses an xsd-prefixed GeoServer schema and excludes its geometry property", () => {
    const properties = parseWfsDescribeFeatureType(
      "topp:beheer_lichtmasten",
      `<?xml version="1.0" encoding="UTF-8"?>
      <xsd:schema
        xmlns:gml="http://www.opengis.net/gml/3.2"
        xmlns:topp="http://datalab.purmerend.nl/omgevingen"
        xmlns:wfs="http://www.opengis.net/wfs/2.0"
        xmlns:xsd="http://www.w3.org/2001/XMLSchema"
        elementFormDefault="qualified"
        targetNamespace="http://datalab.purmerend.nl/omgevingen"
      >
        <xsd:import
          namespace="http://www.opengis.net/gml/3.2"
          schemaLocation="https://datalab.purmerend.nl/geoserver/schemas/gml/3.2.1/gml.xsd"
        />
        <xsd:complexType name="beheer_lichtmastenType">
          <xsd:complexContent>
            <xsd:extension base="gml:AbstractFeatureType">
              <xsd:sequence>
                <xsd:element maxOccurs="1" minOccurs="0" name="lichtmast_id" nillable="true" type="xsd:string" />
                <xsd:element maxOccurs="1" minOccurs="0" name="status" nillable="true" type="xsd:string" />
                <xsd:element maxOccurs="1" minOccurs="0" name="eigenaar" nillable="true" type="xsd:string" />
                <xsd:element maxOccurs="1" minOccurs="0" name="pkey" nillable="true" type="xsd:int" />
                <xsd:element maxOccurs="1" minOccurs="0" name="geom" nillable="true" type="gml:GeometryPropertyType" />
              </xsd:sequence>
            </xsd:extension>
          </xsd:complexContent>
        </xsd:complexType>
        <xsd:element
          name="beheer_lichtmasten"
          substitutionGroup="gml:AbstractFeature"
          type="topp:beheer_lichtmastenType"
        />
      </xsd:schema>`,
    );

    expect(properties).toEqual([
      { name: "lichtmast_id", type: "string" },
      { name: "status", type: "string" },
      { name: "eigenaar", type: "string" },
      { name: "pkey", type: "int" },
    ]);
  });

  it("returns no properties when the feature type is absent from the schema", () => {
    expect(parseWfsDescribeFeatureType("bag:pand", "<schema />")).toEqual([]);
  });
});
