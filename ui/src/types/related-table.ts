import { ISource } from "@/types/source";

export enum SourceType {
  OWS = "OWS",
  WMTS = "WMTS",
  REST = "REST",
}

export interface ICqlFilterEntry {
  key: string;
  cql_filter: string;
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
  list_property: string | null;
  detail_property: string | null;
  page_param: string | null;
  items_per_page_param: string | null;
  total_items_page_property: string | null;
  list_error_property: string | null;
  detail_error_property: string | null;
  layer_name: string;
  list_cql_filters: ICqlFilterEntry[];
  detail_cql_filters: ICqlFilterEntry[];
  related_tables: IRelatedTable[] | null;
  field_mapping: Record<string, string>;
  to_table: IRelatedTable;
  list_display_properties: string[];
  detail_display_properties: string[];
}
