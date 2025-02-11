<template>
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
              'tools-panel__button--active': editLayerStore.editLayerMode === EEditLayerMode.ADD,
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
            aria-label="Punt"
            class="tools-panel__button"
            :class="{
              'tools-panel__button--active':
                tool === 'EDIT_POINT' && editLayerStore.editLayerMode === EEditLayerMode.ADD,
            }"
            :disabled="editLayerStore.editLayerMode !== EEditLayerMode.ADD || editLayerStore.feature"
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
                tool === 'EDIT_LINE' && editLayerStore.editLayerMode === EEditLayerMode.ADD,
            }"
            :disabled="editLayerStore.editLayerMode !== EEditLayerMode.ADD || editLayerStore.feature"
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
                tool === 'EDIT_POLYGON' && editLayerStore.editLayerMode === EEditLayerMode.ADD,
            }"
            :disabled="editLayerStore.editLayerMode !== EEditLayerMode.ADD || editLayerStore.feature"
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
</template>

<script setup lang="ts">
import EditLocationIcon from "@/assets/icons/edit-location.icon.svg";
import LineIcon from "@/assets/icons/line-icon.svg";
import UndoIcon from "@/assets/icons/undo-icon.svg";
import PolyGonIcon from "@/assets/icons/polygon-icon.svg";
import DotIcon from "@/assets/icons/dot-icon.svg";
import AddIcon from "@/assets/icons/add-icon.svg";
import { useEditLayerStore } from "@/stores/edit_layer_store";
import { EEditLayerMode } from "@/types/map";

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
// TODO: Fix working of this
const emitKeyDown = () => {
  const keyDownEvent = new KeyboardEvent("keydown", { key: "Backspace" });

  document.dispatchEvent(keyDownEvent);
};

const toggleEditLayerMenu = () => {
  if (editLayerStore.editLayerMode !== EEditLayerMode.NONE) {
    editLayerStore.setEditLayerMode(EEditLayerMode.NONE);
  }

  toggleEditLayer();
};

const toggleAddEditFeatureMode = () => {
  if (editLayerStore.editLayerMode !== EEditLayerMode.ADD) {
    editLayerStore.setEditLayerMode(EEditLayerMode.ADD);
    setTool("");

    return;
  }

  editLayerStore.setEditLayerMode(EEditLayerMode.NONE);
  setTool("");
};
</script>
