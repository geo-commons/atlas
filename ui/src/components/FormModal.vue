<template>
  <!-- Note: Make sure to place the FormModal component at the end of the template,
  otherwise the model backdrop does not always overlap the background components completely. -->
  <transition name="modal-fade">
    <div id="modal" ref="modal" class="modal-backdrop">
      <div class="modal container __admin" role="dialog">
        <header class="modal-header">
          <slot name="header"></slot>
          <button
            v-tippy="{ placement: 'bottom' }"
            type="button"
            class="iconbutton __normal __round"
            aria-label="Sluit"
            content="Sluit"
            @click="close"
          >
            <CloseIcon class="icon" />
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
import CloseIcon from "../assets/icons/close-icon.svg";

export default {
  name: "FormModal",
  components: { CloseIcon },
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
  mounted() {
    this.setTabMode(this.toggleModal);
  },
  unmounted() {
    this.enableTabOutside(this.modal);
  },
  methods: {
    close() {
      this.$emit("close");
    },
    setTabMode(showModal) {
      this.modal = this.$refs.modal;
      if (showModal) {
        this.preventTabOutside();
      } else {
        this.enableTabOutside();
      }
    },
    // The following methods prevent the user from accessing elements in the background
    // of the modal using the tab key. For reference:
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
  z-index: 10;
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
