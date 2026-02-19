export interface IMetadatasetLayer {
  slug: string;
  title: string;
}

export interface IMetadataset {
  id: number;
  title: string;
  slug?: string;
  layers?: IMetadatasetLayer[];
  description?: string;
  abstract: string;
  topic_category: string;
  keyword: string;
  statement: string;
  source_origin: string;
  source_location?: string;
  source_name_internal?: string;
  source_email_internal?: string;
  source_organization: string;
  source_name_public?: string;
  source_email_public: string;
  source_email_person_responsible?: string;
  source_role_person_responsible: string;
  update_method?: string;
  update_frequency: string;
  last_updated: string | null;
  authorization_level?: string;
  status: string;
  show_in_overview: boolean;
  access_constraints: string | null;
  other_constraints: string | null;
  usage_constraints: string | null;
  meta_email_internal?: string;
  meta_organization: string;
  meta_email_person_responsible: string;
  meta_role_person_responsible: string;
}

// Helper type for metadataset form options
export interface IMetadatasetOption {
  id: string;
  label: string;
  value: number;
  organization?: string;
  description?: string;
  last_updated?: string;
  update_frequency?: string;
  responsible_email_internal?: string;
}
