<template>
    <iframe :src="src" class="iframe"></iframe>
</template>

<script>
export default {
    name: 'Obliquo',
    methods: {
        resize() {
            // iframe resize is not required
        },
    },
    computed: {
        src() {
            if (!this.position.marker) {
                return
            }

            const params = new URLSearchParams([
                ['x', this.position.marker[0]],
                ['y', this.position.marker[1]],
                ['srs', '28992'],
                ['mode', 'pano'],
            ])

            const url = new URL(this.url)
            url.search = params.toString()

            return url.toString()
        },
    },
    watch: {
        position(value) {
            if (!value.marker) {
                return
            }

            const latlong = transform(value.marker, 'EPSG:28992', 'EPSG:4326')
            this.streetview.setPosition({ lat: latlong[1], lng: latlong[0] })
        },
    },
    props: {
        position: Object,
        url: String,
    },
}
</script>

<style scoped>
.iframe {
    width: 100%;
    height: 100%;
}
</style>
