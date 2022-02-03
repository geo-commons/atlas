<template>
    <div class="container">
        <router-link to="/maps/create">Maak kaart</router-link>
        <ul>
            <li v-bind:key="map.id" v-for="map in maps">{{ map.title }}</li>
        </ul>
    </div>
</template>

<script>
export default {
    name: 'MapList',
    created() {
        this.getMaps()
    },
    methods: {
        async getMaps() {
            const result = await fetch('/atlas/api/v1/maps/', {
                credentials: 'same-origin',
                headers: { 'Content-Type': 'application/json' },
            })

            if (!result.ok) {
                console.error('Could not fetch maps')
            }

            this.maps = await result.json()
        },
    },
    data() {
        return {
            maps: [],
        }
    },
}
</script>

<style scoped>
.container {
    padding: 14px 32px;
}
</style>
