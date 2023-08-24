<template>
  <div class="container">
    <div class="section">
      <router-link to="/sources/create" class="button __tertiary __large">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          height="24px"
          viewBox="0 0 24 24"
          width="24px"
          fill="#000000"
        >
          <path d="M0 0h24v24H0V0z" fill="none" />
          <path
            d="M13 7h-2v4H7v2h4v4h2v-4h4v-2h-4V7zm-1-5C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z"
          />
        </svg>
        Maak bron
      </router-link>
    </div>
    <div class="section">
      <ul>
        <li v-for="source in sources" :key="source.id" class="source">
          <router-link :to="`/sources/update/${source.id}`">{{
            source.title
          }}</router-link>
          <div class="buttons">
            <button
              v-tippy="{ placement: 'bottom' }"
              class="iconbutton"
              aria-label="Verwijder bron"
              content="Verwijder"
              type="button"
              @click="deleteSource(source)"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                height="24px"
                viewBox="0 0 24 24"
                width="24px"
                fill="#000000"
              >
                <path d="M0 0h24v24H0V0z" fill="none" />
                <path
                  d="M16 9v10H8V9h8m-1.5-6h-5l-1 1H5v2h14V4h-3.5l-1-1zM18 7H6v12c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7z"
                />
              </svg>
            </button>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import Cookies from "js-cookie";

export default {
  name: "SourceList",
  data() {
    return {
      sources: [],
    };
  },
  created() {
    this.getSources();
  },
  methods: {
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
    async deleteSource(source) {
      const acknowledged = confirm(
        "Weet je zeker dat je de bron wil verwijderen?"
      );
      if (!acknowledged) {
        return;
      }

      const result = await fetch(`/atlas/api/v1/sources/${source.id}/`, {
        method: "DELETE",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": Cookies.get("csrftoken"),
        },
      });

      if (result.ok) {
        this.getSources();
      }
    },
  },
};
</script>

<style scoped>
.buttons {
  display: flex;
}

.button {
  max-width: 300px;
}

.source {
  display: flex;
  align-items: center;
  border: 2px solid var(--color-grey-60);
  border-radius: var(--radius-normal);
  margin-top: 16px;
}

.source a {
  padding: 12px 0 12px 20px;
  flex-grow: 1;
  font-size: var(--font-size-normal);
  font-weight: var(--font-weight-bold);
  color: var(--color-primary);
  text-decoration: none;
}

.source a:hover,
.source a:focus {
  text-decoration: underline;
}

.source .iconbutton {
  margin-right: 8px;
  width: 40px;
  height: 40px;
  border-radius: 50%;
}
</style>
