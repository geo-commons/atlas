import Vue from "vue";
import MarkdownIt from "markdown-it";

const Markdown = Vue.extend({
  name: "VueMarkdown",
  props: {
    source: {
      required: true,
      default: function () {
        return "";
      },
    },
    options: {
      required: false,
      default: function () {
        return { linkify: true };
      },
    },
    inline: {
      required: false,
      default: function () {
        return true;
      },
    },
  },
  data() {
    return {
      md: null,
    };
  },
  computed: {
    content() {
      const src = this.source;

      if (this.inline) {
        return this.md?.renderInline(src);
      }

      return this.md?.render(src);
    },
  },
  created() {
    this.md = new MarkdownIt(this.options);

    const defaultRender =
      this.md.renderer.rules.link_open ||
      function (tokens, idx, options, env, self) {
        return self.renderToken(tokens, idx, options);
      };

    this.md.renderer.rules.link_open = function (
      tokens,
      idx,
      options,
      env,
      self
    ) {
      // If you are sure other plugins can't add `target` - drop check below
      var aIndex = tokens[idx].attrIndex("target");

      if (aIndex < 0) {
        tokens[idx].attrPush(["target", "_blank"]); // add new attribute
      } else {
        tokens[idx].attrs[aIndex][1] = "_blank"; // replace value of existing attr
      }

      // pass token to default renderer.
      return defaultRender(tokens, idx, options, env, self);
    };
  },
  render(h) {
    return h("div", { domProps: { innerHTML: this.content } });
  },
});

export default Markdown;
