import { describe, expect, it } from "vitest";

import { mount } from "@vue/test-utils";
import SearchPanel from "../SearchPanel.vue";
// import HelloWorld from "../HelloWorld.vue";

describe("SearchPanel", () => {
  it("renders properly", () => {
    const wrapper = mount(SearchPanel, {
      propsData: { layers: [], position: {} },
    });
    // const wrapper = mount(SearchPanel);
    expect(wrapper.text()).toContain("Hello Vitest");
  });
});

// describe("HelloWorld", () => {
//   it("renders properly", () => {
//     const wrapper = mount(HelloWorld, { propsData: { msg: "Hello Vitest" } });
//     expect(wrapper.text()).toContain("Hello Vitest");
//   });
// });
