export const getSettingsFromPath = () => {
  const pathExpression = /@(?<x>[0-9.]+),(?<y>[0-9.]+),(?<zoom>[0-9.]+)z(?:\/layers=(?<layers>[a-zA-Z0-9.\-_,]+))?/
  const match = window.location.pathname.match(pathExpression) || { groups: {} }

  return {
    position: {
      zoom: match.groups.zoom ? parseFloat(match.groups.zoom) : 13,
      center: [ match.groups.x ? parseFloat(match.groups.x) : 126910, match.groups.y ? parseFloat(match.groups.y) : 505834 ],
      marker: null
    },
    visibleLayers: match.groups.layers ? match.groups.layers.split(',') : []
  }
}
