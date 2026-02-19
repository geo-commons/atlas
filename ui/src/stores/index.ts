import { defineStore } from "pinia";
import type { IConfig } from "@/types/ConfigType";
import type { IUser } from "@/types/user";
import type { ILayer } from "@/types/layer";

export interface PortalAvailableLinks {
  maps: boolean;
  metadatasets: boolean;
  tables: boolean;
}

export const DEFAULT_PORTAL_AVAILABLE_LINKS: PortalAvailableLinks = {
  maps: false,
  metadatasets: false,
  tables: false,
};

export interface IGlobalStoreState {
  position: any;
  layers: ILayer[];
  tool: any;
  selectedArea: any;
  searchQuery: any;
  alert: any;
  user: IUser | null;
  drawing: any;
  isEmbed: boolean | null;
  config: IConfig | null;
  initiallyShowLayerList: boolean | null;
  tables: any;
  maps: any;
  map: any;
  outdated_map_slug: string | null;
  portalAvailableLinks: PortalAvailableLinks;
}

export const useGlobalStore = defineStore("global", {
  state: (): IGlobalStoreState => ({
    position: null,
    layers: [],
    tool: null,
    selectedArea: null,
    searchQuery: null,
    alert: null,
    user: null,
    drawing: null,
    isEmbed: null,
    config: null,
    initiallyShowLayerList: null,
    tables: null,
    maps: null,
    map: null,
    outdated_map_slug: null,
    portalAvailableLinks: DEFAULT_PORTAL_AVAILABLE_LINKS,
  }),
  getters: {
    // getters
  },
  actions: {
    setInitialState(initialState: Partial<IGlobalStoreState>) {
      Object.assign(this, initialState);
    },
    setPosition(position: any) {
      this.position = position;
    },
    setLayers(layers: ILayer[]) {
      this.layers = layers;
    },
    addLayer(layer: ILayer) {
      if (!this.layers.includes(layer)) {
        this.layers.push(layer);
      }
    },
    deleteLayer(layer: ILayer) {
      const index = this.layers.indexOf(layer);
      if (index !== -1) {
        this.layers.splice(index, 1);
      }
    },
    toggleLayer([layerId, isVisible]: [string, boolean]) {
      this.layers = this.layers.map((layer) => (layer.id === layerId ? { ...layer, is_visible: isVisible } : layer));
    },
    setLayerOpacity([layerId, opacity]: [string, number]) {
      this.layers = this.layers.map((layer) => (layer.id === layerId ? { ...layer, opacity: opacity } : layer));
    },
    setTool(tool: any) {
      this.tool = tool;
    },
    setSelectedArea(area: any) {
      this.selectedArea = area;
    },
    setSearchQuery(searchQuery: any) {
      this.searchQuery = searchQuery;
    },
    setAlert(alert: any) {
      this.alert = alert;
    },
    setUser(user: IUser | null) {
      this.user = user;
    },
  },
});
