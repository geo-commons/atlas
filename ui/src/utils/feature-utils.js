export const getFeatureRgba = (feature, alpha) => {
  const red = feature.get("color")?.red !== undefined ? feature.get("color").red : 0;
  const green = feature.get("color")?.green !== undefined ? feature.get("color").green : 102;
  const blue = feature.get("color")?.blue !== undefined ? feature.get("color").blue : 255;

  return `rgba(${red},${green},${blue},${alpha})`;
};

export const getFeatureStrokeWidth = (feature, isCircle) => {
  return feature.get("strokeWidth")
    ? isCircle
      ? feature.get("strokeWidth") * 2
      : feature.get("strokeWidth")
    : isCircle
      ? 10
      : 5;
};

export const getFeatureFontSize = (feature) => {
  return feature.get("fontSize") ? feature.get("fontSize") : 22;
};
