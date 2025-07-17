import { ILayer } from "@/types/layer";

export interface Position {
  center: [number, number];
  zoom: number;
  marker?: [number, number];
}

export function pushHistoryState(
  position: Position,
  baseLayer: ILayer,
  visibleLayers: ILayer[],
  drawing?: string,
): void {
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

  window.history.replaceState({}, "", urlParts.join("/"));
}
