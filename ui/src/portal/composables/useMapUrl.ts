import { useGlobalStore } from "@/stores";
import { getMapUrlWithLayers } from "@/utils/map-url-utils";

export const useMapUrl = () => {
  const getMapUrl = (layerIds: string[]) => {
    const position = useGlobalStore().config?.position;
    return position ? getMapUrlWithLayers(layerIds, position) : `${window.location.origin}/atlas/`;
  };
  return { getMapUrl };
};
