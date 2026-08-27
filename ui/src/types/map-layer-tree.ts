import type { ILayer } from "@/types/layer";
import type { ICategory } from "@/types/category";

export type LayerId = number | string;
export type CategoryId = string;

export interface IAdminLayer extends Omit<ILayer, "id"> {
  id: LayerId;
  internal_id?: LayerId;
  ordering?: number;
  search_terms?: string[];
  category: ICategory | null;
}

export interface IMapLayerSettings {
  customSettings?: boolean;
  [key: string]: unknown;
}

export interface IMapLayerConfig {
  layer: LayerId;
  settings: IMapLayerSettings;
  is_base?: boolean;
  is_visible?: boolean;
  map_category?: CategoryId | null;
  ordering?: number;
}

export interface IMapCategoryConfig {
  id?: CategoryId;
  category: CategoryId;
  title: string;
  ordering?: number;
}

export interface ISubcategoryTreeNode {
  id: CategoryId;
  title: string;
  slug?: string;
  ordering: number;
  layers: IAdminLayer[];
}

export interface ICategoryTreeNode {
  id: CategoryId;
  title: string;
  slug?: string;
  ordering: number;
  layers: IAdminLayer[];
  subcategories: ISubcategoryTreeNode[];
}

export interface IMapLayersData {
  layers: IMapLayerConfig[];
  categories?: IMapCategoryConfig[];
}
