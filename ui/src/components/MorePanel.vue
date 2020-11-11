<template>
  <div class="wrapper">
    <button class="iconbutton" v-bind:class="{ isOpen }" @click="toggle" aria-label="Meer..."><svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M12 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"/></svg></button>
    <div class="menu" v-if="isOpen">
      <ul>
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
  position: fixed;
  top: 16px;
  right: 16px;
}

.iconbutton {
  width: 40px;
  height: 40px;
  background: white;
  border-radius: 6px;
  box-shadow: 0 0 4px rgba(0,0,0,.1), 0 0 12px rgba(0,0,0,.15);
}

.iconbutton.isOpen {
  border-bottom-left-radius: 0;
  border-bottom-right-radius: 0;
}

.menu {
  position: absolute;
  top: 40px;
  right: 0;
  padding: 8px 12px;
  background: white;
  border-radius: 3px;
  border-top-right-radius: 0;
  box-shadow: 0 0 4px rgba(0,0,0,.1), 0 0 12px rgba(0,0,0,.15);
}
</style>
