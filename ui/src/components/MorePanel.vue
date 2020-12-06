<template>
  <div class="wrapper">
    <button class="iconbutton" :class="{ isOpen }" @click="toggle" aria-label="Meer..."><svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M12 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"/></svg></button>
    <div class="menu" v-if="isOpen">
      <ul class="list">
        <li><a href="#">Log in</a></li>
        <li><a href="#">Help</a></li>
        <li><a href="#">Print</a></li>
        <li><a href="#">Deel</a></li>
        <li><a href="#">Embed</a></li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MorePanel',
  data() {
    return {
      isOpen: false
    }
  },
  methods: {
    toggle() {
      this.isOpen = !this.isOpen
    }
  }
}
</script>

<style scoped>
.wrapper {
  position: relative;
}

.iconbutton {
  width: var(--width-button-normal);
  height: var(--width-button-normal);
  background: white;
  border-radius: var(--radius-small);
  box-shadow: var(--shadow-normal);
}

.iconbutton.isOpen {
  border-bottom-left-radius: 0;
  border-bottom-right-radius: 0;
}

.menu {
  position: absolute;
  top: var(--width-button-normal);
  right: 0;
  padding: 6px 0;
  background: white;
  border-radius: var(--radius-small);
  border-top-right-radius: 0;
  box-shadow: var(--shadow-normal);
}

.list a {
  display: block;
  color: black;
  text-decoration: none;
  padding: 2px 12px;
  font-size: var(--font-size-small);
}

.list a:hover {
  background: #F5F5F5;
}

.list a:active {
  background: #EAEAEA;
}
</style>
