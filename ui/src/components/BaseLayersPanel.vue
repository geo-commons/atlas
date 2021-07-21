<template>
    <div class="wrapper" id="baseLayers">
        <ul>
            <li class="layer" v-for="layer in baseLayers" :key="layer.id">
                <input
                    type="radio"
                    :id="layer.id"
                    name="baseLayer"
                    :checked="layer.is_visible"
                    @change="() => onSelect(layer)"
                />
                <label :for="layer.id">{{ layer.title }}</label>
                <LayerInfo :layer="layer" />
            </li>
        </ul>
    </div>
</template>

<script>
import LayerInfo from './LayerInfo'

export default {
    name: 'BaseLayersPanel',
    components: {
        LayerInfo,
    },
    methods: {
        onSelect(selectedLayer) {
            this.baseLayers.map((layer) => {
                if (selectedLayer.id === layer.id) {
                    this.$emit('toggle-layer', [layer.id, true])
                } else {
                    this.$emit('toggle-layer', [layer.id, false])
                }
            })
        },
    },
    computed: {
        baseLayers() {
            return this.layers.filter((layer) => layer.is_base)
        },
    },
    props: {
        layers: Array,
    },
}
</script>

<style scoped>
.wrapper {
    position: absolute;
    bottom: var(--width-button-normal);
    right: 0;
    padding: 8px 12px;
    background: white;
    border-radius: var(--radius-small);
    border-bottom-right-radius: 0;
    box-shadow: var(--shadow-normal);
}

.layer {
    position: relative;
    display: flex;
}

.layer > input {
    position: absolute;
    top: 6px;
    left: 0;
    width: 12px;
    height: 12px;
    margin: 0;
}

.layer > label {
    display: block;
    position: relative;
    width: 100%;
    cursor: pointer;
    padding: 3px 0 3px 18px;
    user-select: none;
    font-size: var(--font-size-small);
    white-space: nowrap;
}
</style>
