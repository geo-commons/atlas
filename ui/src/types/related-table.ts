import { ISource } from "@/types/source";

export enum SourceType {
  OWS = "OWS",
  WMTS = "WMTS",
  REST = "REST",
}

export interface IRelatedTable {
  id: number;
  title: string;
  slug: string;
  source: ISource;
  source_type: SourceType;
  fields: string[];
  list_endpoint: string;
  detail_endpoint: string;
  layer_name: string;
  list_cql_filters: string[];
  detail_cql_filters: string | null;
  related_tables: IRelatedTable[] | null;
  field_mapping: Record<string, string>;
}
