<template>
  <div class="container">
    <h1 class="font-weight-normal">Kaartlaag wijzigen</h1>
    <validation-observer v-slot="{ handleSubmit }">
      <form @submit.prevent="handleSubmit(saveLayer)">
        <AdminFormSections
          :sections="sections"
          :initial-values="initialValues"
          @update="(newValues) => (currentValues = newValues)"
        />
        <div class="config-btn-wrapper">
          <router-link to="/layers" class="button __tertiary">Annuleer</router-link>
          <button class="button __primary" type="submit">Opslaan</button>
        </div>
      </form>
    </validation-observer>

    <!--            <div>-->
    <!--              <validation-provider v-slot="{ errors }" name="LayerName">-->
    <!--                <label for="layer-name">Laagnaam</label>-->
    <!--                <input id="layer-name" v-model="data.layer_name" type="text" />-->
    <!--                <span>{{ errors[0] }}</span>-->
    <!--              </validation-provider>-->
    <!--            </div>-->

    <!--            <div>-->
    <!--              <validation-provider v-slot="{ errors }" name="SourceType" class="flex flex-column">-->
    <!--                <label for="source-type">Brontype</label>-->
    <!--                <select id="source-type" v-model="data.source_type" class="config-select-wrapper">-->
    <!--                  <option disabled value="">Selecteer een brontype</option>-->
    <!--                  <option v-for="type in sourceTypes" :key="type">-->
    <!--                    {{ type }}-->
    <!--                  </option>-->
    <!--                </select>-->
    <!--                <span>{{ errors[0] }}</span>-->
    <!--              </validation-provider>-->
    <!--            </div>-->

    <!--            <div>-->
    <!--              <validation-provider v-slot="{ errors }" name="Projection">-->
    <!--                <label for="projection">Projectie</label>-->
    <!--                <input id="projection" v-model="data.projection" type="text" />-->
    <!--                <span>{{ errors[0] }}</span>-->
    <!--              </validation-provider>-->
    <!--            </div>-->

    <!--            <div>-->
    <!--              <validation-provider v-slot="{ errors }" name="ServerType">-->
    <!--                <label for="server-type">Servertype</label>-->
    <!--                <input id="server-type" v-model="data.server_type" type="text" />-->
    <!--                <span>{{ errors[0] }}</span>-->
    <!--              </validation-provider>-->
    <!--            </div>-->

    <!--            <div>-->
    <!--              <validation-provider v-slot="{ errors }" name="Format" class="flex flex-column">-->
    <!--                <label for="format">Formaat</label>-->
    <!--                <select id="format" v-model="data.format" class="config-select-wrapper">-->
    <!--                  <option disabled value="">Selecteer een formaat</option>-->
    <!--                  <option v-for="format in formats" :key="format">-->
    <!--                    {{ format }}-->
    <!--                  </option>-->
    <!--                </select>-->
    <!--                <span>{{ errors[0] }}</span>-->
    <!--              </validation-provider>-->
    <!--            </div>-->
    <!--          </div>-->
    <!--        </div>-->

    <!--        <hr />-->
    <!--        <div class="config-section-wrapper">-->
    <!--          <div><h3 class="font-weight-normal">Weergave</h3></div>-->

    <!--          <div></div>-->
    <!--        </div>-->
    <!--        <hr />-->
    <!--        <div class="config-section-wrapper">-->
    <!--          <div><h3 class="font-weight-normal">Metadata</h3></div>-->
    <!--          <div>-->
    <!--            &lt;!&ndash;                todo: naam metadata niet in api response?&ndash;&gt;-->

    <!--            <div>-->
    <!--              <validation-provider v-slot="{ errors }" name="Naam">-->
    <!--                <label for="name">Naam</label>-->
    <!--                <input id="name" type="text" />-->
    <!--                <span>{{ errors[0] }}</span>-->
    <!--              </validation-provider>-->
    <!--            </div>-->

    <!--            <div>-->
    <!--              <validation-provider v-slot="{ errors }" name="Description" class="flex flex-column">-->
    <!--                <label for="description">Omschrijving</label>-->
    <!--                <textarea id="description" v-model="data.metadata.description" type="text" />-->
    <!--                <span>{{ errors[0] }}</span>-->
    <!--              </validation-provider>-->
    <!--            </div>-->

    <!--            &lt;!&ndash;              todo: laatst bijgewerkt > waarom is dit een invoerveld? &ndash;&gt;-->
    <!--            <div>-->
    <!--              <validation-provider v-slot="{ errors }" name="Updated">-->
    <!--                <label for="updated">Laatst bijgewerkt</label>-->
    <!--                <input id="updated" v-model="data.metadata.updated" type="text" />-->
    <!--                <span>{{ errors[0] }}</span>-->
    <!--              </validation-provider>-->
    <!--            </div>-->

    <!--            <div>-->
    <!--              <validation-provider v-slot="{ errors }" name="Link">-->
    <!--                <label for="link">Meer informatie</label>-->
    <!--                <input id="link" v-model="data.metadata.link" type="text" />-->
    <!--                <span>{{ errors[0] }}</span>-->
    <!--              </validation-provider>-->
    <!--            </div>-->
    <!--          </div>-->
    <!--        </div>-->
    <!--        <hr />-->
    <!--        <div class="config-section-wrapper">-->
    <!--          <div><h3 class="font-weight-normal">Toegang</h3></div>-->

    <!--          <div></div>-->
    <!--        </div>-->

    <!--        <div class="config-btn-wrapper">-->
    <!--          <router-link to="/layers" class="button __tertiary">Annuleer</router-link>-->
    <!--          <button class="button __primary" type="submit">Opslaan</button>-->
    <!--        </div>-->
    <!--      </form>-->
    <!--    </validation-observer>-->
  </div>
