export const getSettingsFromPath = (defaultConfig) => {
  const pathExpression = /@(?<x>[0-9.]+),(?<y>[0-9.]+),(?<zoom>[0-9.]+)z(?<params>.*)?/;
  const paramsExpression = /(?<key>[^=/]+)=?(?<value>[^/]*)?/g;

  const pathMatch = window.location.pathname.match(pathExpression) || {
    groups: {},
  };

  let matches,
    params = [];

  while ((matches = paramsExpression.exec(pathMatch.groups.params || ""))) {
    params[matches.groups.key] = matches.groups.value;
  }

  const marker = params.marker?.split(",") ?? null;

  return {
    position: {
      zoom: pathMatch.groups.zoom ? parseFloat(pathMatch.groups.zoom) : defaultConfig.position.zoom,
      center: [
        pathMatch.groups.x ? parseFloat(pathMatch.groups.x) : defaultConfig.position.center.x,
        pathMatch.groups.y ? parseFloat(pathMatch.groups.y) : defaultConfig.position.center.y,
      ],
      marker: marker && marker.length === 2 ? [parseFloat(marker[0]), parseFloat(marker[1])] : null,
      geolocation: null,
    },
    drawing: params.drawing ? params.drawing : null,
    visibleBase: params.base ? params.base : null,
    visibleLayers: params.layers ? params.layers.split(",") : [],
    is_embed: params.is_embed ? params.is_embed === "true" : false,
  };
};
