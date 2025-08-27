// Configuration constants
const PAN_DISTANCE_FACTOR = 2500;
const ZOOM_BASE_LEVEL = 13;
const KEY_REPEAT_INTERVAL = 200;
const QUEUE_TIMEOUT_MS = 50;

// Arrow key to movement vector mapping
const ARROW_VEC: Record<string, [number, number]> = {
  ArrowUp: [0, 1],
  ArrowDown: [0, -1],
  ArrowLeft: [-1, 0],
  ArrowRight: [1, 0],
};

// Zoom keys mapping
const ZOOM_KEYS: Record<string, number> = {
  "+": 1,
  "-": -1,
  "=": 1,
  "_": -1,
  "NumpadAdd": 1,
  "NumpadSubtract": -1,
};

interface PanningComponent {
  position?: {
    zoom?: number;
    center?: [number, number] | { x: number; y: number };
  };
  setPosition: (position: any, animateFast?: boolean) => void;
  $refs?: {
    map?: {
      cancelPanAnimation?: () => void;
    };
  };
  $emit: (event: string, ...args: any[]) => void;
  cancelPanAnimation?: () => void;
}

interface PanningController {
  init(): void;
  cleanup(): void;
  handleKeyDown(event: KeyboardEvent): void;
  handleKeyUp(event: KeyboardEvent): void;
  handleBlur(): void;
  processNextPan(): void;
}

interface PanMovement {
  deltaX: number;
  deltaY: number;
}

interface PanningState {
  pressedKeys: Set<string>;
  keyRepeatTimer: ReturnType<typeof setInterval> | null;
  panQueue: PanMovement[];
  isProcessingPan: boolean;
  queueTimeoutTimer: ReturnType<typeof setTimeout> | null;
  lastZoom: number | null;
  cachedPanDistance: number | null;
}

/**
 * Creates a panning controller for keyboard-based map navigation.
 * Provides panning and zooming functionality that can be attached to any component.
 * 
 * @param component - The Vue component to attach panning to
 * @returns Panning controller with init and cleanup methods
 */
