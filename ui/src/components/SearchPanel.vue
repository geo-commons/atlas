<template>
 <transition name="fade">
  <div class="wrapper">
    <Search :showSuggestions="showSuggestions" @show-data-panel="toggleDataPanel" @on-submit="onSearch">
      <template v-slot:default>
        <input v-model="query" @keyup="onSearch" type="search" name="search" placeholder="Zoek adres" autocomplete="off" aria-autocomplete="list" role="combobox" aria-owns="search-results" :aria-expanded="showSuggestions && results.length" />
      </template>

      <template v-slot:suggestions>
        <div class="results" v-if="showSuggestions && results.length">
          <ul class="list" id="search-results" role="listbox">
            <li role="option" tabindex="-1" aria-selected="false" v-for="result in results" :key="result.id" @click="(e) => onNavigate(e, result.id)">
              <a href="#">{{ result.weergavenaam }}</a>
            </li>
          </ul>
        </div>
      </template>
    </Search>
  </div>
  </transition>
</template>

<script>
import Search from './Search'

const suggestEndpoint = 'https://geodata.nationaalgeoregister.nl/locatieserver/v3/suggest'
const freeEndpoint = 'https://geodata.nationaalgeoregister.nl/locatieserver/v3/free'

export default {
  name: 'SearchPanel',
  components: {
    Search,
  },
  data() {
    return {
      showSuggestions: false,
      results: []
    }
  },
  computed: {
    query: {
      get() {
        return this.$store.state.searchQuery
      },
      set(value) {
        this.$store.commit('setSearchQuery', value)
      }
    }
  },
  props: {
    position: Object,
  },
  methods: {
    toggleDataPanel() {
      this.$emit('toggle-data-panel')
    },
    async onSearch() {
      this.results = []

      if (!this.query) {
        this.$emit('set-position', { ...this.position, marker: null })
        this.showSuggestions = false
        return
      }

      try {
        const result = await fetch(`${suggestEndpoint}?fq=${encodeURIComponent(`gemeentenaam:utrecht`)}&q=${encodeURIComponent(this.query)}`)
        const data = await result.json()

        this.showSuggestions = true
        this.results = data.response.docs
      } catch(e) {
        console.error(e)
        this.$store.commit('setAlert', 'Er is een fout opgetreden, controleer de verbinding en probeer het opnieuw.')
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
          center: parsedCenteroide,
          zoom: 19
        })

        this.query = object.weergavenaam
        this.showSuggestions = false
      } catch(e) {
        console.error(e)
        this.$store.commit('setAlert', 'Er is een fout opgetreden, controleer de verbinding en probeer het opnieuw.')
      }
    },
  },
}
</script>

<style scoped>
.wrapper {
  position: fixed;
  z-index: 1;
  left: 0;
  padding: var(--padding-screen);
  padding-bottom: 0;
  width: var(--width-detail);
  max-width: 100%;
}
</style>
