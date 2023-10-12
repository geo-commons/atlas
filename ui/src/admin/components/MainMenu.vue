<template>
  <div class="header container">
    <div class="nav">
      <router-link to="/">
        <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 0 24 24" width="24px" fill="#000000">
          <path d="M0 0h24v24H0V0z" fill="none" />
          <path d="M19 5v2h-4V5h4M9 5v6H5V5h4m10 8v6h-4v-6h4M9 17v2H5v-2h4M21 3h-8v6h8V3zM11 3H3v10h8V3zm10 8h-8v10h8V11zm-10 4H3v6h8v-6z" />
        </svg>
        <span v-if="$route.path === '/'" class="dashboard-title">{{ $route.meta.title }}</span>
      </router-link>
      <div v-if="$route.path !== '/'">
        <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 0 24 24" width="24px" fill="currentColor" class="chevron-icon">
          <path d="M0 0h24v24H0V0z" fill="none" />
          <path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6-6-6z" />
        </svg>
        <span class="title">{{ $route.meta.title }}</span>
      </div>
    </div>

    <a href="/atlas/admin/logout/" class="logout">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        enable-background="new 0 0 24 24"
        height="24px"
        viewBox="0 0 24 24"
        width="24px"
        fill="currentColor"
        class="logout-icon"
      >
        <g><path d="M0,0h24v24H0V0z" fill="none" /></g>
        <g>
          <path d="M17,8l-1.41,1.41L17.17,11H9v2h8.17l-1.58,1.58L17,16l4-4L17,8z M5,5h7V3H5C3.9,3,3,3.9,3,5v14c0,1.1,0.9,2,2,2h7v-2H5V5z" />
        </g>
      </svg>
    </a>
  </div>
</template>

<script>
export default {
  name: "MainMenu",
};
</script>

<style scoped>
.header {
  min-height: 56px;
  display: flex;
  align-items: stretch;
  justify-content: space-between;
  box-shadow: 0 1px 0 var(--color-grey-60);
}

.nav {
  display: flex;
  align-items: center;
}

.nav > * {
  height: 100%;
  display: flex;
  align-items: center;
  text-decoration: none;
  color: black;
  font-size: var(--font-size-large);
  font-weight: var(--font-weight-bold);
}

.chevron-icon,
.logout-icon {
  color: var(--color-icon-grey);
}

.dashboard-title {
  margin-left: 8px;
}

.logout {
  display: flex;
  align-items: center;
}
</style>
