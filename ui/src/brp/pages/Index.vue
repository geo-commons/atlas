<template>
    <div class="container">
        <div class="section">
            <form method="POST" @submit="onSearch">
                <input type="text" name="geslachtsnaam" placeholder="Geslachtsnaam" v-model="geslachtsnaam" />
                <input type="text" name="voornamen" placeholder="Voornamen" v-model="voornamen" />
                <input type="text" name="burgerservicenummer" placeholder="Burgerservicenummer" v-model="burgerservicenummer" />
                <input type="text" name="geboortedatum" placeholder="Geboortedatum" v-model="geboortedatum" />
                <button type="submit">Zoek</button>
            </form>
            <div>
                {{ error }}
            </div>
            <div>
                {{ data }}
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'IndexPage',
    data() {
        return {
            geslachtsnaam: '',
            voornamen: '',
            burgerservicenummer: '',
            geboortedatum: '',
            data: '',
            error: ''
        }
    },
    methods: {
        async onSearch(e) {
            e.preventDefault()

            this.error = ''

            let queryData = {}
            if (this.geslachtsnaam && this.geboortedatum) {
                queryData = {
                    fields: ["burgerservicenummer","geslacht","naam", "geboorte"],
                    type: 'ZoekMetGeslachtsnaamEnGeboortedatum',
                    geslachtsnaam: this.geslachtsnaam,
                    geboortedatum: this.geboortedatum
                }
            } else if (this.voornamen && this.geslachtsnaam) {
                queryData = {
                    fields: ["burgerservicenummer","geslacht","naam", "geboorte"],
                    type: 'ZoekMetNaamEnGemeenteVanInschrijving',
                    voornamen: this.voornamen,
                    geslachtsnaam: this.geslachtsnaam,
                    gemeenteVanInschrijving: '0599'
                }
            } else if (this.burgerservicenummer) {
                queryData = {
                    fields: ["burgerservicenummer","geslacht","naam", "geboorte"],
                    type: 'RaadpleegMetBurgerservicenummer',
                    burgerservicenummer: [ this.burgerservicenummer ]
                }
            } else {
                this.error = 'Vol een combinatie van geslachtsnaam + geboortedatum, voornamen + geslachtsnaam of burgerservicenummer in.'
                return
            }

            const result = await fetch('http://localhost:9000/personen', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(queryData)
            })
            const data = await result.json()
            this.data = data
        }
    }
}
</script>

<style scoped>
.buttons {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    row-gap: 14px;
    column-gap: 14px;
}
</style>
