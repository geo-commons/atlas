<template>
  <ExpandButton v-if="features.length > 0 || html" :title="featureInfoTitle" :is-open="isOpen" class="feature">
    <div v-if="html" class="html" v-html="html" />
    <div v-for="feature in features" :key="feature.id" class="border-bottom">
      <div class="feature-select">
        <table-list>
          <table>
            <tbody>
              <tr v-for="property in filterProperties(feature.properties)" :key="property">
                <td>{{ formatProperty(property) }}</td>
                <td>
                  <RichValue :data-key="property" :data-value="feature.properties[property]" />
                </td>
              </tr>
              <tr v-for="property in Object.keys(layer.templated_properties)" :key="property">
                <td>
                  {{ formatProperty(property) }}
                </td>
                <td>
                  <MarkdownTemplate
                    :source="layer.templated_properties[property]"
                    :data="getTemplatedPropertiesData(feature.properties)"
                  />
                </td>
              </tr>
            </tbody>
          </table>
        </table-list>
      </div>

      <div class="tw-flex tw-px-5 tw-py-2 tw-gap-3 tw-flex-wrap">
        <Button
          v-if="!shouldHideSelectButton(feature)"
          v-tippy
          aria-label="Maak selectie"
          content="Maak selectie"
          outlined
          severity="secondary"
          class="!tw-text-sm !tw-font-medium"
          aria-haspopup="true"
          aria-controls="overlay_menu"
          @click="selectFeature(feature)"
        >
          Maak selectie
          <AreaSelectIcon class="icon __smedium" />
        </Button>
        <Button
          v-if="showEditLayerButton(layer)"
          outlined
          severity="secondary"
          class="!tw-text-sm !tw-font-medium"
          aria-haspopup="true"
          aria-controls="overlay_menu"
          @click="toggleEditLayerMode(feature)"
        >
          Bewerk
          <EditIcon />
        </Button>
        <Button
          v-tippy
          aria-label="Bekijk object"
          content="Bekijk object"
          outlined
          severity="secondary"
          class="!tw-text-sm !tw-font-medium"
          aria-haspopup="true"
          aria-controls="overlay_menu"
          @click="() => $emit('show-selected-feature', feature)"
        >
          Bekijk
          <MarkerIcon class="icon __marker __smedium" />
        </Button>
        <Button
          v-tippy
          aria-label="Kopieer object"
          content="Kopieer object"
          outlined
          severity="secondary"
          class="!tw-text-sm !tw-font-medium"
          aria-haspopup="true"
          aria-controls="overlay_menu"
          @click="copyFeature(feature)"
        >
          {{ checkCopyStatus(feature.id) ? "Gekopieerd!" : "Kopieer" }}
          <CopyIcon class="icon __smedium" />
        </Button>
      </div>

      <div v-for="(linkedData, key) in layer.linked_data" :key="key">
        <div v-if="feature.properties[linkedData.source_key]" class="linked-data">
          <LinkedDataTable
            :linked-data="linkedData"
            :overall-filter="{ key: linkedData.target_key, value: feature.properties[linkedData.source_key] }"
            :position="position"
            @set-position="setPosition"
            @on-fit="(value) => onFit(value)"
          />
        </div>
      </div>

      <div v-for="(template, key) in layer.templates" :key="key">
        <FeatureInfoTemplate :layer="layer" :template="template" :feature="feature" class="template" />
      </div>

      <div v-if="layer.related_tables.length > 0">
        <div v-for="(relatedTable, key) in layer.related_tables" :key="key">
          <RelatedTableList
            :layer-feature="feature"
            :related-table="relatedTable"
            :field-mapping="relatedTable.field_mapping"
            @select-related-table-object="onSelectRelatedTableObject"
          />
        </div>
      </div>
    </div>
  </ExpandButton>
</template>

