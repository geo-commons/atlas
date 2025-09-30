export interface IMetadataset {
  id: number;
  title: string;
  slug?: string;
  description?: string;
  abstract: string;
  topic_category: string;
  keyword: string;
  statement: string;
  source_origin: string;
  source_location?: string;
  source_email_internal?: string;
  source_organization: string;
  source_email_public: string;
  source_email_person_responsible?: string;
  source_role_person_responsible: string;
  update_method?: string;
  update_frequency: string;
  last_updated: string;
  authorization_level?: string;
  status: string;
  show_in_overview: boolean;
  access_constraints: string;
  other_constraints: string;
  usage_constraints?: string;
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
