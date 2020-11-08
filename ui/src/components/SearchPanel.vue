<template>
  <div>
    <form method="GET" @submit="onSearch">
      <input v-model="query" @keyup="onSearch" type="text" name="search" placeholder="Zoek adres.." />
      <button type="submit">Zoek</button>
    </form>
    <span v-if="this.error">Er is een fout opgetreden, probeer het opnieuw.</span>
    <div v-if="this.showResults && results">
      <ul>
        <li v-for="result in results" v-bind:key="result.id">
          <a href="#" @click="(e) => onNavigate(e, result.id)">{{ result.weergavenaam }}</a>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
const suggestEndpoint = 'https://geodata.nationaalgeoregister.nl/locatieserver/v3/suggest'
const freeEndpoint = 'https://geodata.nationaalgeoregister.nl/locatieserver/v3/free'

export default {
  name: 'SearchPanel',
  data() {
    return {
      query: '',
      error: false,
      showResults: false,
      results: []
    }
  },
  props: {
    position: Object,
  },
  methods: {
    async onSearch(e) {
      e.preventDefault()

      this.error = false
      this.results = []

      if (!this.query) {
        this.$emit('set-position', { ...this.position, marker: null })
        return
      }

      try {
        const result = await fetch(`${suggestEndpoint}?fq=gemeentenaam:(purmerend)&q=${encodeURIComponent(this.query)}`)
        const data = await result.json()

        this.showResults = true
        this.results = data.response.docs
      } catch(e) {
        console.error(e)
        this.error = true
      }
    },
    async onNavigate(e, id) {
      e.preventDefault()

      try {
        const result = await fetch(`${freeEndpoint}?q=${encodeURIComponent('id:' + id)}`)

        const data = await result.json()
        if (!data.response.docs) {
          return
        }

        const object = data.response.docs[0]

        const centeroide = /POINT\(([\d.]+) ([\d.]+)\)/.exec(object.centroide_rd)
        const parsedCenteroide = [ parseFloat(centeroide[1]), parseFloat(centeroide[2]) ]

        this.$emit('set-position', {
          ...this.position,
          marker: parsedCenteroide,
          center: parsedCenteroide,
          zoom: 19
        })

        this.showResults = false
        this.query = object.weergavenaam
      } catch(e) {
        console.error(e)
      }
    }
  },
}
</script>

<style scoped>
</style>
