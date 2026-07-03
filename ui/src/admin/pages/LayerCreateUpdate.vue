<template>
  <div class="container __admin">
    <h1 class="font-weight-normal">Kaartlaag wijzigen</h1>
    <Spinner v-if="loading" style-type="'admin'" />
    <AdminFormSections
      v-else
      ref="formSections"
      :sections="sections"
      :initial-values="initialValues"
      :form-object="'layers'"
      :object-specific-save="saveLayer"
      @update-source="(source) => (selectedSource = source)"
      @related-tables-changed="handleRelatedTablesChange"
    >
      <!-- todo: weghalen wanneer we over zijn naar nieuwe manier van data koppelen.      -->
      <template #linkedData>
        <div class="layer-setting">
          <div class="admin-label-button">
            <Button
              v-tippy
              size="small"
              outlined
              aria-label="Voeg gekoppelde data toe"
              content="Voeg gekoppelde data toe"
              class="!tw-text-sm !tw-font-semibold !tw-bg-white hover:!tw-bg-transparent"
              type="button"
              @click="toggleModal('linkedData')"
            >
              <AddIcon />
              Voeg toe
            </Button>
          </div>

          <ul class="admin-list">
            <li v-for="linkedData in initialValues.linked_data" :key="linkedData.id">
              {{ linkedData.title }}
              <div class="admin-list-buttons">
                <button
                  v-tippy
                  :content="`Bewerk gekoppelde data ${linkedData.title}`"
                  :aria-label="`Bewerk gekoppelde data ${linkedData.title}`"
                  type="button"
                  class="iconbutton __normal __round"
                  @click="toggleModal('linkedData', linkedData)"
                >
                  <EditIcon class="icon __medium"></EditIcon>
                </button>
                <button
                  v-tippy
                  :content="`Verwijder gekoppelde data ${linkedData.title}`"
                  :aria-label="`Verwijder gekoppelde data ${linkedData.title}`"
                  type="button"
                  class="iconbutton __normal __round"
                  @click="removeLinkedData(linkedData)"
                >
                  <TrashIcon class="icon __medium"></TrashIcon>
                </button>
              </div>
            </li>
          </ul>
        </div>
      </template>
      <template #templates>
        <div class="layer-setting">
          <div class="admin-label-button">
            <Button
              v-tippy
              size="small"
              outlined
              aria-label="Voeg template toe"
              content="Voeg template toe"
              class="!tw-text-sm !tw-font-semibold !tw-bg-white hover:!tw-bg-transparent"
              type="button"
              @click="toggleModal('templates')"
            >
              <AddIcon />
              Voeg toe
            </Button>
          </div>

          <ul class="admin-list">
            <li v-for="template in initialValues.templates" :key="template.id">
              {{ template.title }}
              <div class="admin-list-buttons">
                <button
                  v-tippy
                  :content="`Bewerk template ${template.title}`"
                  :aria-label="`Bewerk template ${template.title}`"
                  type="button"
                  class="iconbutton __normal __round"
                  @click="toggleModal('templates', template)"
                >
                  <EditIcon class="icon __medium"></EditIcon>
                </button>
                <button
                  v-tippy
                  :content="`Verwijder template ${template.title}`"
                  :aria-label="`Verwijder template ${template.title}`"
                  type="button"
                  class="iconbutton __normal __round"
                  @click="removeTemplate(template)"
                >
                  <TrashIcon class="icon __medium"></TrashIcon>
                </button>
              </div>
            </li>
          </ul>
        </div>
      </template>
    </AdminFormSections>
  </div>
  <Dialog
    v-model:visible="showFormModal"
    modal
    :header="formModalType === 'linkedData' ? 'Gerelateerde data' : 'Templates'"
    :style="{ width: '1200px', marginLeft: '2rem', marginRight: '2rem' }"
  >
    <LinkedDataForm
      v-if="formModalType === 'linkedData'"
      :initial-linked-data="selectedLinkedData"
      @close="closeFormModal"
      @save="saveLinkedData"
    />
    <TemplateForm
      v-else-if="formModalType === 'templates'"
      :initial-template="selectedTemplate"
      @close="closeFormModal"
      @save="saveTemplate"
    />
  </Dialog>
