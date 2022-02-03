<template>
    <div class="content">
        <form method="POST" @submit="saveMap">
            <input
                type="text"
                name="title"
                class="input"
                placeholder="Titel van de kaart"
                v-model="title"
            />
            <input type="text" name="slug" class="input" placeholder="Kenmerk" v-model="slug" />

            <div>
                <button type="button" @click="() => this.$emit('show-layers')">Lagen</button>
            </div>

            <div>
                <input id="features.searchbar" type="checkbox" name="features.searchbar" />
                <label for="features.searchbar">Toon zoekbalk</label>
            </div>

            <div>
                <input id="features.scale" type="checkbox" name="features.scale" />
                <label for="features.scale">Toon schaal</label>
            </div>

            <div>
                <input id="features.measure" type="checkbox" name="features.measure" />
                <label for="features.measure">Opmeten</label>
            </div>

            <div>
                <input id="features.selectarea" type="checkbox" name="features.selectarea" />
                <label for="features.selectarea">Selecteer gebied</label>
            </div>

            <div>
                <input id="features.gps" type="checkbox" name="features.gps" />
                <label for="features.gps">GPS knop</label>
            </div>

            <div>
                <input id="features.streetview" type="checkbox" name="features.streetview" />
                <label for="features.streetview">Rondkijkfoto / obliek</label>
            </div>

            <div>
                <input id="features.zoom" type="checkbox" name="features.zoom" />
                <label for="features.zoom">Zoomfunctie</label>
            </div>

            <router-link to="/maps">Annuleren</router-link>
            <button type="submit">Opslaan</button>
        </form>
    </div>
</template>

<script>
import Cookies from 'js-cookie'

export default {
    name: 'Features',
    data() {
        return {
            title: '',
            slug: '',
        }
    },
    methods: {
        async saveMap(e) {
            e.preventDefault()

            const result = await fetch('/atlas/api/v1/maps/', {
                method: 'POST',
                credentials: 'same-origin',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': Cookies.get('csrftoken'),
                },
                body: JSON.stringify({
                    title: this.title,
                    slug: this.slug,
                }),
            })

            if (result.ok) {
                this.$router.push(`/maps`)
            }
        },
    },
    watch: {
        title: function (newValue) {
            let output = newValue.slice() // create a copy of the string
            output = output.replace(/^\s+|\s+$/g, '') // trim
            output = output.toLowerCase()

            // remove accents, swap ñ for n, etc
            const from = 'àáãäâèéëêìíïîòóöôùúüûñç·/_,:;'
            const to = 'aaaaaeeeeiiiioooouuuunc------'

            for (var i = 0, l = from.length; i < l; i++) {
                output = output.replace(new RegExp(from.charAt(i), 'g'), to.charAt(i))
            }

            output = output
                .replace(/[^a-z0-9 -]/g, '') // remove invalid chars
                .replace(/\s+/g, '-') // collapse whitespace and replace by -
                .replace(/-+/g, '-') // collapse dashes

            this.slug = output
        },
    },
}
</script>

<style scoped>
.content {
    width: 100%;
}
.input {
    width: 100%;
}
</style>
