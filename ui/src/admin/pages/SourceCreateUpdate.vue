<template>
  <div class="container">
    <div class="section">
      <validation-observer v-slot="{ handleSubmit }">
        <form v-if="data" @submit.prevent="handleSubmit(saveSource)">
          <div>
            <validation-provider v-slot="{ errors }" name="Titel">
              <label for="title">Titel</label>
              <input id="title" v-model="data.title" type="text" required />
              <span>{{ errors[0] }}</span>
            </validation-provider>
          </div>

          <div>
            <validation-provider v-slot="{ errors }" name="URL">
              <label for="url">URL</label>
              <input id="url" v-model="data.url" type="url" required />
              <span>{{ errors[0] }}</span>
            </validation-provider>
          </div>

          <div>
            <validation-provider
              v-slot="{ errors }"
              name="Verstuur authenticatieinformatie naar bron"
            >
              <input
                id="authenticate"
                v-model="data.authenticate"
                type="checkbox"
              />
              <label for="authenticate"
                >Verstuur authenticatieinformatie naar bron</label
              >
              <span>{{ errors[0] }}</span>
            </validation-provider>
          </div>

          <div class="flexer">
            <router-link to="/sources" class="button __tertiary"
              >Annuleer</router-link
            >
            <button class="button __primary" type="submit">Opslaan</button>
          </div>
        </form>
      </validation-observer>
    </div>
    <h2>Layers</h2>
    <ul>
      <li v-for="(layer, i) in layersFromCapabilities" :key="i">
        {{ layer.Name }}
      </li>
    </ul>
  </div>
</template>

<script>
import Cookies from "js-cookie";
import { ValidationObserver, ValidationProvider } from "vee-validate";
import WMSCapabilities from "ol/format/WMSCapabilities.js";

const wmsCapabilitiesParser = new WMSCapabilities();

export default {
  name: "SourceCreateUpdate",
  components: {
    ValidationObserver,
    ValidationProvider,
  },
  data() {
    return {
      data: null,
      layersFromCapabilities: [],
    };
  },
  watch: {
    data(value) {
      if (!value || !value.url) {
        return;
      }

      this.getCapabilities(value.url);
    },
  },
  created() {
    this.getSource();
  },
  methods: {
    async getSource() {
      if (this.$route.params.id) {
        const result = await fetch(
          `/atlas/api/v1/sources/${this.$route.params.id}/`,
          {
            credentials: "same-origin",
            headers: { "Content-Type": "application/json" },
          }
        );

        if (!result.ok) {
          console.error("Could not fetch source");
        }

        this.data = await result.json();
        return;
      }

      this.data = {
        title: "",
        url: "",
        authenticate: false,
      };
    },
    async saveSource() {
      let result;

      if (this.$route.params.id) {
        result = await fetch(
          `/atlas/api/v1/sources/${this.$route.params.id}/`,
          {
            method: "PUT",
            credentials: "same-origin",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": Cookies.get("csrftoken"),
            },
            body: JSON.stringify(this.data),
          }
        );
      } else {
        result = await fetch(`/atlas/api/v1/sources/`, {
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
        this.$router.push(`/sources`);
      }
    },
    async getCapabilities(url) {
      const params = new URLSearchParams([
        ["service", "WMS"],
        ["version", "1.3.0"],
        ["request", "GetCapabilities"],
      ]);

      const parsedUrl = new URL(url);
      parsedUrl.search = params.toString();

      const result = await fetch(parsedUrl.toString());
      const text = await result.text();
      const wmsResult = wmsCapabilitiesParser.read(text);
      this.layersFromCapabilities = wmsResult.Capability.Layer.Layer;
    },
  },
};
</script>

<style scoped>
.flexer {
  display: flex;
  margin-top: 20px;
  justify-content: left;
}

.section {
  max-width: 600px;
}
</style>
