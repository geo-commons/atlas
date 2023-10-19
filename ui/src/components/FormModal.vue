<template>
  <transition name="modal-fade">
    <div id="modal" class="modal-backdrop">
      <div class="modal" role="dialog">
        <header class="modal-header">
          <slot name="header"></slot>
          <button type="button" class="iconbutton __normal __round" aria-label="Close Modal" @click="close">
            <close-icon-large />
          </button>
        </header>

        <main class="modal-body">
          <slot name="body"></slot>
        </main>
      </div>
    </div>
  </transition>
</template>

<script>
import CloseIconLarge from "@/icons/CloseIconLarge.vue";

export default {
  name: "FormModal",
  components: { CloseIconLarge },
  props: {
    toggleModal: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      tabData: [],
      modal: null,
    };
  },
  watch: {
    toggleModal(newValue) {
      this.modal = document.getElementById("modal");
      if (newValue) {
        this.preventTabOutside();
      } else {
        this.enableTabOutside();
      }
    },
  },
  created() {},
  methods: {
    close() {
      this.enableTabOutside(this.modal);
      this.$emit("close");
    },
    //note: copied the functions below from:
    // https://stackoverflow.com/questions/14572084/keep-tabbing-within-modal-pane-only
    preventTabOutside() {
      const selector =
        'a[href], area[href], input:not([disabled]):not([type="hidden"]), select:not([disabled]), textarea:not([disabled]), button:not([disabled]), iframe, object, embed, *[tabindex], *[contenteditable]';

      const tabbableElements = document.querySelectorAll(selector);
      this.tabData = Array.from(tabbableElements)
        // filter out any elements within the modal
        .filter((elem) => !this.modal.contains(elem))
        // store refs to the element and its original tabindex
        .map((elem) => {
          // capture original tab index, if it exists
          const tabIndex = elem.hasAttribute("tabindex") ? elem.getAttribute("tabindex") : null;
          // temporarily set the tabindex to -1
          elem.setAttribute("tabindex", -1);
          return { elem, tabIndex };
        });
    },
    enableTabOutside() {
      this.tabData.forEach(({ elem, tabIndex }) => {
        if (tabIndex === null) {
          elem.removeAttribute("tabindex");
        } else {
          elem.setAttribute("tabindex", tabIndex);
        }
      });
      this.tabData = [];
    },
  },
};
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: rgba(0, 0, 0, 0.3);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal {
  background: var(--color-white);
  box-shadow: var(--shadow-normal);
  overflow-x: auto;
  display: flex;
  flex-direction: column;
  width: 80%;
}

.modal-header {
  position: relative;
  padding: 0 15px;
  display: flex;
  border-bottom: 1px solid var(--color-grey-60);
  justify-content: space-between;
  align-items: center;
}

.modal-body {
  padding: 20px 15px;
}

.modal-fade-enter,
.modal-fade-leave-to {
  opacity: 0;
}

.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.2s ease;
}
</style>
