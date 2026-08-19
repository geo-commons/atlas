import type {
  CategoryId,
  IAdminLayer,
  ICategoryTreeNode,
  IMapCategoryConfig,
  IMapLayerConfig,
  LayerId,
} from "@/types/map-layer-tree";
import type { ICategory, IParentCategory } from "@/types/category";

// Helpers for building and updating the nested map layer category tree used by the admin map editor and the layers panel.

export const matchesLayerSearch = (layer: IAdminLayer, searchTerm: string): boolean => {
  const matchesLayerTitle = layer.title.toLowerCase().includes(searchTerm);
  const matchesLayerDescription = layer.description?.toLowerCase().includes(searchTerm) || false;
  const matchesLayerSearchTerms =
    layer.search_terms?.some((term) => term.trim().toLowerCase().includes(searchTerm)) || false;
  const matchesMetadatasetTitle = layer.metadataset?.title.toLowerCase().includes(searchTerm);
  const matchesMetadatasetAbstract = layer.metadataset?.abstract?.toLowerCase().includes(searchTerm) || false;
  const metadatasetKeywords = layer.metadataset?.keyword ? layer.metadataset.keyword.split(/\r?\n/) : [];
  const matchesMetadatasetKeywords = metadatasetKeywords.some((term) => term.trim().toLowerCase().includes(searchTerm));

  return (
    matchesLayerTitle ||
    matchesLayerDescription ||
    matchesLayerSearchTerms ||
    matchesMetadatasetTitle ||
    matchesMetadatasetAbstract ||
    matchesMetadatasetKeywords
  );
};

const resolveCategory = (
  categoryById: Map<CategoryId, ICategory>,
  category?: ICategory | IParentCategory | null,
): ICategory | null => {
  if (!category) {
    return null;
  }

  return categoryById.get(category.id) || (category as ICategory);
};

const getCategoryOrdering = (
  mapCategoryByCategoryId: Map<CategoryId, IMapCategoryConfig>,
  category: ICategory,
): number => {
  const mapCategory = mapCategoryByCategoryId.get(category.id);
  return mapCategory?.ordering ?? category.ordering ?? Number.MAX_SAFE_INTEGER;
};

export const getTreeLayerId = (layer: IAdminLayer): LayerId => {
  return layer.internal_id ?? layer.id;
};

const getLayerOrdering = (layer: IAdminLayer, orderingByLayerId?: Map<LayerId, number>): number => {
  return orderingByLayerId?.get(getTreeLayerId(layer)) ?? layer.ordering ?? Number.MAX_SAFE_INTEGER;
};

const sortTreeLayers = (layers: IAdminLayer[], orderingByLayerId?: Map<LayerId, number>): IAdminLayer[] => {
  return [...layers].sort((layerA, layerB) => {
    const orderingA = getLayerOrdering(layerA, orderingByLayerId);
    const orderingB = getLayerOrdering(layerB, orderingByLayerId);

    if (orderingA !== orderingB) {
      return orderingA - orderingB;
    }

    return layerA.title.localeCompare(layerB.title);
  });
};

export const isBaseLayerConfig = (config: IMapLayerConfig): boolean => {
  return Boolean(config.settings.is_base);
};

export const removeLayerFromCategoryTree = (
  categoryTree: ICategoryTreeNode[],
  layerId: LayerId,
): ICategoryTreeNode[] => {
  return categoryTree.flatMap((category) => {
    const layers = category.layers.filter((selectedLayer) => getTreeLayerId(selectedLayer) !== layerId);
    const subcategories = category.subcategories.flatMap((subcategory) => {
      const subcategoryLayers = subcategory.layers.filter((selectedLayer) => getTreeLayerId(selectedLayer) !== layerId);

      if (subcategoryLayers.length === 0) {
        return [];
      }

      return [
        {
          ...subcategory,
          layers: subcategoryLayers,
        },
      ];
    });

    if (layers.length === 0 && subcategories.length === 0) {
      return [];
    }

    return [
      {
        ...category,
        layers,
        subcategories,
      },
    ];
  });
};

export const addLayerToCategoryTree = (
  categoryTree: ICategoryTreeNode[],
  allCategories: ICategory[],
  layer: IAdminLayer,
): ICategoryTreeNode[] => {
  const layerCategory = layer.category;
  if (!layerCategory) {
    return categoryTree;
  }

  const layerId = getTreeLayerId(layer);
  const layerExists = categoryTree.some(
    (category) =>
      category.layers.some((item) => getTreeLayerId(item) === layerId) ||
      category.subcategories.some((subcategory) => subcategory.layers.some((item) => getTreeLayerId(item) === layerId)),
  );

  if (layerExists) {
    return categoryTree;
  }

  const parentCategory = layerCategory.parent
    ? (allCategories.find((category) => category.id === layerCategory.parent?.id) ?? layerCategory.parent)
    : layerCategory;
  const parentCategoryOrdering = allCategories.find((category) => category.id === parentCategory.id)?.ordering;

  const parentIndex = categoryTree.findIndex((category) => category.id === parentCategory.id);
  const parentNode: ICategoryTreeNode =
    parentIndex >= 0
      ? categoryTree[parentIndex]
      : {
          id: parentCategory.id,
          title: parentCategory.title,
          slug: parentCategory.slug,
          ordering: parentCategoryOrdering ?? categoryTree.length,
          layers: [],
          subcategories: [],
        };

  const nextParentNode: ICategoryTreeNode = layerCategory.parent
    ? {
        ...parentNode,
        subcategories: addLayerToSubcategory(parentNode.subcategories, allCategories, layerCategory, layer),
      }
    : {
        ...parentNode,
        layers: [...parentNode.layers, layer],
      };

  if (parentIndex >= 0) {
    return categoryTree.map((category) => (category.id === parentCategory.id ? nextParentNode : category));
  }

  return [...categoryTree, nextParentNode];
};

