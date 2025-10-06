import TileLayer from "ol/layer/Tile";
import Map from "ol/Map";
import { getRenderPixel } from "ol/render";
import { useMapStore } from "@/stores/map_store";

export const useCompareLayers = (
  map: Map,
  mapStore: ReturnType<typeof useMapStore>,
  tileLayer: TileLayer,
  id: string,
) => {
  /*
   * Note: currently it is only possible to compare WMS and WMTS layers, this is due to the implementation for Tile Layers being more straight forwards as Vector Layers.
   * Vector layers will be implemented in the future.
   * */

  // Function to handle the prerender event
  const handlePrerender = (event: any) => {
    if (!map) {
      return;
    }

    const swipeValue = mapStore.comparePercentage / 100;
    const ctx = event.context;
    const mapSize = map.getSize();

    if (!mapSize) {
      return;
    }

    const width = mapSize[0] * swipeValue;

    let tl, tr, bl, br;

    if (mapStore.leftSelectedCompareLayerId === id) {
      // Clipping region for left side
      tl = getRenderPixel(event, [0, 0]);
      tr = getRenderPixel(event, [width, 0]);
      bl = getRenderPixel(event, [0, mapSize[1]]);
      br = getRenderPixel(event, [width, mapSize[1]]);
    }

    if (mapStore.rightSelectedCompareLayerId === id) {
      // Clipping region for right side
      tl = getRenderPixel(event, [width, 0]);
      tr = getRenderPixel(event, [mapSize[0], 0]);
      bl = getRenderPixel(event, [width, mapSize[1]]);
      br = getRenderPixel(event, mapSize);
    }

    if (!tl || !tr || !bl || !br) {
      return;
    }

    ctx.save();
    ctx.beginPath();
    ctx.moveTo(tl[0], tl[1]);
    ctx.lineTo(bl[0], bl[1]);
    ctx.lineTo(br[0], br[1]);
    ctx.lineTo(tr[0], tr[1]);
    ctx.closePath();
    ctx.clip();
  };

  // Function to handle the postrender event
  const handlePostrender = (event: any) => {
    event.context.restore();
  };

  // Function to set up the swipe effect
  const setupSwipeEffect = () => {
    // Remove any existing event listeners
    tileLayer.un("prerender", handlePrerender);
    tileLayer.un("postrender", handlePostrender);

    // Add swipe effect only if the layer is involved in the comparison
    if (mapStore.leftSelectedCompareLayerId === id || mapStore.rightSelectedCompareLayerId === id) {
      tileLayer.on("prerender", handlePrerender);
      tileLayer.on("postrender", handlePostrender);
    }
  };

  return {
    handlePrerender,
    handlePostrender,
    setupSwipeEffect,
  };
};
