import type { IConfigPosition } from "@/types/ConfigType";
import { ILayer } from "@/types/layer";
import { IPosition } from "@/types/map";

export type Position = IPosition;

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

  const x = encodeURIComponent(position.center[0].toFixed(2));
  const y = encodeURIComponent(position.center[1].toFixed(2));

  const visibleLayerIds = visibleLayers.map((l) => l.id).join(",");

  const markerCoords = position?.marker?.map((coord) => encodeURIComponent(coord.toFixed(2)));

  const urlParts = [
    `${basePath[1]}@${x},${y},${Math.round(position.zoom * 100) / 100}z`,
    `layers=${visibleLayerIds}`,
    `base=${baseLayer?.id || ""}`,
  ];

  if (drawing) {
    urlParts.push(`drawing=${drawing}`);
  }

  if (markerCoords?.length === 2) {
    urlParts.push(`marker=${markerCoords.join(",")}`);
  }

  if (isEmbed) {
    urlParts.push(`is_embed=true`);
  }

  window.history.replaceState({}, "", urlParts.join("/"));
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
