<template>
  <div>
    <div class="input-group">
      <input type="text" ref="input" name="embedCode" class="form-control" :value="embedCode" readonly="readonly" />
      <span class="input-group-btn">
        <button class="btn btn-default" type="button" @click="copyHTML">{{ buttonText }}</button>
      </span>
    </div>

    <iframe :src="embedUrl" width="100%" height="450" frameborder="0" style="border:0;" allowfullscreen="" aria-hidden="false" tabindex="0"></iframe>
  </div>
</template>

<script>
export default {
  name: 'EmbedCode',
  components: {},
  data: () => {
    return {
      buttonText: "HTML kopiëren"
    }
  },
  computed: {
    embedUrl() {
      return `${encodeURI(window.location.origin)}/atlas/embed/@${encodeURIComponent(this.position.center[0])},${encodeURIComponent(this.position.center[1])},${encodeURIComponent(this.position.zoom)}z/layers=${this.layers.map((l) => encodeURIComponent(l)).join(',')}`
    },
    embedCode() {
      return `<iframe src="${this.embedUrl}" width="560" height="450" frameborder="0" style="border:0;" allowfullscreen="" aria-hidden="false" tabindex="0"></iframe>`
    },
    position() {
      return this.$store.state.position
    },
    layers() {
      return this.$store.state.layers
    }
  },
  methods: {
    copyHTML() {
      if (!this.$refs.input) {
        return
      }

      this.$refs.input.select()

      try {
        document.execCommand('copy')

        this.buttonText = "Gekopieerd!"
        setTimeout(() => {
          this.buttonText = "HTML kopiëren"
        }, 2000)
      } catch (err) {
        console.error('Could not copy text')
      }
    }
  }
}
</script>

<style scoped>
.input-group {
  margin-bottom: 1rem;
}
</style>
