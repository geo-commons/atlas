<template>
  <div class="container">
    <div class="section">
      <router-link to="/maps/create" class="button __tertiary __large">
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
        Maak kaart
      </router-link>
    </div>
    <div class="section">
      <ul>
        <li v-for="map in maps" :key="map.id" class="map">
          <router-link :to="`/maps/update/${map.id}`">{{
            map.title
          }}</router-link>
          <div class="buttons">
            <button
              v-tippy="{ placement: 'bottom' }"
              class="iconbutton"
              aria-label="Bekijk kaart"
              content="Bekijk"
              type="button"
              @click="gotoMap(map)"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                height="24"
                viewBox="0 96 960 960"
                width="24"
              >
                <path
                  d="M480.118 726Q551 726 600.5 676.382q49.5-49.617 49.5-120.5Q650 485 600.382 435.5q-49.617-49.5-120.5-49.5Q409 386 359.5 435.618q-49.5 49.617-49.5 120.5Q310 627 359.618 676.5q49.617 49.5 120.5 49.5Zm-.353-58Q433 668 400.5 635.265q-32.5-32.736-32.5-79.5Q368 509 400.735 476.5q32.736-32.5 79.5-32.5Q527 444 559.5 476.735q32.5 32.736 32.5 79.5Q592 603 559.265 635.5q-32.736 32.5-79.5 32.5ZM480 856q-146 0-264-83T40 556q58-134 176-217t264-83q146 0 264 83t176 217q-58 134-176 217t-264 83Zm0-300Zm-.169 240Q601 796 702.5 730.5 804 665 857 556q-53-109-154.331-174.5-101.332-65.5-222.5-65.5Q359 316 257.5 381.5 156 447 102 556q54 109 155.331 174.5 101.332 65.5 222.5 65.5Z"
                />
              </svg>
            </button>
            <button
              v-tippy="{ placement: 'bottom' }"
              class="iconbutton"
              aria-label="Verwijder kaart"
              content="Verwijder"
              type="button"
              @click="deleteMap(map)"
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
  name: "MapList",
  data() {
    return {
      maps: [],
    };
  },
  created() {
    this.getMaps();
  },
  methods: {
    async getMaps() {
      const result = await fetch("/atlas/api/v1/maps/", {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch maps");
      }

      this.maps = await result.json();
    },
    gotoMap(map) {
      window.location.href = `/atlas/maps/${map.slug}`;
    },
    async deleteMap(map) {
      const acknowledged = confirm(
        "Weet je zeker dat je de kaart wil verwijderen?"
      );
      if (!acknowledged) {
        return;
      }

      const result = await fetch(`/atlas/api/v1/maps/${map.id}/`, {
        method: "DELETE",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": Cookies.get("csrftoken"),
        },
      });

      if (result.ok) {
        this.getMaps();
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

.map {
  display: flex;
  align-items: center;
  border: 2px solid var(--color-grey-60);
  border-radius: var(--radius-normal);
  margin-top: 16px;
}

.map a {
  padding: 12px 0 12px 20px;
  flex-grow: 1;
  font-size: var(--font-size-normal);
  font-weight: var(--font-weight-bold);
  color: var(--color-primary);
  text-decoration: none;
}

.map a:hover,
.map a:focus {
  text-decoration: underline;
}

.map .iconbutton {
  margin-right: 8px;
  width: 40px;
  height: 40px;
  border-radius: 50%;
}
</style>
