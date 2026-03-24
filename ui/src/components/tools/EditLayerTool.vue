<template>
  <button
    v-tippy="{ placement: 'bottom' }"
    :aria-label="tool.translation"
    class="tools-panel__button"
    :class="{
      'tools-panel__button--active': toolInUse === tool.name && editLayerStore.editLayerMode === EditLayerMode.ADD,
    }"
    :disabled="
      editLayerStore.editLayerMode !== EditLayerMode.ADD ||
      Boolean(editLayerStore.feature) ||
      Boolean(editLayerStore.draftFeature) ||
      editLayerStore.selectedLayer === null
    "
    :content="tool.translation"
    @click="() => setTool(tool.name)"
  >
    <component :is="tool.icon" />
  </button>
  <div>
    <transition name="fade">
      <div v-if="toolInUse === tool.name && tool.enableUndo" class="tools-panel__draw-options-menu">
        <ul>
          <li>
            <button
              v-tippy="{ placement: 'bottom' }"
              :content="`Verwijder laatste ${tool.translation}`"
              :aria-label="`Verwijder laatste ${tool.translation}`"
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
</template>

<script setup lang="ts">
import { EditLayerMode } from "@/types/map";
import UndoIcon from "@/assets/icons/undo-icon.svg";
import { useEditLayerStore } from "@/stores/edit_layer_store";

// Props
interface EditLayerToolProps {
  tool: {
    name: string;
    icon: string;
    translation: string;
    enableUndo: boolean;
  };
  toolInUse: string;
  setTool: (tool: string) => void;
}

const { tool, toolInUse, setTool } = defineProps<EditLayerToolProps>();

// Store
const editLayerStore = useEditLayerStore();

// Methods
const emitKeyDown = () => {
  const keyDownEvent = new KeyboardEvent("keydown", { key: "Backspace" });

  document.dispatchEvent(keyDownEvent);
};
</script>
