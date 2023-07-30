export const getSettingsFromPath = (defaultConfig) => {
  const pathExpression =
    /@(?<x>[0-9.]+),(?<y>[0-9.]+),(?<zoom>[0-9.]+)z(?:\/layers=(?<layers>[a-zA-Z0-9.\-_,]*))?(?:\/base=(?<base>[a-zA-Z0-9.\-_,]*))(?:\/drawing=(?<drawing>[a-zA-Z0-9.\-_,]*))?/;
  const match = window.location.pathname.match(pathExpression) || {
    groups: {},
  };

  return {
    position: {
      zoom: match.groups.zoom
        ? parseFloat(match.groups.zoom)
        : defaultConfig.position.zoom,
      center: [
        match.groups.x
          ? parseFloat(match.groups.x)
          : defaultConfig.position.center.x,
        match.groups.y
          ? parseFloat(match.groups.y)
          : defaultConfig.position.center.y,
      ],
      marker: null,
      geolocation: null,
    },
    drawing: match.groups.drawing ? match.groups.drawing : null,
    visibleBase: match.groups.base ? match.groups.base : null,
    visibleLayers: match.groups.layers ? match.groups.layers.split(",") : [],
  };
};
