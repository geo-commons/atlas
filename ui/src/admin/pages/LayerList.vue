<template>
  <div class="container">
    <div class="section">
      <router-link to="/layer/create" class="button __tertiary __large">
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
        Maak laag
      </router-link>
    </div>
    <div class="section">Lijst met lagen</div>
  </div>
</template>

<script>
export default {
  name: "LayerList",
  data() {
    return {
      sources: [],
    };
  },
  created() {},
  methods: {},
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
