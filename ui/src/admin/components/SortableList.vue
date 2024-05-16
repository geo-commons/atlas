<template>
  <div>
    <div class="sort-column-header-wrapper">
      <h3>{{ title }}</h3>
      <button class="button __secondary_admin __small" type="button" @click="sortItems">Sorteer alfabetisch</button>
    </div>

    <div class="help-text-wrapper">
      <button
        type="button"
        class="help-text-button"
        @click="showKeyboardInstructions = !showKeyboardInstructions"
        @keydown.enter.prevent="showKeyboardInstructions = !showKeyboardInstructions"
        v-text="keyboardInstructionsButtonText"
      />
      <p
        v-if="showKeyboardInstructions"
        v-text="
          'Selecteer en deselecteer een actief element met behulp van de spatiebalk. Verplaats met behulp van pijlen omhoog en omlaag het element naar de gewenste plek.'
        "
      />
    </div>

    <div id="reorder_instructions" aria-live="assertive" class="sr-only" v-text="assistiveText" />

    <table v-if="items?.length > 0" class="sort-table">
      <thead>
        <tr class="table-border">
          <th class="sort-column-padding">Titel</th>
        </tr>
      </thead>
      <draggable
        v-bind="dragOptions"
        v-model="items"
        tag="tbody"
        item-key="id"
        :group="group"
        role="listbox"
        @change="onItemMove"
        @start="dragStart"
      >
        <template #item="{ element }">
          <tr
            class="table-border"
            :class="{ 'active-row': checkRow(element), [itemGroupClass]: true }"
            role="option"
            draggable="true"
            tabindex="0"
            aria-describedby="reorder_instructions"
            @click="selectRow(element)"
            @keydown.space.prevent="toggleGrabbed(element)"
            @keydown.down.prevent="moveItem(true)"
            @keydown.up.prevent="moveItem(false)"
            @keydown.enter.prevent="selectRow(element)"
          >
            <td class="sort-column-padding">{{ element.title }}</td>
          </tr>
        </template>
      </draggable>
    </table>
    <div v-else>
      <slot name="empty-list"></slot>
    </div>
  </div>
</template>

<script>
import draggable from "vuedraggable";
import { sortAlphabetically } from "@/utils/table-sort-helpers";
import { debounce } from "@/utils/debouncer";

draggable.compatConfig = { MODE: 3 };

