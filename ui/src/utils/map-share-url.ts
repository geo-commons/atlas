import type { ILayer } from "@/types/layer";
import type { IPosition } from "@/types/map";
import { buildMapStatePath } from "@/utils/map-url-utils";

interface IMapShareUrlOptions {
  origin: string;
  /**
   * ID of the map to build a share URL for.
   * Use "primary" for the main map. Other map IDs are encoded into `/atlas/maps/:mapId/`.
   */
  mapId: string;
  position: IPosition;
  layers: ILayer[];
  drawing?: string | null;
  isEmbed?: boolean;
}

export const getMapShareUrl = ({ origin, mapId, position, layers, drawing, isEmbed }: IMapShareUrlOptions): string => {
  const baseLayer = layers.filter((layer) => layer.is_visible && layer.is_base).map((layer) => layer.id);
  const visibleLayers = layers.filter((layer) => layer.is_visible && !layer.is_base);
  const urlPrefix = mapId !== "primary" ? `/atlas/maps/${encodeURIComponent(mapId)}/` : "/atlas/";

  return buildMapStatePath({
    basePath: `${encodeURI(origin)}${urlPrefix}`,
    position,
    baseLayerId: baseLayer.length > 0 ? baseLayer[0] : null,
    visibleLayerIds: visibleLayers.map((layer) => layer.id),
    drawing,
    isEmbed,
  });
};
