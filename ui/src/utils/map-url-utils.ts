import type { IConfigPosition } from "@/types/ConfigType";
import { ILayer } from "@/types/layer";
import { IPosition } from "@/types/map";

interface IMapStatePathOptions {
  position: IPosition;
  baseLayerId?: string | null;
  visibleLayerIds: string[];
  drawing?: string | null;
  isEmbed?: boolean;
}

export const getMapPositionPath = (position: IPosition): string => {
  const x = encodeURIComponent(position.center[0].toFixed(2));
  const y = encodeURIComponent(position.center[1].toFixed(2));

  return `@${x},${y},${Math.round(position.zoom * 100) / 100}z`;
};

export const buildMapStatePath = ({
  basePath,
  position,
  baseLayerId,
  visibleLayerIds,
  drawing,
  isEmbed,
}: IMapStatePathOptions & { basePath: string }): string => {
  const markerCoords = position.marker?.map((coord) => encodeURIComponent(coord.toFixed(2)));
  const urlParts = [
    `${basePath}${getMapPositionPath(position)}`,
    `layers=${visibleLayerIds.map((layerId) => encodeURIComponent(layerId)).join(",")}`,
    `base=${baseLayerId ? encodeURIComponent(baseLayerId) : ""}`,
  ];

  if (drawing) {
    urlParts.push(`drawing=${encodeURIComponent(drawing)}`);
  }

  if (markerCoords?.length === 2) {
    urlParts.push(`marker=${markerCoords.join(",")}`);
  }

  if (isEmbed) {
    urlParts.push("is_embed=true");
  }

  return urlParts.join("/");
};

export const pushHistoryState = (
  position: IPosition,
  baseLayer: ILayer,
  visibleLayers: ILayer[],
  drawing?: string,
  isEmbed?: boolean,
): void => {
  const basePath = /(.*?)(@|$)/.exec(window.location.pathname);

  if (!basePath) {
    return;
  }

  window.history.replaceState(
    {},
    "",
    buildMapStatePath({
      basePath: basePath[1],
      position,
      baseLayerId: baseLayer?.id,
      visibleLayerIds: visibleLayers.map((layer) => layer.id),
      drawing,
      isEmbed,
    }),
  );
};

/**
 * Build a URL to the atlas map with the given layer IDs visible.
 * Uses Atlas path format (@x,y,zoomz/layers=...) with configured municipality center.
 * Layer IDs are layer slugs from the API.
 */
export const getMapUrlWithLayers = (layerIds: string[], position: IConfigPosition): string => {
  const { center, zoom } = position;
  const pos = `@${center.x.toFixed(2)},${center.y.toFixed(2)},${Math.round(zoom * 100) / 100}z`;
  return `${window.location.origin}/atlas/${pos}/layers=${layerIds.map(encodeURIComponent).join(",")}`;
};
