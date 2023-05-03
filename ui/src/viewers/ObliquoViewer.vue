<template>
  <iframe :src="src" class="iframe"></iframe>
</template>

<script>
export default {
  name: "ObliquoViewer",
  props: {
    position: Object,
    url: String,
    username: String,
    password: String,
  },
  data() {
    return {
      token: "",
      src: "",
    };
  },
  watch: {
    async position(newValue, oldValue) {
      if (newValue.marker === oldValue.marker) {
        return;
      }

      this.src = await this.getLink(newValue.marker);
    },
  },
  async mounted() {
    await this.getLoginToken();

    if (this.position.marker) {
      this.src = await this.getLink(this.position.marker);
    }
  },
  methods: {
    resize() {
      // iframe resize is not required
    },
    async getLoginToken() {
      const loginUrl = new URL(this.url);
      loginUrl.pathname = "/manager/auth";

      const loginParameters = {
        email: this.username,
        password: this.password,
      };

      const loginResult = await fetch(loginUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(loginParameters),
      });

      if (!loginResult.ok) {
        console.error("Could not login to Obliquo", loginResult);
        return;
      }

      const loginData = await loginResult.json();

      this.token = loginData.token;
    },
    async getLink(position) {
      if (!this.token) {
        return;
      }

      const elinkUrl = new URL(this.url);
      elinkUrl.pathname = "/manager/elink";

      const elinkParameters = {
        x: position[0],
        y: position[1],
        srid: 28992,
      };

      const elinkResult = await fetch(elinkUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${this.token}`,
        },
        body: JSON.stringify(elinkParameters),
      });

      if (!elinkResult.ok) {
        console.error("Could not fetch elink for Obliquo", elinkResult);
        return;
      }

      const elinkData = await elinkResult.json();

      const linkParams = new URLSearchParams([["e", elinkData.linkID]]);

      const linkUrl = new URL(this.url);
      linkUrl.pathname = "";
      linkUrl.search = linkParams;

      return linkUrl.toString();
    },
  },
};
</script>

<style scoped>
.iframe {
  width: 100%;
  height: 100%;
}
</style>
