import { defineQuery, useQuery } from "@pinia/colada";
import { apiFetch, getAllObjects } from "@/utils/api-helpers";
import { ref } from "vue";

export const useSourceList = defineQuery(() => {
  const { state, ...rest } = useQuery({
    key: () => ["sources"],
    query: async () => {
      const url = getAllObjects("/atlas/api/v1/sources/");
      const res = await (await apiFetch(url)).json();
      return res.results.map((source: any) => ({
        id: source.id,
        label: source.title,
        url: source.url,
        type: source.source_type,
      }));
    },
  });
  return {
    ...rest,
    sourcesState: state,
  };
});

export const useGroupList = defineQuery(() => {
  const { state, ...rest } = useQuery({
    key: () => ["groups"],
    query: async () => {
      const url = getAllObjects("/atlas/api/v1/groups/");
      const res = await (await apiFetch(url)).json();
      return res.results;
    },
  });
  return {
    ...rest,
    groupsState: state,
  };
});

export const useLayerList = defineQuery(() => {
  const search = ref("");
  const { state, ...rest } = useQuery({
    key: () => ["layers"],
    query: async () => {
      const url = getAllObjects("/atlas/api/v1/layers/");
      const res = await (await apiFetch(url)).json();
      return res.results
        .filter((layer: any) => layer.metadataset?.id === parseInt(search.value))
        .map((layer: any) => ({
          id: parseInt(layer.id),
          name: layer.title,
        }));
    },
  });
  return {
    ...rest,
    layersState: state,
    layersSearch: search,
  };
});

export const useMetadatasetList = defineQuery(() => {
  const { state, ...rest } = useQuery({
    key: () => ["metadata"],
    query: async () => {
      const url = getAllObjects("/atlas/api/v1/metadatasets/");
      const res = await (await apiFetch(url)).json();
      return res.results.map((metadataset: any) => ({
        id: metadataset.id,
        label: metadataset.title,
        value: metadataset.id,
        organization: metadataset.organization,
        description: metadataset.description,
        last_updated: metadataset.last_updated,
        update_frequency: metadataset.update_frequency,
        responsible_email_internal: metadataset.responsible_email_internal,
      }));
    },
  });
  return {
    ...rest,
    metadatasetsState: state,
  };
});

export const useCategoryList = defineQuery(() => {
  const { state, ...rest } = useQuery({
    key: () => ["categories"],
    query: async () => {
      const url = getAllObjects("/atlas/api/v1/categories/");
      const res = await (await apiFetch(url)).json();
      return res.results.map((category: any) => ({
        id: category.id,
        label: category.title,
        fullTitle: category.full_title,
      }));
    },
  });
  return {
    ...rest,
    categoriesState: state,
  };
});

export const useTableList = defineQuery(() => {
  const { state, ...rest } = useQuery({
    key: () => ["tables"],
    query: async () => {
      const url = getAllObjects("/atlas/api/v1/tables/");
      const res = await (await apiFetch(url)).json();
      return res.results;
    },
  });
  return {
    ...rest,
    tablesState: state,
  };
});