</template>

<script>
import AdminFormSections from "@/admin/components/AdminFormSections.vue";
import LinkedDataForm from "@/admin/components/LinkedDataForm.vue";
import TemplateForm from "@/admin/components/TemplateForm.vue";
import AddIcon from "@/assets/icons/add-icon.svg";
import EditIcon from "@/assets/icons/edit-icon.svg";
import TrashIcon from "@/assets/icons/trash-icon.svg";
import Spinner from "@/components/Spinner.vue";
import { useGlobalStore } from "@/stores";
import { mapState } from "pinia";
import { useQueryCache } from "@pinia/colada";
import { useCategoryList, useGroupList, useMetadatasetList, useSourceList, useTableList } from "@/admin/queries";

export default {
  name: "LayerCreateUpdate",
  components: {
    Spinner,
    EditIcon,
    AddIcon,
    TrashIcon,
    TemplateForm,
    LinkedDataForm,
    AdminFormSections,
  },
  setup() {
    const queryCache = useQueryCache();
    const { metadatasetsState } = useMetadatasetList();
    const { categoriesState } = useCategoryList();
    const { sourcesState } = useSourceList();
    const { groupsState, refresh: refreshGroups } = useGroupList();
    const { tablesState } = useTableList();
    return {
      queryCache,
      metadatasetsState,
      categoriesState,
      sourcesState,
      groupsState,
      refreshGroups,
      tablesState,
    };
  },
  data() {
    return {
      categories: [],
      metadatasets: [],
      selectedRelatedTables: [],
      sourceTypes: [],
      formats: [],
      initialValues: {},
      selectedSource: {},
      showFormModal: false,
      formModalType: null,
      selectedLinkedData: null,
      selectedTemplate: null,
      loading: false,
    };
  },
  computed: {
    ...mapState(useGlobalStore, ["config"]),
    categoriesWithFullTitle() {
      return (this.categoriesState.data || []).map((category) => ({
        id: category.id,
        label: category.fullTitle,
      }));
    },
    sections() {
      return this.getSections();
    },
  },

  created() {
    this.loading = true;

    this.sourceTypes = [
      { id: "WMS_WFS", label: "WMS en WFS" },
      { id: "WMS", label: "WMS" },
      { id: "WFS", label: "WFS" },
      { id: "WMTS", label: "WMTS" },
      { id: "XYZ", label: "XYZ" },
      { id: "MVT", label: "MVT" },
    ];
    this.formats = [
      { id: "image/png", label: "image/png" },
      { id: "image/jpeg", label: "image/jpeg" },
      { id: "image/vnd.jpeg-png", label: "image/vnd.jpeg-png" },
    ];

    this.getLayer()
      .then(() => this.setAtlasGroups())
      .finally(() => {
        this.loading = false;
      });
  },
  methods: {
    async getLayer() {
      const result = await fetch(`/atlas/api/v1/layers/${this.$route.params.id}/`, {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch layer");
        return;
      }

      const response = await result.json();
      this.initialValues = response;
      this.initialValues.category_id = response.category?.id;
      this.initialValues.source_id = response.source.id;

      // Internal fields used for v-model binding
      this.initialValues.client_style = JSON.stringify(response.client_style, null, 2);
      this.initialValues.friendly_fields = JSON.stringify(response.friendly_fields, null, 2);
      this.initialValues.templated_properties = JSON.stringify(response.templated_properties, null, 2);
      this.initialValues.linked_data = response.linked_data;
      this.initialValues.templates = response.templates;
      this.initialValues.search_properties = response.search_properties.join("\n");
      this.initialValues.display_properties = response.display_properties.join("\n");
      this.initialValues.search_terms = response.search_terms ? response.search_terms.join("\n") : "";
      if (response.metadataset) {
        this.initialValues.metadataset = response.metadataset;
      } else {
        this.initialValues.metadataset = null;
      }

      // Set selectedSource
      this.selectedSource = {
        id: response.source.id,
        label: response.source.title,
        url: response.source.url,
        type: response.source.source_type,
      };

      return result;
    },
    async saveLayer(currentValues, continueEditing = false) {
      if (currentValues.layer_name) {
        currentValues.layer_name =
          typeof currentValues.layer_name === "string"
            ? currentValues.layer_name
            : currentValues.layer_name?.value || currentValues.layer_name;
      } else {
        currentValues.layer_name = null;
      }

      // Convert internal fields back to layer model.
      currentValues.atlas_groups = currentValues.atlas_groups?.[1]?.map((group) => group.id) || [];
      currentValues.atlas_write_groups = currentValues.atlas_write_groups?.[1]?.map((group) => group.id) || [];

      currentValues.display_properties = currentValues.display_properties
        .split("\n")
        .filter((value) => value.trim() !== "");
      currentValues.search_properties = currentValues.search_properties
        .split("\n")
        .filter((value) => value.trim() !== "");
      currentValues.search_terms = currentValues.search_terms.split("\n").filter((value) => value.trim() !== "");

      currentValues.extent_min_x = currentValues.extent_min_x === "" ? null : currentValues.extent_min_x;
      currentValues.extent_min_y = currentValues.extent_min_y === "" ? null : currentValues.extent_min_y;
      currentValues.extent_max_x = currentValues.extent_max_x === "" ? null : currentValues.extent_max_x;
      currentValues.extent_max_y = currentValues.extent_max_y === "" ? null : currentValues.extent_max_y;

      currentValues.client_style = this.validateAndParseJsonString(currentValues.client_style);
      currentValues.friendly_fields = this.validateAndParseJsonString(currentValues.friendly_fields);
      currentValues.templated_properties = this.validateAndParseJsonString(currentValues.templated_properties);

      if (currentValues.related_tables && currentValues.related_tables.length > 0) {
        const relatedTables = [];
        // Because relatedTables consist of the actual tables we still need to translate it to the relations objects
        // expected by the API.
        currentValues.related_tables.forEach((related_table) => {
          const layerToTable = {
            id: related_table.layer_to_table_id,
            from_layer: currentValues.id,
            to_table: related_table.id,
            field_mapping: related_table.field_mapping,
            related_table_title: related_table.related_table_title,
          };
          relatedTables.push(layerToTable);
        });

        currentValues.related_tables = relatedTables;
      }

      currentValues.templates = this.initialValues.templates;
      currentValues.linked_data = this.initialValues.linked_data;

      if (currentValues.metadataset === undefined || currentValues.metadataset === "") {
        currentValues.metadataset = null;
      }

      const url = `/atlas/api/v1/layers/${this.$route.params.id}/`;

      try {
        const result = await this.$refs.formSections.sendSaveRequest(url, "PATCH", currentValues);
        if (result.ok) {
          await this.queryCache.invalidateQueries(["layers"]);
          this.$toast.add({
            severity: "success",
            summary: "Laag opgeslagen",
            detail: "De laag is succesvol opgeslagen.",
            life: 3000,
          });

          if (!continueEditing) {
            this.$router.push(`/layers`);
          }
        }
      } catch (e) {
        console.error("An unexpected error occurred:", e);
      }
    },
    async setAtlasGroups() {
      await this.refreshGroups();
      const groups = this.groupsState.data || [];
      const selectedGroups = groups.filter((group) => this.initialValues.atlas_groups.includes(group.id));
      const availableGroups = groups.filter((group) => !this.initialValues.atlas_groups.includes(group.id));
      const selectedWritableGroups = groups.filter((group) => this.initialValues.atlas_write_groups.includes(group.id));
      const availableWritableGroups = groups.filter(
        (group) => !this.initialValues.atlas_write_groups.includes(group.id),
      );
      this.initialValues.atlas_groups = [availableGroups, selectedGroups];
      this.initialValues.atlas_write_groups = [availableWritableGroups, selectedWritableGroups];
    },
    validateAndParseJsonString(text) {
      if (!text || text.trim() === "") {
        return {};
      }

      return JSON.parse(text);
    },
    saveLinkedData(newValues) {
      if (!newValues.id && !newValues.randomId) {
        // If newValues has no id it needs to be added to the linked_data array.
        this.initialValues.linked_data.push({ ...newValues, randomId: crypto.getRandomValues(new Uint32Array(1))[0] });
      } else {
        // Otherwise update existing values.
        const index = this.initialValues.linked_data.findIndex(
          (data) => (data.id && data.id === newValues.id) || (data.randomId && data.randomId === newValues.randomId),
        );

        if (index !== -1) {
          this.initialValues.linked_data.splice(index, 1, newValues);
        }
      }
      this.closeFormModal();
    },
    async saveTemplate(newValues) {
      if (!newValues.id && !newValues.randomId) {
        this.initialValues.templates.push({ ...newValues, randomId: crypto.getRandomValues(new Uint32Array(1))[0] });
      } else {
        const index = this.initialValues.templates.findIndex(
          (data) => (data.id && data.id === newValues.id) || (data.randomId && data.randomId === newValues.randomId),
        );

        if (index !== -1) {
          this.initialValues.templates.splice(index, 1, newValues);
        }
      }
      this.closeFormModal();
    },
    removeLinkedData(linkedData) {
      const acknowledged = confirm("Weet je zeker dat je het geselecteerde data object wilt verwijderen?");

      if (acknowledged) {
        const index = this.initialValues.linked_data.indexOf(linkedData);
        this.initialValues.linked_data.splice(index, 1);
      }
    },
    removeTemplate(template) {
      const acknowledged = confirm("Weet je zeker dat je het geselecteerde data object wilt verwijderen?");

      if (acknowledged) {
        const index = this.initialValues.templates.indexOf(template);
        this.initialValues.templates.splice(index, 1);
      }
    },
    closeFormModal() {
      this.showFormModal = false;
      this.formModalType = null;
      this.selectedLinkedData = null;
    },
    toggleModal(modalType, editObject = null) {
      this.formModalType = modalType;

      if (modalType === "linkedData") {
        if (editObject) {
          this.selectedLinkedData = { ...editObject, edit: true };
        } else {
          this.selectedLinkedData = {
            title: "",
            url: "",
            name: "",
            source_key: "",
            target_key: "",
            display_properties: [],
            headers: [],
            use_detail_view: false,
            detail_view_fields: [],
            edit: false,
          };
        }
      } else if (modalType === "templates") {
        if (editObject) {
          this.selectedTemplate = { ...editObject, edit: true };
        } else {
          this.selectedTemplate = {
            title: "",
            source: "",
            endpoint: "",
            method: "",
            list: "",
            headers: [],
            fields: [],
            template: "",
            source_key: "",
            target_key: "",
            edit: false,
          };
        }
      }

      this.showFormModal = true;
    },
    handleRelatedTablesChange(newValue) {
      this.initialValues.related_tables = newValue;
    },
    getSections() {
      return {
        general: {
          label: "Algemene gegevens",
          questions: [
            {
              label: "Titel",
              id: "title",
              name: "Title",
              type: "text",
              required: true,
            },
            {
              label: "Kort kenmerk",
              id: "slug",
              name: "Slug",
              type: "text",
              required: true,
              maxLength: 255,
              infoText: "Een uniek kenmerk voor de laag in Atlas. Dit kenmerk komt terug in links naar de laag.",
            },
            {
              label: "Categorie",
              id: "category_id",
              name: "Category",
              type: "dropdown",
              placeholder: "categorie",
              required: false,
              options: this.categoriesWithFullTitle || [],
            },
            {
              label: "Beschrijving",
              id: "description",
              name: "Description",
              type: "text",
              required: false,
              multiLine: true,
              infoText: "Een beschrijving van de laag. Het is mogelijk om tekst op te maken met Markdown in dit veld.",
            },
            {
              label: "Metadata",
              id: "metadataset",
              name: "Metadataset",
              type: "metadataset-select",
              required: false,
              placeholder: "Metadata",
              options: this.metadatasetsState.data,
            },
            {
              label: "Gepubliceerd",
              id: "published",
              name: "Published",
              type: "checkbox",
              required: false,
              getHintText: (values) => {
                const hasMetadataset = values.metadataset != null && values.metadataset !== "";
                if (values.published && !hasMetadataset) {
                  return "Let op: er is nog geen metadataset geselecteerd. Metadata maakt de kaartlaag herleidbaar.";
                }
                return "";
              },
            },
            {
              label: "Kaartlaag is exporteerbaar",
              infoText:
                "Met dit veld configureer je of de data achter een kaartlaag wel/niet exporteerbaar is vanuit de dataweergave.",
              id: "is_exportable",
              name: "IsExportable",
              type: "checkbox",
              required: false,
            },
          ],
        },
        source: {
          label: "Bron",
          questions: [
            {
              label: "Bron",
              id: "source_id",
              name: "Source",
              type: "dropdown",
              required: true,
              placeholder: "bron",
              options: this.sourcesState.data || [],
            },
            {
              label: "Laagnaam",
              id: "layer_name",
              name: "LayerName",
              type: "layer-select",
              placeholder: "laag",
              sourceField: "source_id",
              options: this.sourcesState.data || [],
              infoText: "De naam van de laag op de geoserver.",
              contains_colon: true,
            },
            {
              label: "Brontype",
              id: "source_type",
              name: "SourceType",
              type: "dropdown",
              required: false,
              placeholder: "brontype",
              options: this.sourceTypes,
              infoText:
                '"WMS en WFS" en WFS is zichtbaar in zowel het datapaneel als op de kaart. WMS en WMTS toont alleen op de kaart.',
            },
            {
              label: "Projectie",
              id: "projection",
              name: "Projection",
              type: "text",
              required: false,
            },
            {
              label: "Servertype",
              id: "server_type",
              name: "ServerType",
              type: "text",
              required: false,
            },
            {
              label: "Formaat",
              id: "format",
              name: "Format",
              type: "dropdown",
              required: false,
              placeholder: "bron",
              options: this.formats,
            },
          ],
        },
        display: {
          label: "Weergave",
          questions: [
            {
              label: "Transparantie",
              id: "opacity",
              name: "Transparantie",
              type: "decimal",
              required: true,
              step: 0.1,
            },
            {
              label: "Is basislaag",
              id: "is_base",
              name: "IsBase",
              type: "checkbox",
              required: false,
            },
            {
              label: "Is standaard zichtbaar",
              id: "is_visible",
              name: "IsVisible",
              type: "checkbox",
              required: false,
            },
            {
              label: "Is selecteerbaar",
              id: "is_selectable",
              name: "IsSelectable",
              type: "checkbox",
              required: false,
            },
            {
              label: "Haal detailinformatie als HTML op bij de bron",
              id: "use_html_info_format",
              name: "UseHtmlInfoFormat",
              type: "checkbox",
              required: false,
            },
            {
              label: "Toon laag in detail- en dataweergave",
              id: "show_in_detail_panel",
              name: "ShowInDetailPanel",
              type: "checkbox",
              required: false,
            },
            {
              label: "Maak laag filterbaar in legenda",
              id: "is_filterable_in_legend",
              name: "IsFilterableInLegend",
              type: "checkbox",
              required: false,
              infoText:
                "Hiermee kunnen gebruikers filteren op de verschillende waarden die in de legenda worden weergegeven. Let op: Deze functie werkt enkel met WMS-, WMS-WFS- en WFS-bronnen die een JSON-response ondersteunen.",
            },
            {
              label: "Toon deze velden",
              id: "display_properties",
              name: "DisplayProperties",
              type: "text",
              multiLine: true,
              required: false,
              isNested: true,
              infoText: "Voer één veld per regel in. Bij geen invoer worden alle velden getoond.",
            },
            {
              label: "Doorzoek deze velden",
              id: "search_properties",
              name: "SearchProperties",
              type: "text",
              multiLine: true,
              required: false,
              isNested: true,
              infoText: "Voer één veld per regel in. Bij geen invoer worden alle velden getoond.",
            },
            {
              label: "Bereik minimum x",
              id: "extent_min_x",
              name: "ExtentMinX",
              type: "decimal",
              required: false,
              step: 0.01,
              infoText: "Vul in om de laag inactief te maken wanneer de weergave buiten het bereik ligt.",
            },
            {
              label: "Bereik minimum y",
              id: "extent_min_y",
              name: "ExtentMinY",
              type: "decimal",
              required: false,
              step: 0.01,
              infoText: "Vul in om de laag inactief te maken wanneer de weergave buiten het bereik ligt.",
            },
            {
              label: "Bereik maximum x",
              id: "extent_max_x",
              name: "ExtentMaxX",
              type: "decimal",
              required: false,
              step: 0.01,
              infoText: "Vul in om de laag inactief te maken wanneer de weergave buiten het bereik ligt.",
            },
            {
              label: "Bereik maximum y",
              id: "extent_max_y",
              name: "ExtentMaxY",
              type: "decimal",
              required: false,
              step: 0.01,
              infoText: "Vul in om de laag inactief te maken wanneer de weergave buiten het bereik ligt.",
            },
            {
              label: "Zoomniveau minimum",
              id: "zoom_min",
              name: "ZoomMin",
              type: "decimal",
              required: false,
              step: 0.01,
            },
            {
              label: "Zoomniveau maximum",
              id: "zoom_max",
              name: "ZoomMax",
              type: "decimal",
              required: false,
              step: 0.01,
            },
            {
              label: "Stijlnaam voor WMS / WMTS laag",
              id: "server_style",
              name: "ServerStyle",
              type: "text",
              required: false,
              infoText: "Stijlnaam zoals beschikbaar op de server",
            },
            {
              label: "Stijl voor WFS / MVT laag",
              id: "client_style",
              name: "ClientStyle",
              type: "json",
              required: false,
              isNested: true,
              infoText: "Stijl in GeoStyler formaat.",
            },
            {
              label: "Vriendelijke veldnamen",
              id: "friendly_fields",
              name: "FriendlyFields",
              type: "json",
              required: false,
              isNested: true,
              infoText: "Maak veldnamen vriendelijk.",
            },
            {
              label: "Templatevelden",
              id: "templated_properties",
              name: "TemplatedProperties",
              type: "json",
              required: false,
              isNested: true,
              infoText: "Velden die samengesteld worden vanuit een template.",
            },
            {
              label: "Legenda",
              id: "legend_url",
              name: "LegendUrl",
              type: "text",
              required: false,
              infoText: "Overschrijf link naar legenda",
              withImagePreview: true,
            },
            {
              label: "Zoektermen",
              id: "search_terms",
              name: "SearchTerms",
              type: "text",
              required: false,
              multiLine: true,
              infoText:
                "Deze worden gebruikt om de laag beter vindbaar te maken in het lagenpaneel. Voer één zoekterm per regel in.",
            },
          ],
        },
        timeline: {
          label: "Tijdlijn",
          questions: [
            {
              label: "Tijdlijn",
              id: "is_time_enabled",
              name: "IsTimeEnabled",
              type: "checkbox",
              required: false,
              infoText: "Schakel tijdlijn in voor deze laag.",
            },
            {
              label: "Peildatumweergave",
              id: "is_reference_date_enabled",
              name: "IsReferenceDateEnabled",
              type: "checkbox",
              required: false,
              infoText: "Maakt het mogelijk om in de tijdlijn één peildatum te kiezen in plaats van een periode.",
            },
            {
              label: "Standaardweergave",
              id: "time_slider_default_display_mode",
              name: "TimeSliderDefaultDisplayMode",
              type: "dropdown",
              placeholder: "standaardweergave",
              options: [
                { id: "period", label: "Periode" },
                { id: "referenceDate", label: "Peildatum" },
              ],
              infoText: "De weergave waarmee de tijdlijn standaard opent voor deze laag.",
            },
            {
              label: "Startdatumveld (GeoServer TIME)",
              id: "time_slider_start_field",
              name: "TimeSliderStartField",
              type: "text",
              required: false,
              infoText:
                "Naam van het WFS-attribuut dat in GeoServer als startdatum voor de TIME-dimensie is geconfigureerd.",
            },
            {
              label: "Einddatumveld (GeoServer TIME)",
              id: "time_slider_end_field",
              name: "TimeSliderEndField",
              type: "text",
              required: false,
              infoText:
                "Naam van het WFS-attribuut dat in GeoServer als einddatum voor de TIME-dimensie is geconfigureerd.",
            },
          ],
        },
        access: {
          label: "Toegang",
          questions: [
            {
              label: "Alleen intern zichtbaar",
              id: "closed_dataset",
              name: "ClosedDataset",
              type: "checkbox",
              required: false,
              infoText: "Laag is alleen zichtbaar binnen het interne netwerk.",
              showIf: this.config?.features?.featureLayerInternalVisibility,
            },
            {
              label: "Vereis inlog voor deze kaartlaag",
              id: "login_required",
              name: "LoginRequired",
              type: "checkbox",
              required: false,
              infoText: "De inhoud van deze kaartlaag kan alleen bekeken worden door ingelogde gebruikers.",
            },
            {
              label: "Ingelogde gebruikers kunnen kaartlaag bewerken",
              id: "authenticated_can_mutate",
              name: "AuthenticatedCanMutate",
              type: "checkbox",
              required: false,
              infoText:
                "Alle ingelogde gebruikers kunnen wanneer deze optie aanstaat de kaartlaag muteren voor kaarten waar de CRUD-functionaliteit is ingeschakeld.",
            },
            {
              label: "Lees groepen",
              objectDisplayName: "lees groepen",
              id: "atlas_groups",
              name: "atlasGroups",
              type: "picklist",
            },
            {
              label: "Schrijf groepen",
              objectDisplayName: "schrijf groepen",
              id: "atlas_write_groups",
              name: "atlasWriteGroups",
              type: "picklist",
            },
          ],
        },
        tables: {
          label: "Relaties",
          questions: [
            {
              label: "Gerelateerde tabellen",
              id: "related_tables",
              name: "relatedTables",
              type: "related-tables-select",
              required: false,
              placeholder: "Selecteer gerelateerde tabellen",
              options: this.tablesState.data || [],
            },
          ],
          showIf: this.config?.features?.newTables,
        },
        linkedData: {
          label: "(Oud) Gekoppelde data",
          questions: [],
          disableInputs: true,
          showIf: this.config?.features?.oldLinkedDataAndTemplate,
        },
        templates: {
          label: "(Oud) Templates",
          questions: [],
          disableInputs: true,
          showIf: this.config?.features?.oldLinkedDataAndTemplate,
        },
      };
    },
  },
};
</script>

<style scoped>
.admin-label-button {
  display: flex;
  justify-content: end;
  align-items: center;
  margin-bottom: 12px;
}

.admin-list > li {
  display: flex;
  align-items: center;
  background: var(--color-white);
  padding: 4px 12px;
}

.admin-list > li:not(:last-child) {
  border-bottom: 1px solid var(--color-grey-60);
}

.admin-list-buttons {
  display: flex;
  gap: 6px;
  margin-left: auto;
}

.admin-list-buttons button:hover {
  background-color: var(--color-backdrop);
}
</style>
