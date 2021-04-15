<template>
  <div>
    <span v-if="this.valueType === 'STRING'">{{ dataValue }}</span>
    <a v-if="this.valueType === 'URL'" :href="dataValue" target="_blank" rel="noopener">{{ dataValue }}</a>
    <img v-if="this.valueType === 'IMAGE'" :src="dataValue" :alt="`Afbeelding ${dataKey}`" />
  </div>
</template>

<script>
const imageRegex = /^(http|https).*(\.jpg|\.jpeg|\.png|\.gif)/
const urlRegex = /^(http|https)/

export default {
  name: 'RichValue',
  components: {},
  computed: {
    valueType() {
      if (typeof this.dataValue !== 'string') {
        return 'STRING'
      }

      if (this.dataValue.match(imageRegex)) {
        return 'IMAGE'
      }

      if (this.dataValue.match(urlRegex)) {
        return 'URL'
      }

      return 'STRING'
    }
  },
  props: {
    dataKey: String,
    dataValue: [String, Number]
  }
}
</script>