<template>
  <div class="wrapper">
      <form class="search" autocomplete="off" method="GET" @submit="onSearch">
        <input v-model="query" @keyup="onSearch" type="text" name="search" placeholder="Zoek adres.." />
        <button class="iconbutton" type="submit" :disabled="!this.query" aria-label="Zoek"><svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg></button>
      </form>
      <span v-if="this.error">Er is een fout opgetreden, probeer het opnieuw.</span>
      <div class="results" v-if="this.showResults && results.length">
        <ul class="list">
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
        this.showResults = false
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
.wrapper {
  position: fixed;
  top: 16px;
  left: 16px;
  width: 320px;
  background: white;
  border-radius: 6px;
  overflow: hidden;
  box-shadow: 0 0 4px rgba(0,0,0,.1), 0 0 12px rgba(0,0,0,.15);
}

.search {
  display: flex;
  height: 40px;
  width: 100%;
}

.search input {
  width: 100%;
  height: 100%;
  padding-left: 16px;
}

.search button {
  flex-shrink: 0;
  width: 48px;
  height: 100%;
}

.results {
  width: 100%;
  border-top: 1px solid #EAEAEA;
  padding: 12px 0;
}

.list a {
  display: block;
  color: #4285F4;
  text-decoration: none;
  padding: 3px 16px;
}

.list a:hover {
  text-decoration: underline;
}
</style>
