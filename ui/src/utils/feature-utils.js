import { DEFAULT_DRAWING_COLOR, DEFAULT_DRAWING_FONT_SIZE, DEFAULT_DRAWING_STROKE_WIDTH } from "@/constants/defaults";

export const getFeatureRgba = (feature, alpha) => {
  const red = feature.get("color")?.red !== undefined ? feature.get("color").red : DEFAULT_DRAWING_COLOR.red;
  const green = feature.get("color")?.green !== undefined ? feature.get("color").green : DEFAULT_DRAWING_COLOR.green;
  const blue = feature.get("color")?.blue !== undefined ? feature.get("color").blue : DEFAULT_DRAWING_COLOR.blue;

  return `rgba(${red},${green},${blue},${alpha})`;
};

export const getFeatureStrokeWidth = (feature, isCircle) => {
  return feature.get("strokeWidth")
    ? isCircle
      ? feature.get("strokeWidth") * 2
      : feature.get("strokeWidth")
    : isCircle
      ? 10
      : DEFAULT_DRAWING_STROKE_WIDTH;
};

export const getFeatureFontSize = (feature) => {
  return feature.get("fontSize") ? feature.get("fontSize") : DEFAULT_DRAWING_FONT_SIZE;
};
