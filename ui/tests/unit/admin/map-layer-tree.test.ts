import { describe, expect, it } from "vitest";

import {
  addLayerToCategoryTree,
  buildCategoryTree,
  flattenCategoryTreeLayers,
  removeBaseLayersFromCategoryTree,
  removeLayerFromCategoryTree,
} from "@/utils/map-layer-tree";

import type { IAdminLayer, ICategoryTreeNode, IMapLayerConfig } from "@/types/map-layer-tree";
import type { ICategory } from "@/types/category";

const parentCategory: ICategory = {
  id: "parent",
  title: "Parent",
  ordering: 1,
  parent: null,
  slug: "parent",
  full_title: "Parent",
};

const subCategory: ICategory = {
  id: "sub",
  title: "Sub",
  ordering: 2,
  parent: parentCategory,
  slug: "sub",
  full_title: "Parent / Sub",
};

const regularLayer: IAdminLayer = {
  id: 1,
  title: "Regular layer",
  category: parentCategory,
} as IAdminLayer;

const baseLayer: IAdminLayer = {
  id: 2,
  title: "Base layer",
  category: parentCategory,
} as IAdminLayer;

const subcategoryBaseLayer: IAdminLayer = {
  id: 3,
  title: "Subcategory base layer",
  category: subCategory,
} as IAdminLayer;

describe("mapLayerTree", () => {
  it("removes base layers and empty parent categories", () => {
    const tree: ICategoryTreeNode[] = [
      {
        id: parentCategory.id,
        title: parentCategory.title,
        ordering: 1,
        layers: [baseLayer],
        subcategories: [],
      },
    ];
    const configs: IMapLayerConfig[] = [{ layer: baseLayer.id, settings: { customSettings: true }, is_base: true }];

    expect(removeBaseLayersFromCategoryTree(tree, configs)).toEqual([]);
  });

  it("removes empty subcategories when a base layer is removed", () => {
    const tree: ICategoryTreeNode[] = [
      {
        id: parentCategory.id,
        title: parentCategory.title,
        ordering: 1,
        layers: [regularLayer],
        subcategories: [
          {
            id: subCategory.id,
            title: subCategory.title,
            ordering: 2,
            layers: [subcategoryBaseLayer],
          },
        ],
      },
    ];

    expect(removeLayerFromCategoryTree(tree, subcategoryBaseLayer.id)).toEqual([
      {
        id: parentCategory.id,
        title: parentCategory.title,
        ordering: 1,
        layers: [regularLayer],
        subcategories: [],
      },
    ]);
  });

  it("adds a layer back to its subcategory", () => {
    const tree: ICategoryTreeNode[] = [
      {
        id: parentCategory.id,
        title: parentCategory.title,
        ordering: 1,
        layers: [],
        subcategories: [],
      },
    ];

    expect(addLayerToCategoryTree(tree, [parentCategory, subCategory], subcategoryBaseLayer)).toEqual([
      {
        id: parentCategory.id,
        title: parentCategory.title,
        ordering: 1,
        layers: [],
        subcategories: [
          {
            id: subCategory.id,
            slug: subCategory.slug,
            title: subCategory.title,
            ordering: 2,
            layers: [subcategoryBaseLayer],
          },
        ],
      },
    ]);
  });

  it("sorts layers by map layer ordering using internal ids", () => {
    const firstLayer = {
      id: "first-layer",
      internal_id: 10,
      title: "First layer",
      category: parentCategory,
    } as IAdminLayer;
    const secondLayer = {
      id: "second-layer",
      internal_id: 20,
      title: "Second layer",
      category: parentCategory,
    } as IAdminLayer;

    const tree = buildCategoryTree(
      [firstLayer, secondLayer],
      [parentCategory],
      [{ category: parentCategory.id, title: parentCategory.title, ordering: 0 }],
      new Map([
        [10, 1],
        [20, 0],
      ]),
    );

    expect(tree[0].layers.map((layer) => layer.id)).toEqual(["second-layer", "first-layer"]);
  });

  it("flattens direct category layers before subcategory layers", () => {
    const subcategoryLayer = {
      id: 4,
      title: "Subcategory layer",
      category: subCategory,
    } as IAdminLayer;
    const tree: ICategoryTreeNode[] = [
      {
        id: parentCategory.id,
        title: parentCategory.title,
        ordering: 1,
        layers: [regularLayer],
        subcategories: [
          {
            id: subCategory.id,
            title: subCategory.title,
            ordering: 2,
            layers: [subcategoryLayer],
          },
        ],
      },
    ];

    expect(flattenCategoryTreeLayers(tree).map((layer) => layer.id)).toEqual([regularLayer.id, subcategoryLayer.id]);
  });
});
