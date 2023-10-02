<template>
  <div class="container">
    <div class="section">
      <div class="buttons">
        <router-link to="/maps" class="button __tertiary __large"
          ><svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 0 24 24" width="24px" fill="#000000">
            <path d="M0 0h24v24H0V0z" fill="none" />
            <path
              d="M20.5 3l-.16.03L15 5.1 9 3 3.36 4.9c-.21.07-.36.25-.36.48V20.5c0 .28.22.5.5.5l.16-.03L9 18.9l6 2.1 5.64-1.9c.21-.07.36-.25.36-.48V3.5c0-.28-.22-.5-.5-.5zM10 5.47l4 1.4v11.66l-4-1.4V5.47zm-5 .99l3-1.01v11.7l-3 1.16V6.46zm14 11.08l-3 1.01V6.86l3-1.16v11.84z"
            /></svg
          >Kaarten</router-link
        >
        <router-link to="/sources" class="button __tertiary __large"
          ><svg xmlns="http://www.w3.org/2000/svg" enable-background="new 0 0 24 24" height="24px" viewBox="0 0 24 24" width="24px" fill="#000000">
            <g>
              <rect fill="none" height="24" width="24" />
              <path
                d="M20,6h-8l-2-2H4C2.9,4,2.01,4.9,2.01,6L2,18c0,1.1,0.9,2,2,2h16c1.1,0,2-0.9,2-2V8C22,6.9,21.1,6,20,6z M20,18L4,18V6h5.17 l2,2H20V18z M18,12H6v-2h12V12z M14,16H6v-2h8V16z"
              />
            </g></svg
          >Bronnen</router-link
        >
        <!--        <router-link to="/layers" class="button __tertiary __large"-->
        <!--          ><svg data-v-5ec8bae2="" xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24">-->
        <!--            <path data-v-5ec8bae2="" d="M0 0h24v24H0V0z" fill="none"></path>-->
        <!--            <path-->
        <!--              data-v-5ec8bae2=""-->
        <!--              fill="currentColor"-->
        <!--              d="M11.99 18.54l-7.37-5.73L3 14.07l9 7 9-7-1.63-1.27zM12 16l7.36-5.73L21 9l-9-7-9 7 1.63 1.27L12 16zm0-11.47L17.74 9 12 13.47 6.26 9 12 4.53z"-->
        <!--            ></path></svg-->
        <!--          >Lagen</router-link-->
        <!--        >-->
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "AdminDashboard",
};
</script>

<style scoped>
.buttons {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  row-gap: 14px;
  column-gap: 14px;
}
</style>
