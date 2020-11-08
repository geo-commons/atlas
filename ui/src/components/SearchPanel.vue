<template>
  <div>
    <form method="GET" @submit="onSearch">
      <input v-model="query" @keyup="onSearch" type="text" name="search" placeholder="Zoek adres.." />
      <button type="submit">Zoek</button>
    </form>
    <span v-if="this.error">Er is een fout opgetreden, probeer het opnieuw.</span>
    <div v-if="this.results">
      <ul>
        <li v-for="result in results" v-bind:key="result.id">
          <a href="#">{{ result.weergavenaam }}</a>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
const suggestEndpoint = 'https://geodata.nationaalgeoregister.nl/locatieserver/v3/suggest'

export default {
  name: 'SearchPanel',
  data() {
    return {
      query: '',
      error: false,
      results: []
    }
  },
  methods: {
    async onSearch(e) {
      e.preventDefault()

      this.error = false
      this.results = []

      if (!this.query) {
        return
      }

      try {
        const result = await fetch(`${suggestEndpoint}?fq=gemeentenaam:(purmerend)&q=${encodeURIComponent(this.query)}`)
        const data = await result.json()

        this.results = data.response.docs
      } catch(e) {
        console.error(e)
        this.error = true
      }
    }
  },
}
</script>

<style scoped>
</style>
