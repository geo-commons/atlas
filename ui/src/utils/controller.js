import Map from 'ol/Map'
import View from 'ol/View'
import TileLayer from 'ol/layer/Tile'
import TileWMS from 'ol/source/TileWMS'
import { defaults as defaultInteractions, DragRotateAndZoom } from 'ol/interaction'

class MapController {
    constructor(settings) {
        this.settings = settings
        this.layers = []
    }

    addLayers(layers) {
        layers.forEach((layer) => {
            this.addLayer(layer)
        })
    }

    addLayer(layer) {
        this.layers = [
            ...this.layers,
            new TileLayer({
                id: layer.id,
                visible:
                    layer.is_visible === true || this.settings.visibleLayers.includes(layer.id),
                layerName: layer.name,
                opacity: layer.opacity,
                source: new TileWMS({
                    projection: 'EPSG:28992',
                    url: layer.url,
                    servertype: layer.server_type,
                    params: {
                        layers: layer.name,
                    },
                }),
            }),
        ]
    }

    render(targetId) {
        return new Map({
            interactions: defaultInteractions().extend([new DragRotateAndZoom()]),
            layers: this.layers,
            target: targetId,
            view: new View({
                projection: 'EPSG:28992',
                center: this.settings.position.center,
                zoom: this.settings.position.zoom,
            }),
        })
    }
}

export default MapController
