<template>
  <button
    v-tippy="{ placement: 'bottom' }"
    class="tools-panel__button"
    :class="{
      'tools-panel__button--active': showEditFeatureMenu,
    }"
    content="Laag objecten bewerken"
    aria-label="Laag objecten bewerken"
    @click="toggleEditLayer"
  >
    <EditLocationIcon class="icon" />
  </button>

  <div v-if="showEditFeatureMenu">
    <transition name="fade">
      <div class="tools-panel__draw-bar">
        <div class="tools-panel__draw-menu">
          <button
            v-tippy="{ placement: 'bottom' }"
            aria-label="Punt"
            class="tools-panel__button"
            :class="{
              'tools-panel__button--active': tool === 'EDIT_POINT',
            }"
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
              'tools-panel__button--active': tool === 'EDIT_LINE',
            }"
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
            aria-label="Polygoon"
            class="tools-panel__button"
            :class="{
              'tools-panel__button--active': tool === 'EDIT_POLYGON',
            }"
            content="Polygoon"
            @click="() => setTool('DRAW_POLYGON')"
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

interface EditLayerMenuProps {
  tool: string;
  showEditFeatureMenu: boolean;
  toggleEditLayer: () => void;
  setTool: (tool: string) => void;
}

const { tool, showEditFeatureMenu, toggleEditLayer, setTool } = defineProps<EditLayerMenuProps>();

// TODO: Fix working of this
const emitKeyDown = () => {
  const keyDownEvent = new KeyboardEvent("keydown", { key: "Backspace" });

  document.dispatchEvent(keyDownEvent);
};
</script>