const addLayerToSubcategory = (
  subcategories: ICategoryTreeNode["subcategories"],
  allCategories: ICategory[],
  layerCategory: ICategory,
  layer: IAdminLayer,
): ICategoryTreeNode["subcategories"] => {
  const subcategoryIndex = subcategories.findIndex((subcategory) => subcategory.id === layerCategory.id);

  if (subcategoryIndex < 0) {
    const categoryOrdering = allCategories.find((category) => category.id === layerCategory.id)?.ordering;

    return [
      ...subcategories,
      {
        id: layerCategory.id,
        title: layerCategory.title,
        slug: layerCategory.slug,
        ordering: categoryOrdering ?? subcategories.length,
        layers: [layer],
      },
    ];
  }

  return subcategories.map((subcategory) => {
    if (subcategory.id !== layerCategory.id) {
      return subcategory;
    }

    return {
      ...subcategory,
      layers: [...subcategory.layers, layer],
    };
  });
};

export const removeBaseLayersFromCategoryTree = (
  categoryTree: ICategoryTreeNode[],
  mapLayerConfigs: IMapLayerConfig[],
): ICategoryTreeNode[] => {
  const baseLayerIds = new Set(
    mapLayerConfigs.filter((config) => isBaseLayerConfig(config)).map((config) => config.layer),
  );

  return [...baseLayerIds].reduce((tree, layerId) => removeLayerFromCategoryTree(tree, layerId), categoryTree);
};

export const buildCategoryTree = (
  layers: IAdminLayer[],
  allCategories: ICategory[],
  mapCategories: IMapCategoryConfig[] = [],
  orderingByLayerId?: Map<LayerId, number>,
): ICategoryTreeNode[] => {
  const categories = new Map<CategoryId, ICategoryTreeNode>();
  const categoryById = new Map<CategoryId, ICategory>(allCategories.map((category) => [category.id, category]));
  const mapCategoryByCategoryId = new Map<CategoryId, IMapCategoryConfig>(
    mapCategories.map((category) => [category.category, category]),
  );

  layers.forEach((layer) => {
    const resolvedCategory = resolveCategory(categoryById, layer.category);
    if (!resolvedCategory) {
      return;
    }

    const parentCategory = resolvedCategory.parent
      ? resolveCategory(categoryById, categoryById.get(resolvedCategory.parent.id) || resolvedCategory.parent)
      : resolvedCategory;

    if (!parentCategory) {
      return;
    }

    const parentNode = categories.get(parentCategory.id) || {
      id: parentCategory.id,
      title: parentCategory.title,
      slug: parentCategory.slug,
      ordering: getCategoryOrdering(mapCategoryByCategoryId, parentCategory),
      layers: [],
      subcategories: [],
    };

    categories.set(parentCategory.id, parentNode);

    if (!resolvedCategory.parent) {
      parentNode.layers.push(layer);
      return;
    }

    let subcategoryNode = parentNode.subcategories.find((subcategory) => subcategory.id === resolvedCategory.id);

    if (!subcategoryNode) {
      subcategoryNode = {
        id: resolvedCategory.id,
        title: resolvedCategory.title,
        slug: resolvedCategory.slug,
        ordering: getCategoryOrdering(mapCategoryByCategoryId, resolvedCategory),
        layers: [],
      };
      parentNode.subcategories.push(subcategoryNode);
    }

    subcategoryNode.layers.push(layer);
  });

  return [...categories.values()]
    .map((category) => ({
      ...category,
      layers: sortTreeLayers(category.layers, orderingByLayerId),
      subcategories: [...category.subcategories]
        .map((subcategory) => ({
          ...subcategory,
          layers: sortTreeLayers(subcategory.layers, orderingByLayerId),
        }))
        .sort((subcategoryA, subcategoryB) => {
          if (subcategoryA.ordering !== subcategoryB.ordering) {
            return subcategoryA.ordering - subcategoryB.ordering;
          }

          return subcategoryA.title.localeCompare(subcategoryB.title);
        }),
    }))
    .sort((categoryA, categoryB) => {
      if (categoryA.ordering !== categoryB.ordering) {
        return categoryA.ordering - categoryB.ordering;
      }

      return categoryA.title.localeCompare(categoryB.title);
    });
};

export const flattenCategoryTreeLayers = (categoryTree: ICategoryTreeNode[]): IAdminLayer[] => {
  return categoryTree.flatMap((category) => [
    ...category.layers,
    ...category.subcategories.flatMap((subcategory) => subcategory.layers),
  ]);
};
