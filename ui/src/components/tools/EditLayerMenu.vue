<template>
  <div class="tools-panel__button-container">
    <button
      v-tippy="{ placement: 'bottom' }"
      class="tools-panel__button"
      :class="{
        'tools-panel__button--active': showEditFeatureMenu,
      }"
      content="Laag objecten bewerken"
      aria-label="Laag objecten bewerken"
      @click="toggleEditLayerMenu"
    >
      <EditLocationIcon class="icon" />
    </button>

    <div v-if="showEditFeatureMenu">
      <transition name="fade">
        <div class="tools-panel__draw-bar">
          <div class="tools-panel__draw-menu">
            <button
              v-tippy="{ placement: 'bottom' }"
              aria-label="Object toevoegen"
              class="tools-panel__button"
              :class="{
                'tools-panel__button--active': editLayerStore.editLayerMode === EditLayerMode.ADD,
              }"
              content="Object toevoegen"
              @click="() => toggleAddEditFeatureMode()"
            >
              <AddIcon />
            </button>
          </div>
          <div class="tools-panel__draw-menu">
            <button
              v-tippy="{ placement: 'bottom' }"
              aria-label="Object bewerken"
              class="tools-panel__button"
              :class="{
                'tools-panel__button--active': editLayerStore.editLayerMode === EditLayerMode.EDIT,
              }"
              content="Object bewerken"
              @click="() => toggleEditFeatureMode()"
            >
              <EditIcon />
            </button>
          </div>
          <div class="tools-panel__draw-menu">
            <button
              v-tippy="{ placement: 'bottom' }"
              aria-label="Punt"
              class="tools-panel__button"
              :class="{
                'tools-panel__button--active':
                  tool === 'EDIT_POINT' && editLayerStore.editLayerMode === EditLayerMode.ADD,
              }"
              :disabled="editLayerStore.editLayerMode !== EditLayerMode.ADD || editLayerStore.feature"
              content="Punt"
              @click="() => setTool('EDIT_POINT')"
            >
              <DotIcon />
            </button>
          </div>
          <div class="tools-panel__draw-menu">
            <button
              v-tippy="{ placement: 'bottom' }"
              aria-label="Lijn"
              class="tools-panel__button"
              :class="{
                'tools-panel__button--active':
                  tool === 'EDIT_LINE' && editLayerStore.editLayerMode === EditLayerMode.ADD,
              }"
              :disabled="editLayerStore.editLayerMode !== EditLayerMode.ADD || editLayerStore.feature"
              content="Lijn"
              @click="() => setTool('EDIT_LINE')"
            >
              <LineIcon />
            </button>
            <div v-if="showEditFeatureMenu && tool === 'EDIT_LINE'">
              <transition name="fade">
                <div class="tools-panel__draw-options-menu">
                  <ul>
                    <li>
                      <button
                        v-tippy="{ placement: 'bottom' }"
                        content="Verwijder laatste punt"
                        aria-label="Verwijder laatste punt"
                        class="tools-panel__option tools-panel__option--rectangle"
                        @click="() => emitKeyDown()"
                      >
                        <UndoIcon />
                      </button>
                    </li>
                  </ul>
                </div>
              </transition>
            </div>
          </div>
          <div class="tools-panel__draw-menu">
            <button
              v-tippy="{ placement: 'bottom' }"
              aria-label="Vlak"
              class="tools-panel__button"
              :class="{
                'tools-panel__button--active':
                  tool === 'EDIT_POLYGON' && editLayerStore.editLayerMode === EditLayerMode.ADD,
              }"
              :disabled="editLayerStore.editLayerMode !== EditLayerMode.ADD || editLayerStore.feature"
              content="Vlak"
              @click="() => setTool('EDIT_POLYGON')"
            >
              <PolyGonIcon />
            </button>
            <div v-if="showEditFeatureMenu && tool === 'EDIT_POLYGON'">
              <transition name="fade">
                <div class="tools-panel__draw-options-menu">
                  <ul>
                    <li>
                      <button
                        v-tippy="{ placement: 'bottom' }"
                        content="Verwijder laatste punt"
                        aria-label="Verwijder laatste punt"
                        class="tools-panel__option tools-panel__option--rectangle"
                        @click="() => emitKeyDown()"
                      >
                        <UndoIcon />
                      </button>
                    </li>
                  </ul>
                </div>
              </transition>
            </div>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup lang="ts">
import EditLocationIcon from "@/assets/icons/edit-location.icon.svg";
import LineIcon from "@/assets/icons/line-icon.svg";
import UndoIcon from "@/assets/icons/undo-icon.svg";
import PolyGonIcon from "@/assets/icons/polygon-icon.svg";
import DotIcon from "@/assets/icons/dot-icon.svg";
import AddIcon from "@/assets/icons/add-icon.svg";
import EditIcon from "@/assets/icons/edit-icon.svg";
import { useEditLayerStore } from "@/stores/edit_layer_store";
import { EditLayerMode } from "@/types/map";

// Props
interface EditLayerMenuProps {
  tool: string;
  showEditFeatureMenu: boolean;
  toggleEditLayer: () => void;
  setTool: (tool: string) => void;
}

const { tool, showEditFeatureMenu, toggleEditLayer, setTool } = defineProps<EditLayerMenuProps>();

// Store
const editLayerStore = useEditLayerStore();

// Methods
const emitKeyDown = () => {
  const keyDownEvent = new KeyboardEvent("keydown", { key: "Backspace" });

  document.dispatchEvent(keyDownEvent);
};

const toggleEditLayerMenu = () => {
  if (editLayerStore.editLayerMode !== EditLayerMode.NONE) {
    editLayerStore.setEditLayerMode(EditLayerMode.NONE);
  }

  toggleEditLayer();
};

const toggleAddEditFeatureMode = () => {
  if (editLayerStore.editLayerMode !== EditLayerMode.ADD) {
    editLayerStore.setEditLayerMode(EditLayerMode.ADD);
    setTool("");

    return;
  }

  editLayerStore.setEditLayerMode(EditLayerMode.NONE);
  setTool("");
};

const toggleEditFeatureMode = () => {
  if (editLayerStore.editLayerMode !== EditLayerMode.EDIT) {
    editLayerStore.setEditLayerMode(EditLayerMode.EDIT);
    setTool("");

    return;
  }

  editLayerStore.setEditLayerMode(EditLayerMode.NONE);
  setTool("");
};
</script>
