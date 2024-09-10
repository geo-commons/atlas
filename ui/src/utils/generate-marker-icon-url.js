import { createApp } from "vue";
import MarkerIcon from "../components/MarkerIcon";

// Create a constructor function that initializes and mounts a Vue component
const LocationIconConstructor = (propsData) => {
  const app = createApp(MarkerIcon, { ...propsData });
  // Create a temporary div element
  const container = document.createElement("div");
  // Mount the Vue app to the temporary div
  const instance = app.mount(container);
  // Return the DOM element containing the mounted component
  return instance.$el;
};

export default (fillColor, strokeColor) => {
  // Create an instance of the LocationIconConstructor with props data
  const iconElement = LocationIconConstructor({ fillColor, strokeColor });
  // Serialize the component's DOM to an SVG string
  const iconString = new XMLSerializer().serializeToString(iconElement);
  // Generate a data URL from the SVG string
  return "data:image/svg+xml;charset=UTF-8;base64," + btoa(iconString);
};
