import { createApp } from "vue";
import LocationIcon from "../components/LocationIcon";

// From https://medium.com/better-programming/dynamic-svg-markers-for-google-maps-in-vue-js-7541fa1a54a

// create a constructor from a Vue component
const LocationIconConstructor = (propsData) => {
  const app = createApp(LocationIcon, { ...propsData });
  const wrapper = app.mount(document.createElement("div"));

  return wrapper;
};

export default (fillColor, strokeColor) => {
  // create an instance of the LocationIconConstructor with props data
  const iconComponent = LocationIconConstructor({ fillColor, strokeColor });
  // serialize the component's DOM to an SVG string
  const iconString = new XMLSerializer().serializeToString(iconComponent.$el);
  // generate a data URL from the SVG string
  return "data:image/svg+xml;charset=UTF-8;base64," + btoa(iconString);
};