</template>

<script>
import { ValidationObserver } from "vee-validate";

import Cookies from "js-cookie";
import AdminFormSections from "@/admin/components/AdminFormSections.vue";
// import { convertApiModelToFormData, convertFormDataToApiModel } from "@/utils/api-model-converter";

export default {
  name: "LayerCreateUpdate",
  components: {
    AdminFormSections,
    ValidationObserver,
    // ValidationProvider,
  },
  data() {
    return {
      data: null,
      formData: null,
      layersFromCapabilities: [],
      categories: {},
      sources: {},
      sourceTypes: [],
      formats: [],
      sections: {},
      initialValues: {},
      currentValues: {},
    };
  },
  created() {
    this.getLayer();
    // this.getSources();
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
    this.sections = this.getSections();
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

      this.data = await result.json();
      this.data.category_id = this.data.category.id;
      this.data.source_id = this.data.source.id;

      this.initialValues = this.data;
    },
    async saveLayer() {
      let result;

      result = await fetch(`/atlas/api/v1/layers/${this.$route.params.id}/`, {
        method: "PATCH",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": Cookies.get("csrftoken"),
        },
        body: JSON.stringify(this.currentValues),
      });

      if (!result.ok) {
        console.error(
          `Error occurred while saving layer with layer id: ${this.currentValues.id} and title: ${this.currentValues.title}`
        );
      }

      this.$router.push(`/layers`);
    },
    async getCategories() {
      const result = await fetch("/atlas/api/v1/categories/", {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch categories");
      }

      const response = await result.json();

      return response.map((category) => {
        return { id: category.id, label: category.title };
      });
    },
    async getSources() {
      const result = await fetch("/atlas/api/v1/sources/", {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch sources");
      }

      const response = await result.json();

      return response.map((source) => {
        return { id: source.id, label: source.title };
      });
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
            },
            {
              label: "Categorie",
              id: "category_id",
              name: "Category",
              type: "dropdown",
              required: true,
              placeholder: "categorie",
              options: this.getCategories,
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
              options: this.getSources,
            },
            {
              label: "Laagnaam",
              id: "layer_name",
              name: "LayerName",
              type: "text",
              required: true,
            },
            {
              label: "Brontype",
              id: "source_type",
              name: "SourceType",
              type: "dropdown",
              required: false,
              placeholder: "brontype",
              options: this.sourceTypes,
            },
            {
              label: "Projectie",
              id: "projection",
              name: "Projection",
              type: "text",
              required: true,
            },
            {
              label: "Servertype",
              id: "server_type",
              name: "ServerType",
              type: "text",
              required: true,
            },
            {
              label: "Formaat",
              id: "format",
              name: "Format",
              type: "dropdown",
              required: true,
              placeholder: "bron",
              options: this.formats,
            },
          ],
        },
        display: {
          label: "Weergave",
          questions: [
            {
              label: "Titel",
              id: "title",
              name: "Title",
              type: "text",
              required: true,
            },
          ],
        },
        metadata: {
          label: "Metadata",
          questions: [
            {
              label: "Titel",
              id: "title",
              name: "Title",
              type: "text",
              required: true,
            },
          ],
        },
        access: {
          label: "Toegang",
          questions: [
            {
              label: "Titel",
              id: "title",
              name: "Title",
              type: "text",
              required: true,
            },
          ],
        },
        linkedData: {
          label: "Gekoppelde data",
          questions: [
            {
              label: "Titel",
              id: "title",
              name: "Title",
              type: "text",
              required: true,
            },
          ],
        },
        templates: {
          label: "Templates",
          questions: [],
        },
      };
    },
  },
};
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  width: 100%;
  max-width: 1280px;
  margin: 0 auto;
}

.config-btn-wrapper {
  display: flex;
  justify-content: flex-end;
  gap: 20px;
  padding: 30px 0;
}
</style>
