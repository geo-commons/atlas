<template>
  <div class="container">
    <h1>Kaartlaag wijzigen</h1>

    <div class="section">
      <validation-observer v-slot="{ handleSubmit }">
        <form v-if="data" @submit.prevent="handleSubmit(saveLayer)">
          <hr />
          <div class="config-section-wrapper">
            <div><h3>Algemene gegevens</h3></div>

            <div>
              <div>
                <validation-provider v-slot="{ errors }" name="Titel">
                  <label for="title">Titel</label>
                  <input id="title" v-model="data.title" type="text" required />
                  <span>{{ errors[0] }}</span>
                </validation-provider>
              </div>

              <div>
                <validation-provider v-slot="{ errors }" name="Slug">
                  <label for="slug">Kort kenmerk</label>
                  <input id="slug" v-model="data.slug" type="text" required />
                  <span>{{ errors[0] }}</span>
                </validation-provider>
              </div>

              <div>
                <validation-provider v-slot="{ errors }" name="Category" class="flex flex-column">
                  <label for="category">Categorie</label>
                  <select id="category" v-model="data.category" class="" required>
                    <option disabled value="">Selecteer een categorie</option>
                    <option v-for="category in categories" :key="category.id" :value="category">
                      {{ category.title }}
                    </option>
                  </select>
                  <span>{{ errors[0] }}</span>
                </validation-provider>
              </div>
            </div>
          </div>
          <hr />
          <div class="config-section-wrapper">
            <div><h3>Bron</h3></div>
            <div>
              <div>
                <div>{{ data.source }}</div>
                <validation-provider v-slot="{ errors }" name="Source" class="flex flex-column">
                  <label for="source">Bron</label>
                  <select id="source" v-model="data.source" class="" required>
                    <option disabled value="">Selecteer een bron</option>
                    <option v-for="source in sources" :key="source.id" :value="source">
                      {{ source.title }}
                    </option>
                  </select>
                  <span>{{ errors[0] }}</span>
                </validation-provider>
              </div>

              <div>
                <validation-provider v-slot="{ errors }" name="LayerName">
                  <label for="layer-name">Laagnaam</label>
                  <input id="layer-name" v-model="data.layer_name" type="text" />
                  <span>{{ errors[0] }}</span>
                </validation-provider>
              </div>

              <div>
                <validation-provider v-slot="{ errors }" name="SourceType" class="flex flex-column">
                  <label for="source-type">Brontype</label>
                  <select id="source-type" v-model="data.source_type" class="">
                    <option disabled value="">Selecteer een brontype</option>
                    <option v-for="type in sourceTypes" :key="type">
                      {{ type }}
                    </option>
                  </select>
                  <span>{{ errors[0] }}</span>
                </validation-provider>
              </div>

              <div>
                <validation-provider v-slot="{ errors }" name="Projection">
                  <label for="projection">Projectie</label>
                  <input id="projection" v-model="data.projection" type="text" />
                  <span>{{ errors[0] }}</span>
                </validation-provider>
              </div>

              <div>
                <validation-provider v-slot="{ errors }" name="ServerType">
                  <label for="server-type">Servertype</label>
                  <input id="server-type" v-model="data.server_type" type="text" />
                  <span>{{ errors[0] }}</span>
                </validation-provider>
              </div>

              <div>
                <validation-provider v-slot="{ errors }" name="Format" class="flex flex-column">
                  <label for="format">Formaat</label>
                  <select id="format" v-model="data.format" class="">
                    <option disabled value="">Selecteer een formaat</option>
                    <option v-for="format in formats" :key="format">
                      {{ format }}
                    </option>
                  </select>
                  <span>{{ errors[0] }}</span>
                </validation-provider>
              </div>
            </div>
          </div>
          <hr />
          <div class="config-section-wrapper">
            <div><h3>Weergave</h3></div>

            <div></div>
          </div>
          <hr />
          <div class="config-section-wrapper">
            <div><h3>Metadata</h3></div>
            <div>
              <!--                todo: naam metadata niet in api response?-->

              <div>
                <validation-provider v-slot="{ errors }" name="Naam">
                  <label for="name">Naam</label>
                  <input id="name" type="text" />
                  <span>{{ errors[0] }}</span>
                </validation-provider>
              </div>

              <div>
                <validation-provider v-slot="{ errors }" name="Description" class="flex flex-column">
                  <label for="description">Omschrijving</label>
                  <textarea id="description" v-model="data.metadata.description" type="text" />
                  <span>{{ errors[0] }}</span>
                </validation-provider>
              </div>

              <!--              todo: laatst bijgewerkt > waarom is dit een invoerveld? -->
              <div>
                <validation-provider v-slot="{ errors }" name="Updated">
                  <label for="updated">Laatst bijgewerkt</label>
                  <input id="updated" v-model="data.metadata.updated" type="text" />
                  <span>{{ errors[0] }}</span>
                </validation-provider>
              </div>

              <div>
                <validation-provider v-slot="{ errors }" name="Link">
                  <label for="link">Meer informatie</label>
                  <input id="link" v-model="data.metadata.link" type="text" />
                  <span>{{ errors[0] }}</span>
                </validation-provider>
              </div>
            </div>
          </div>
          <hr />
          <div class="config-section-wrapper">
            <div><h3>Toegang</h3></div>

            <div></div>
          </div>

          <div class="config-btn-wrapper">
            <router-link to="/layers" class="button __tertiary">Annuleer</router-link>
            <button class="button __primary" type="submit">Opslaan</button>
          </div>
        </form>
      </validation-observer>
    </div>
  </div>