<script>
import nunjucks from "nunjucks";
import { getForViewAndSize } from "ol/extent";
import LinkedDataTable from "./LinkedDataTable.vue";
import TableList from "./TableList";
import TileWMS from "ol/source/TileWMS";
import View from "ol/View";
import ExpandButton from "./ExpandButton";
import RichValue from "./RichValue";
import FeatureInfoTemplate from "./FeatureInfoTemplate";
import MarkdownTemplate from "./MarkdownTemplate";
import { mapState, mapStores } from "pinia";
import { useGlobalStore } from "@/stores";
import { formatRawString } from "@/utils/string-helpers";
import MarkerIcon from "@/assets/icons/marker-icon.svg";
import CopyIcon from "@/assets/icons/copy-icon.svg";
import AreaSelectIcon from "@/assets/icons/area-select-icon.svg";
import EditIcon from "@/assets/icons/edit-icon.svg";
import { useEditLayerStore } from "@/stores/edit_layer_store";
import { EditLayerMode } from "@/types/map";
import GeoJSON from "ol/format/GeoJSON";
import { ELayerTypes } from "@/types/layer";
import { WMTS } from "ol/source";
import { optionsFromCapabilities } from "ol/source/WMTS";
import WMTSCapabilities from "ol/format/WMTSCapabilities";
import RelatedTableList from "@/components/related-tables/RelatedTableList.vue";

nunjucks.configure({ autoescaping: true });

