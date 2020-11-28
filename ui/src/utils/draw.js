import Draw from 'ol/interaction/Draw'
import VectorSource from 'ol/source/Vector'
import { Circle as CircleStyle, Fill, Stroke, Style } from 'ol/style'
import { LineString, Polygon } from 'ol/geom'
import { getArea, getLength } from 'ol/sphere'

const constructDraw = (measure) => {
  const draw = new Draw({
    source: new VectorSource(),
    type: measure == 'area' ? 'Polygon' : 'LineString',
    style: new Style({
      fill: new Fill({
        color: 'rgba(255, 255, 255, 0.2)',
      }),
      stroke: new Stroke({
        color: 'rgba(0, 0, 0, 0.5)',
        lineDash: [10, 10],
        width: 2,
      }),
      image: new CircleStyle({
        radius: 5,
        stroke: new Stroke({
          color: 'rgba(0, 0, 0, 0.7)',
        }),
        fill: new Fill({
          color: 'rgba(255, 255, 255, 0.2)',
        }),
      }),
    })
  })

  let sketch
  draw.on('drawstart', (e) => {
    sketch = e.feature
  })

  draw.on('drawend', () => {
    const geometry = sketch.getGeometry()
    if (geometry instanceof Polygon) {
      alert(`${getArea(geometry)} m2`)
    } else if (geometry instanceof LineString) {
      alert(`${getLength(geometry)} m`)
    }
  })

  return draw
}

export default constructDraw
