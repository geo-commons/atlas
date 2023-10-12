<template>
  <div class="container">
    <div class="section">
      <h2>Configureer laag</h2>
      <validation-observer v-slot="{ handleSubmit }">
        <form v-if="data" @submit.prevent="handleSubmit(saveLayer)">
          <div>
            <validation-provider v-slot="{ errors }" name="Titel">
              <label for="title">Titel</label>
              <input id="title" v-model="data.title" type="text" required />
              <span>{{ errors[0] }}</span>
            </validation-provider>
          </div>

          <div class="flexer">
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
    };
  },
  created() {
    this.getLayer();
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