export default {
  name: "SortableList",
  components: { draggable },
  props: {
    currentItemList: Array,
    title: String,
    group: String,
    selectableItems: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      items: this.currentItemList,
      selectedItem: null,
      itemGroupClass: null,
      isGrabbed: false,
      grabbedItemIndex: null,
      grabbedItemElement: null,
      assistiveText: "Selecteer een element met behulp van de spatiebalk",
      showKeyboardInstructions: false,
    };
  },
  computed: {
    dragOptions() {
      return {
        animation: 0,
        group: "description",
        disabled: false,
        ghostClass: "ghost",
      };
    },
    keyboardInstructionsButtonText() {
      return this.showKeyboardInstructions ? "Verberg toetsenbord instructies" : "Toon toetsenbord instructies";
    },
  },
  watch: {
    currentItemList: {
      handler(newValues) {
        this.items = newValues;
        if (this.isGrabbed) {
          this.$nextTick(() => {
            // Makes sure the focus item is still in focus after this component receives
            // an update to the items array.
            const items = [...document.getElementsByClassName(this.itemGroupClass)];
            items[this.grabbedItemIndex].focus();
          });
        }
      },
      deep: true,
    },
  },
  created() {
    this.itemGroupClass = `${this.group}-list__item`;
  },
  methods: {
    update() {
      this.$emit("update", this.items);
    },
    sortItems() {
      this.items = this.items.slice(0).sort((a, b) => {
        const textA = a["title"].toLowerCase();
        const textB = b["title"].toLowerCase();
        return sortAlphabetically(textA, textB, true);
      });

      this.onItemMove();
    },
    onItemMove() {
      this.reorderItems();
      this.timeout = debounce(this.update, this.timeout, 2000);
    },
    dragStart() {
      if (this.timeout) clearTimeout(this.timeout);
    },
    reorderItems() {
      this.items = this.items.map((item, index) => {
        return { ...item, newOrder: index };
      });
    },
    selectRow(item) {
      if (!this.selectableItems) {
        return;
      }

      // Reset selected item when pressed again.
      if (this.selectedItem?.id === item.id) {
        this.selectedItem = null;
      } else {
        this.selectedItem = item;
      }

      this.$emit("item-selected", this.selectedItem);
    },
    checkRow(item) {
      return this.selectedItem?.id === item?.id;
    },
    toggleGrabbed(item) {
      this.isGrabbed = !this.isGrabbed;

      if (this.isGrabbed) {
        this.assistiveText = `${item.title}, geselecteerd. Huidige positie in de lijst: ${
          item.currentOrder + 1
        }. Toets pijl omhoog of omlaag om het element te verplaatsen, of spatiebalk om te deselecteren.`;

        this.grabbedItemIndex = item.newOrder;
        return;
      }

      this.assistiveText = `${item.title}, gedeselecteerd. Laatste positie in de lijst: ${this.grabbedItemIndex + 1}`;
      this.grabbedItemIndex = null;
    },
    moveItem(moveDown) {
      if (!this.isGrabbed) {
        return;
      }

      const hoverIndex = moveDown ? this.grabbedItemIndex + 1 : this.grabbedItemIndex - 1;

      // Make sure the new position isn't out of bounds
      if (hoverIndex < 0 || hoverIndex >= this.items.length) {
        return;
      }

      // Make a copy of the existing list & find the item that's being moved
      const todosCopy = this.items.slice(0);
      const draggedItem = todosCopy[this.grabbedItemIndex];

      // Remove the item that's being moved
      todosCopy.splice(this.grabbedItemIndex, 1);

      // Place it in its new position
      todosCopy.splice(hoverIndex, 0, draggedItem);

      // Update the list of todos to reflect the new order
      this.items = todosCopy;

      this.onItemMove();

      // Update the assistive text announced to the screen reader user
      this.assistiveText = `${draggedItem.title}. New position in list: ${hoverIndex + 1}`;

      // Wait for the DOM to update, then find all list items & focus the one that was just moved
      this.$nextTick(() => {
        const items = [...document.getElementsByClassName(this.itemGroupClass)];
        this.grabbedItemElement = items[hoverIndex];
        this.grabbedItemElement.focus();

        this.grabbedItemIndex = hoverIndex;
      });
    },
  },
};
</script>

<style scoped>
.sort-column-header-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.help-text-wrapper {
  padding-bottom: 16px;
}

.help-text-button {
  font-size: var(--font-size-small);
  background-color: transparent;
}

.help-text-button:hover {
  text-decoration: underline;
  color: var(--color-admin-primary);
}

.active-row {
  background: var(--color-admin-primary-active);
  box-shadow: 3px 0 0 var(--color-admin-primary) inset;
}

.sort-table {
  width: 100%;
  border-collapse: collapse;
  background: var(--color-white);
}

tbody > tr:hover {
  background-color: var(--color-admin-primary-hover);
  cursor: move;
}

.sort-table thead tr th {
  text-align: left;
  font-weight: var(--font-weight-normal);
  color: var(--color-text-grey);
  padding-top: 10px;
  padding-bottom: 10px;
}

.sort-table tbody tr td {
  text-align: left;
  font-weight: var(--font-weight-normal);
  padding-top: 5px;
  padding-bottom: 5px;
}

tr.table-border:not(:last-child) > td,
th {
  border-bottom: 1px solid var(--color-grey-60);
}

tr > td:not(:nth-last-child(-n + 2)) {
  padding-right: 8px;
}

.sort-column-padding {
  padding: 0 12px;
}
</style>
