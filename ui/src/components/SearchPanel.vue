<template>
 <transition name="fade">
  <div class="wrapper" v-if="showSearchPanel">
    <div class="search-wrapper">
      <form class="search" autocomplete="off" method="GET" @submit="onSearch">
        <input v-model="query" @keyup="onSearch" type="text" name="search" placeholder="Zoek adres.." autocomplete="off" aria-autocomplete="list" role="combobox" aria-owns="search-results" :aria-expanded="this.showResults && results.length" />
        <div class="buttons">
          <button class="iconbutton search-button" type="submit" :disabled="!this.query" v-tippy='{ placement : "bottom", theme: "primary" }' content="Zoek" aria-label="Zoek">
            <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24"><path d="M0 0h24v24H0V0z" fill="none"/><path fill="currentColor" d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>
          </button>

          <button v-if="showInfoPanel" type="button" class="iconbutton clear-button" @click="clearPosition" v-tippy='{ placement : "bottom" }' content="Wis selectie" aria-label="Wis selectie">
            <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24"><path d="M0 0h24v24H0z" fill="none"/><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>
          </button>
        </div>
      </form>
      <span v-if="this.error">Er is een fout opgetreden, probeer het opnieuw.</span>
      <div class="results" v-if="this.showResults && results.length">
        <ul class="list" id="search-results" role="listbox">
          <li role="option" tabindex="-1" aria-selected="false" v-for="result in results" :key="result.id" @click="(e) => onNavigate(e, result.id)">
            <a href="#">{{ result.weergavenaam }}</a>
          </li>
        </ul>
      </div>
    </div>
  </div>
  </transition>
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
    showInfoPanel: Boolean,
    showSearchPanel: Boolean,
  },
  methods: {
    clearPosition() {
      this.query = ''
      this.$emit('set-position', { ...this.position, marker: null })
    },

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
  z-index: 2;
  left: 0;
  padding: var(--padding-screen);
  padding-bottom: 0;
  width: var(--width-detail);
  max-width: 100%;
}

.search-wrapper {
  width: 100%;
  background: white;
  border-radius: var(--radius-normal);
  overflow: hidden;
  border: 1px solid transparent;
  box-shadow: var(--shadow-normal);
  transition: border-color .1s, box-shadow .1s;
}

.showInfoPanel .search-wrapper{
  border-color: var(--color-grey-60);
  box-shadow: none;
}

.search {
  display: flex;
  /* Subtract search-wrapper border */
  height: calc(var(--width-button-large) - 2px);
  width: 100%;
}

.search input {
  width: 100%;
  height: 100%;
  padding-left: 16px;
}

.buttons {
  flex-shrink: 0;
  display: flex;
  height: 100%;
}

.search-button {
  width: 48px;
}

.showInfoPanel .search-button {
  width: var(--width-button-large);
}

.search-button:not([disabled]) {
  background: transparent;
  color: var(--color-primary);
}

.clear-button {
  width: var(--width-button-large);
  border-left: 1px solid var(--color-grey-50);
}

.open-button {
  width: 24px;
  height: var(--width-button-large);
  border-left: 1px solid var(--color-grey-50);
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
