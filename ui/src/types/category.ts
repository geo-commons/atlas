export interface IParentCategory {
  id: string;
  title: string;
  slug: string;
}

export interface ICategory {
  id: string;
  title: string;
  slug: string;
  ordering?: number;
  parent: IParentCategory | null;
  full_title: string;
}
