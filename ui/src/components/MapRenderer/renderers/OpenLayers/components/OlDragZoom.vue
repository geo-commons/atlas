<template>
    <div v-if="false"></div>
</template>

<script>
import { DragZoom } from 'ol/interaction'

export default {
    name: 'ol-drag-zoom',
    inject: ['map'],
    created() {
        this.dragZoom = new DragZoom()
        this.map.addInteraction(this.dragZoom)
    },
    destroyed() {
        this.map.removeInteraction(this.dragZoom)
    },
    props: {
        tool: String,
    },
}
</script>
