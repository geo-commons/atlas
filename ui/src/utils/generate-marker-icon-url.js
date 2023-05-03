import Vue from "vue";
import MarkerIcon from "../components/MarkerIcon";

// From https://medium.com/better-programming/dynamic-svg-markers-for-google-maps-in-vue-js-7541fa1a54a

// create a constructor from a Vue component
const LocationIconConstructor = Vue.extend(MarkerIcon);

export default (fillColor, strokeColor) => {
  // create a Vue element with required props
  const iconComponent = new LocationIconConstructor({
    propsData: { fillColor, strokeColor },
  });
  // mount the component shadow DOM
  iconComponent.$mount();
  // generate an html string from an element
  const iconString = new XMLSerializer().serializeToString(iconComponent.$el);
  // finally, generate a data url from a string
  return "data:image/svg+xml;charset=UTF-8;base64," + btoa(iconString);
};
