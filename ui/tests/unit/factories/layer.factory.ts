import { ELayerTypes, ILayer } from "@/types/layer";
import { ETimeSliderDisplayMode } from "@/types/mapStore";

const createDefaultLayer = (overrides: Partial<ILayer> = {}): ILayer => ({
  id: "layer-a",
  name: "workspace:layer-a",
  title: "Layer A",
  url: "https://example.com/geoserver/wfs",
  source_type: ELayerTypes.WMS_WFS,
  is_visible: true,
  projection: "EPSG:28992",
  can_write: false,
  opacity: 1,
  friendly_fields: {},
  is_selectable: true,
  is_base: false,
  category: null,
  show_in_detail_panel: true,
  server_type: "geoserver",
  server_style: null,
  source: {
    authenticate: false,
  },
  login_required: false,
  extent: null,
  zoom_min: null,
  zoom_max: null,
  is_time_enabled: true,
  is_reference_date_enabled: true,
  time_slider_default_display_mode: ETimeSliderDisplayMode.Period,
  time_slider_start_field: "valid_from",
  time_slider_end_field: "valid_to",
  ...overrides,
});

export const createLayer = (overrides: Partial<ILayer> = {}): ILayer => ({
  ...createDefaultLayer(),
  ...overrides,
});
