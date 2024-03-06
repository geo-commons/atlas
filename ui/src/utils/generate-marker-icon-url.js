import { createApp } from "vue";
import MarkerIcon from "../components/MarkerIcon";

// From https://medium.com/better-programming/dynamic-svg-markers-for-google-maps-in-vue-js-7541fa1a54a

// create a constructor from a Vue component
const LocationIconConstructor = (propsData) => {
  const app = createApp(MarkerIcon, { ...propsData });
  const wrapper = app.mount(document.createElement("div"));

  return wrapper;
};

export default (fillColor, strokeColor) => {
  // create an instance of the LocationIconConstructor with props data
  const iconComponent = LocationIconConstructor({ fillColor, strokeColor });
  // mount the component shadow DOM
  iconComponent.$mount();
  // serialize the component's DOM to an SVG string
  const iconString = new XMLSerializer().serializeToString(iconComponent.$el);
  // generate a data URL from the SVG string
  return "data:image/svg+xml;charset=UTF-8;base64," + btoa(iconString);
};
