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

  return {
    position: {
      zoom: pathMatch.groups.zoom ? parseFloat(pathMatch.groups.zoom) : defaultConfig.position.zoom,
      center: [
        pathMatch.groups.x ? parseFloat(pathMatch.groups.x) : defaultConfig.position.center.x,
        pathMatch.groups.y ? parseFloat(pathMatch.groups.y) : defaultConfig.position.center.y,
      ],
      marker: null,
      geolocation: null,
    },
    drawing: params.drawing ? params.drawing : null,
    visibleBase: params.base ? params.base : null,
    visibleLayers: params.layers ? params.layers.split(",") : [],
  };
};
