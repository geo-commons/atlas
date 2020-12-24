import { transform } from 'ol/proj'
import { getDefinitions } from './projections'
import { register } from 'ol/proj/proj4'

// Register EPSG:28992 projection
register(getDefinitions())

export class GooglePanorama {
  constructor(target, position) {
    const latlong = transform(position.marker, 'EPSG:28992','EPSG:4326')

    this.streetview = new google.maps.StreetViewPanorama(target, {
      position: {
        lat: latlong[1],
        lng: latlong[0]
      },
      zoom: position.zoom,
      fullscreenControl: false
    })
  }

  setPosition(position) {
    const latlong = transform(position.marker, 'EPSG:28992','EPSG:4326')
    this.streetview.setPosition({ lat: latlong[1], lng: latlong[0] })
  }
}

export class StreetSmartPanorama {
  constructor(target, position) {
    if (window.STREETSMART_INITIALIZED) {
      this.setPosition(position)
      return
    }

    window.STREETSMART_INITIALIZED = true

    const options = {
      targetElement: target,
      username: STREETSMART_USER,
      password: STREETSMART_PASSWORD,
      apiKey: STREETSMART_API_KEY,
      srs: 'EPSG:28992',
      locale: 'nl',
    }

    StreetSmartApi.init(options).then(() => {
      this.setPosition(position)
    })
  }

  setPosition(position) {
    const options = {
      viewerType: [ StreetSmartApi.ViewerType.PANORAMA ],
      panoramaViewer: {
        closable: false,
        maximizable: false
      },
      obliqueViewer: {
        closable: false,
        maximizable: false
      }
    }

    StreetSmartApi.open(`${position.marker[0]}, ${position.marker[1]}`, options).then((results) => {
      if (!results || results.length === 0) {
        return
      }

      const viewer = results[0]
      viewer.toggle3DCursor(false)
    })
  }
}