export default {
  name: "FeatureInfo",
  components: {
    RelatedTableList,
    EditIcon,
    MarkerIcon,
    CopyIcon,
    AreaSelectIcon,
    TableList,
    LinkedDataTable,
    ExpandButton,
    RichValue,
    FeatureInfoTemplate,
    MarkdownTemplate,
  },
  props: {
    layer: Object,
    position: Object,
    config: Object,
    atlasFeatures: Object,
    isOpen: Boolean,
  },
  emits: [
    "set-position",
    "on-fit",
    "select-feature-details",
    "show-selected-feature",
    "select-feature",
    "select-related-linked-data",
    "select-related-table-object",
  ],
  data() {
    return {
      features: [],
      html: "",
      onCopy: {},
    };
  },
  computed: {
    ...mapStores(useEditLayerStore),
    ...mapStores(useGlobalStore),
    ...mapState(useGlobalStore, ["user"]),
    featureInfoTitle() {
      if (this.features.length > 1) {
        return `${this.layer.title} (${this.features.length})`;
      }

      return this.layer.title;
    },
  },
  watch: {
    position: "fetchFeatures",
  },
  mounted() {
    this.fetchFeatures();
  },
  methods: {
    fetchFeatures() {
      this.onSelectRelatedTableObject(null);

      if (this.layer.source_type === ELayerTypes.WMS || this.layer.source_type === ELayerTypes.WMS_WFS) {
        return this.fetchFeaturesFromWMS();
      }

      if (this.layer.source_type === ELayerTypes.WFS) {
        return this.fetchFeaturesFromWFS();
      }

      if (this.layer.source_type === ELayerTypes.WMTS) {
        return this.fetchFeaturesFromWMTS();
      }
    },
    async fetchFeaturesFromWMS() {
      const wmsSource = new TileWMS({
        url: this.layer.url,
        servertype: this.layer.server_type,
        params: {
          LAYERS: this.layer.name,
          TILED: true,
        },
      });

      const view = new View({
        center: this.position.center,
        zoom: this.position.zoom,
      });

      const url = wmsSource.getFeatureInfoUrl(this.position.marker, view.getResolution(), "EPSG:28992", {
        info_format: this.layer.use_html_info_format ? "text/html" : "application/json",
        feature_count: 100,
      });

      try {
        const result = await fetch(url, this.getFetchParameters());

        if (this.layer.use_html_info_format) {
          const data = await result.text();
          this.html = data;
          this.features = [];
        }

        if (!this.layer.use_html_info_format) {
          const data = await result.json();
          this.features = data.features;
        }
      } catch (e) {
        console.error(e);
      }
    },
    async fetchFeaturesFromWFS() {
      const view = new View({
        center: this.position.center,
        zoom: this.position.zoom,
      });

      const extent = getForViewAndSize(this.position.marker, view.getResolution(), 0, [1, 1]);

      const params = new URLSearchParams([
        ["service", "WFS"],
        ["version", "2.0.0"],
        ["request", "GetFeature"],
        ["typename", this.layer.name],
        ["outputFormat", "application/json"],
        ["srsname", this.layer.projection],
        ["bbox", extent.join(",")],
        ["maxFeatures", "100"],
      ]);

      const url = new URL(this.layer.url);
      url.search = params.toString();

      const result = await fetch(url.toString(), this.getFetchParameters());
      const data = await result.json();
      this.features = data.features;
    },
    /**
     * Fetches feature information from a WMTS layer at the current map position.
     *
     * This method:
     *  1. Requests and parses the WMTS GetCapabilities document.
     *  2. Builds a WMTS source from the capabilities and layer configuration.
     *  3. Constructs an OpenLayers View to determine the map resolution and the WMTS zoom level.
     *  4. Computes the WMTS tile (TileMatrix, TileRow, TileCol) that contains the user-selected coordinate.
     *  5. Calculates the pixel position (I, J) of the coordinate within that tile.
     *  6. Issues a WMTS GetFeatureInfo request using those computed values.
     *  7. Stores the returned HTML or GeoJSON features depending on configuration.
     *
     * WMTS Specification Reference:
     *   For definitions of TileMatrix, TileRow, TileCol, I, J, and the GetFeatureInfo
     *   request structure, see the OGC WMTS 1.0.0 standard:
     *   - Overview page: https://www.ogc.org/standards/wmts
     *   - Direct PDF:    https://portal.ogc.org/files/?artifact_id=35326  (OGC 07-057r7)
     */
    async fetchFeaturesFromWMTS() {
      const capabilitiesUrl = new URL(this.layer.url);

      const capabilitiesParams = new URLSearchParams({
        REQUEST: "GetCapabilities",
        service: "wmts",
      });

      capabilitiesUrl.search = capabilitiesParams.toString();

      const response = await fetch(capabilitiesUrl);
      const text = await response.text();
      const caps = new WMTSCapabilities().read(text);

      const options = optionsFromCapabilities(caps, {
        layer: this.layer.name,
        matrixSet: this.layer.projection,
        projection: this.layer.projection,
        format: this.layer.format,
        crossOrigin: "anonymous",
        style: this.layer.serverStyle || null,
      });

      const wmtsSource = new WMTS(options);
      const tileGrid = wmtsSource.getTileGrid();

      const view = new View({
        center: this.position.center,
        resolutions: tileGrid.getResolutions(),
        zoom: this.position.zoom,
        projection: this.layer.projection,
      });

      const resolution = view.getResolution();
      const coord = this.position.marker;

      const z = tileGrid.getZForResolution(resolution);

      const tileCoord = tileGrid.getTileCoordForCoordAndZ(coord, z);
      const tileCol = tileCoord[1];
      const tileRow = tileCoord[2];

      const tileOrigin = tileGrid.getOrigin(z);
      const tileSize = tileGrid.getTileSize(z);

      const xFromOrigin = (coord[0] - tileOrigin[0]) / resolution;
      const yFromOrigin = (tileOrigin[1] - coord[1]) / resolution;

      const I = Math.floor(xFromOrigin - tileCol * tileSize);
      const J = Math.floor(yFromOrigin - tileRow * tileSize);

      const url = new URL(this.layer.url);

      const params = new URLSearchParams({
        SERVICE: "WMTS",
        VERSION: "1.0.0",
        REQUEST: "GetFeatureInfo",
        LAYER: this.layer.name,
        TileMatrixSet: this.layer.projection,
        TileMatrix: `${this.layer.projection}:${z}`,
        TileCol: tileCol,
        TileRow: tileRow,
        I: I,
        J: J,
        INFOFORMAT: this.layer.use_html_info_format ? "text/html" : "application/json",
        FEATURE_COUNT: "20",
      });

      url.search = params.toString();

      try {
        const result = await fetch(url, this.getFetchParameters());

        if (this.layer.use_html_info_format) {
          this.html = await result.text();
          this.features = [];
        } else {
          const data = await result.json();
          this.features = data.features ?? [];
        }
      } catch (err) {
        console.error(err);
      }
    },
    setPosition(value) {
      this.$emit("set-position", value);
      this.globalStore.setPosition(value);
    },
    filterProperties(fetchedProperties) {
      if (this.layer.display_properties.length > 0) {
        return this.layer.display_properties.filter((p) => Object.keys(fetchedProperties).includes(p));
      }

      return Object.keys(fetchedProperties);
    },
    getFetchParameters() {
      if (this.layer.source && this.layer.source.authenticate && this.user && this.user.token) {
        return {
          headers: { Authorization: `Bearer ${this.user.token}` },
        };
      }

      return {};
    },
    getTemplatedPropertiesData(properties) {
      return {
        properties,
        position: this.position,
      };
    },
    onFit(value) {
      this.$emit("on-fit", value);
    },
    onSelectFeatureDetails(selectedFeature) {
      this.$emit("select-feature-details", selectedFeature);
    },
    onSelectRelatedLinkedData(linkedDataIdAttributes) {
      this.$emit("select-related-linked-data", linkedDataIdAttributes);
    },
    onSelectRelatedTableObject(attr) {
      this.$emit("select-related-table-object", attr);
    },
    formatProperty(property) {
      if (this.layer.friendly_fields && this.layer.friendly_fields[property]) {
        return this.layer.friendly_fields[property];
      }

      return formatRawString(property);
    },
    async copyFeature(feature) {
      if (!navigator.clipboard) {
        console.error("Clipboard API not supported");
        return;
      }

      const properties = this.filterProperties(feature.properties);

      const featureData = properties.reduce((acc, item) => {
        acc[item] = feature.properties[item];
        return acc;
      }, {});

      const formattedText = Object.entries(featureData)
        .map(([key, value]) => `${key}: ${value}`)
        .join("\n");
      try {
        await navigator.clipboard.writeText(formattedText);
        this.onCopy[feature.id] = true;
      } catch (err) {
        console.error("Failed to copy:", err);
      }

      setTimeout(() => {
        this.onCopy[feature.id] = false;
      }, 1000);
    },
    checkCopyStatus(featureId) {
      return this.onCopy[featureId];
    },
    async selectFeature(feature) {
      const geoFeature = new GeoJSON().readFeature(feature);

      this.$emit("select-feature", geoFeature.getGeometry());
    },
    shouldHideSelectButton(feature) {
      if (
        feature &&
        feature.geometry &&
        (feature.geometry.type === "Polygon" || feature.geometry.type === "MultiPolygon")
      ) {
        return false;
      }

      return true;
    },
    toggleEditLayerMode(feature) {
      try {
        const geoFeature = new GeoJSON().readFeature(feature);

        if (this.editLayerStore.editLayerMode !== EditLayerMode.EDIT) {
          this.editLayerStore.setEditLayerMode(EditLayerMode.EDIT);
          this.editLayerStore.setHighlightedFeatureAndLayer({
            feature: geoFeature,
            layer: this.layer,
          });

          return;
        }

        this.editLayerStore.setEditLayerMode(EditLayerMode.NONE);
        this.editLayerStore.setHighlightedFeatureAndLayer(null);
      } catch (e) {
        console.error(e);
      }
    },
    showEditLayerButton(layer) {
      return (
        this.config &&
        this.config.features.edit_layer_features &&
        this.atlasFeatures.edit_layer_features &&
        this.user &&
        layer.can_write &&
        (layer.source_type === "WMS_WFS" || layer.source_type === "WFS")
      );
    },
  },
};
</script>

<style scoped>
.feature {
  margin: 0 8px;
}

.feature :deep(.expand-wrapper) {
  border-radius: var(--radius-normal);
  overflow: hidden;
  height: 40px;
}

.feature :deep(.expand-button) {
  align-items: center;
}

.feature :deep(.name) {
  font-weight: var(--font-weight-bold);
}

.linked-data {
  padding: 0 8px 0 20px;
}

.template {
  padding: 0 8px 0 20px;
}

.table-wrapper + .table-wrapper {
  border-top: 1px solid var(--color-grey-50);
}

.table-wrapper td:first-child {
  width: 40%;
  color: var(--color-text-grey);
}

.table-wrapper td:last-child {
  padding-left: 20px;
}

.table-wrapper th,
.table-wrapper td {
  padding: 4px;
  vertical-align: top;
}

.border-bottom:not(:last-child) {
  border-bottom: 1px solid var(--color-grey-60);
  margin-bottom: 10px;
  padding-bottom: 10px;
}

.html {
  margin-left: 20px;
  margin-right: 20px;
}
</style>