export const createPanningController = (component: PanningComponent): PanningController => {
  // State
  const state: PanningState = {
    pressedKeys: new Set(),
    keyRepeatTimer: null,
    panQueue: [],
    isProcessingPan: false,
    queueTimeoutTimer: null,
    lastZoom: null,
    cachedPanDistance: null,
  };

  // Helper functions
  const calculatePanDistance = (): number => {
    if (component.position?.zoom !== state.lastZoom) {
      state.lastZoom = component.position?.zoom || null;
      state.cachedPanDistance = PAN_DISTANCE_FACTOR * Math.pow(2, ZOOM_BASE_LEVEL - (component.position?.zoom || 10));
    }
    return state.cachedPanDistance || PAN_DISTANCE_FACTOR;
  };

  const isTypingInField = (): boolean => {
    const activeElement = document.activeElement;
    return !!activeElement && (
      activeElement.matches('input, textarea, select, [role="textbox"]') || 
      (activeElement as HTMLElement).isContentEditable === true
    );
  };

  const clearQueueTimeout = () => {
    if (state.queueTimeoutTimer) {
      clearTimeout(state.queueTimeoutTimer);
      state.queueTimeoutTimer = null;
    }
  };

  const stopKeyRepeat = () => {
    if (!state.keyRepeatTimer) return;
    clearInterval(state.keyRepeatTimer);
    state.keyRepeatTimer = null;
  };

  const panFromPressedKeys = () => {
    let totalDeltaX = 0;
    let totalDeltaY = 0;
    
    for (const key of state.pressedKeys) {
      const movementVector = ARROW_VEC[key];
      if (movementVector) {
        totalDeltaX += movementVector[0];
        totalDeltaY += movementVector[1];
      }
    }
    
    if (totalDeltaX || totalDeltaY) {
      queuePanMovement(totalDeltaX, totalDeltaY);
    }
  };

  const queuePanMovement = (deltaX: number, deltaY: number): void => {
    state.panQueue.push({ deltaX, deltaY });
    if (!state.isProcessingPan) {
      processNextPan();
    }
  };

  const processNextPan = (): void => {
    if (state.panQueue.length === 0) {
      state.isProcessingPan = false;
      clearQueueTimeout();
      return;
    }

    state.isProcessingPan = true;
    const movement = state.panQueue.shift();
    if (!movement) return;
    const { deltaX, deltaY } = movement;

    // Add timeout protection to prevent a stuck queue
    clearQueueTimeout();
    state.queueTimeoutTimer = setTimeout(() => {
      if (state.isProcessingPan) {
        state.isProcessingPan = false;
        processNextPan();
      }
    }, QUEUE_TIMEOUT_MS);

    panMap(deltaX, deltaY);
  };

  const panMap = (deltaX: number, deltaY: number): void => {
    const pos = component.position;
    if (!pos || !pos.center) return;
    const { center } = pos;
    const panDistance = calculatePanDistance();
    
    // Handle both array and object center formats
    const [currentX, currentY] = Array.isArray(center)
      ? center
      : [center.x, center.y];
    const newCenter = [
      currentX + deltaX * panDistance, 
      currentY + deltaY * panDistance
    ];

    // Use the same logic as other position changes: call setPosition with animateFast = true
    component.setPosition({
      ...pos,
      center: newCenter,
    }, true);
  };

  const handleZoom = (zoomDirection: number): void => {
    const currentZoom = component.position?.zoom || 10;
    const newZoom = Math.max(1, Math.min(28, currentZoom + zoomDirection));

    // Only update if zoom level actually changes
    if (newZoom !== currentZoom) {
      // Use the same logic as zoom buttons: call setPosition with animateFast = true
      component.setPosition({
        ...component.position,
        zoom: newZoom,
      }, true);
    }
  };

  const stopPanning = () => {
    // Clear the queue and stop processing
    state.panQueue = [];
    state.isProcessingPan = false;
    clearQueueTimeout();
    
    // Cancel current animation directly if host exposes API; fall back to emit for legacy
    if (typeof component.cancelPanAnimation === "function") {
      component.cancelPanAnimation();
    } else if (component.$refs?.map?.cancelPanAnimation) {
      component.$refs.map.cancelPanAnimation();
    } else {
      component.$emit("cancel-pan-animation");
    }
  };

  const startKeyRepeat = () => {
    stopKeyRepeat();
    state.keyRepeatTimer = setInterval(() => panFromPressedKeys(), KEY_REPEAT_INTERVAL);
  };

  // Event handlers
  const handleKeyDown = (event: KeyboardEvent): void => {
    if (isTypingInField()) return;

    const key = event.key;

    // Handle zoom keys
    if (key in ZOOM_KEYS) {
      // Allow browser/system zoom shortcuts (Ctrl/Cmd + +/-) to work
      if (event.ctrlKey || event.metaKey) {
        return;
      }

      event.preventDefault();

      // Ignore auto-repeat for zoom to prevent rapid zooming
      if (event.repeat) return;

      handleZoom(ZOOM_KEYS[key]);
      return;
    }

    // Handle arrow keys for panning
    if (!(key in ARROW_VEC)) return;

    event.preventDefault();
    state.pressedKeys.add(key);

    // Ignore auto-repeat if the timer is already running
    if (event.repeat && state.keyRepeatTimer) return;

    panFromPressedKeys();
    startKeyRepeat();
  };

  const handleKeyUp = (event: KeyboardEvent): void => {
    state.pressedKeys.delete(event.key);
    if (state.pressedKeys.size === 0) {
      stopKeyRepeat();
      stopPanning();
    }
  };

  const handleBlur = () => {
    stopKeyRepeat();
    stopPanning();
    state.pressedKeys.clear();
  };

  // Public API
  return {
    init() {
      window.addEventListener('beforeunload', handleBlur);
    },

    cleanup() {
      stopKeyRepeat();
      window.removeEventListener('beforeunload', handleBlur);
      stopPanning();
      clearQueueTimeout();
    },

    handleKeyDown,
    handleKeyUp,
    handleBlur,
    processNextPan,
  };
};