</template>

<script>
import { ValidationObserver, ValidationProvider } from "vee-validate";

import Cookies from "js-cookie";

export default {
  name: "LayerCreateUpdate",
  components: {
    ValidationObserver,
    ValidationProvider,
  },
  data() {
    return {
      data: null,
      layersFromCapabilities: [],
      categories: {},
      sources: {},
      sourceTypes: [],
      formats: [],
    };
  },
  created() {
    this.getLayer();
    this.getCategories();
    this.getSources();
    this.sourceTypes = ["WMS en WFS", "WMS", "WFS", "WMTS", "XYZ", "MVT"];
    this.formats = ["image/png", "image/jpeg", "image/vnd.jpeg-png"];
  },
  methods: {
    async getLayer() {
      if (this.$route.params.id) {
        const result = await fetch(`/atlas/api/v1/layers/${this.$route.params.id}/`, {
          credentials: "same-origin",
          headers: { "Content-Type": "application/json" },
        });

        if (!result.ok) {
          console.error("Could not fetch layer");
        }

        this.data = await result.json();
        console.log(this.data);
        return;
      }

      this.data = {
        title: "",
        url: "",
        authenticate: false,
      };
    },
    async saveLayer() {
      let result;

      if (this.$route.params.id) {
        result = await fetch(`/atlas/api/v1/layers/${this.$route.params.id}/`, {
          method: "PUT",
          credentials: "same-origin",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": Cookies.get("csrftoken"),
          },
          body: JSON.stringify(this.data),
        });
      } else {
        result = await fetch(`/atlas/api/v1/layers/`, {
          method: "POST",
          credentials: "same-origin",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": Cookies.get("csrftoken"),
          },
          body: JSON.stringify(this.data),
        });
      }

      if (result.ok) {
        this.$router.push(`/layers`);
      }
    },
    async getCategories() {
      const result = await fetch("/atlas/api/v1/categories/", {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch categories");
      }

      this.categories = await result.json();
    },
    async getSources() {
      const result = await fetch("/atlas/api/v1/sources/", {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch sources");
      }

      this.sources = await result.json();
    },
  },
};
</script>

<style scoped>
/*todo: move*/
input {
  background: var(--color-white);
}

.container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  width: 100%;
  max-width: 1280px;
  margin: 0 auto;
}

.config-section-wrapper {
  display: grid;
  grid-template-columns: 1fr 1fr;
}

.config-btn-wrapper {
  display: flex;
  justify-content: flex-end;
  gap: 20px;
}

.section {
  max-width: 600px;
}
</style>
