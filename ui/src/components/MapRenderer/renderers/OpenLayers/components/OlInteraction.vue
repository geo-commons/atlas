<template>
    <div v-if="false"></div>
</template>

<script>
import Snap from 'ol/interaction/Snap'
import VectorSource from 'ol/source/Vector'
import constructDraw from '../../../../../utils/draw'

export default {
    name: 'ol-interaction',
    inject: ['map'],
    created() {
        const onDrawStart = () => {
            this.$emit('draw-start')
        }

        const onDrawEnd = (sketch) => {
            this.$emit('draw-end', { tool: this.tool, sketch })
        }

        this.draw = constructDraw(this.tool, this.map, onDrawStart, onDrawEnd)
        this.map.addInteraction(this.draw)

        const layers = this.map.getLayers().getArray().filter((layer) => layer.getSource() instanceof VectorSource)
        if (layers.length > 0) {
            this.map.addInteraction(new Snap({
                source: layers[0].getSource()
            }))
        }
    },
    destroyed() {
        this.map.removeOverlay(this.draw.measureTooltip)
        this.map.removeInteraction(this.draw)

        if (this.snap) {
            this.map.removeInteraction(this.snap)
        }
    },
    props: {
        tool: String,
    },
}
</script>
