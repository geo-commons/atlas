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
  "_": 0,
};

interface PanMovement {
  deltaX: number;
  deltaY: number;
}

interface PanningData {
  pressedKeys: Set<string>;
  keyRepeatTimer: number | null;
  panQueue: PanMovement[];
  isProcessingPan: boolean;
  queueTimeoutTimer: number | null;
  lastZoom: number | null;
  cachedPanDistance: number | null;
}

const panning = {
  data(): PanningData {
    return {
      pressedKeys: new Set<string>(),
      keyRepeatTimer: null,
      panQueue: [],
      isProcessingPan: false,
      queueTimeoutTimer: null,
      lastZoom: null,
      cachedPanDistance: null,
    };
  },

  computed: {
    /**
     * Calculates and caches the pan distance based on current zoom level.
     * The distance decreases as zoom level increases for more precise control.
     * @returns {number} The calculated pan distance in map units
     */
    panDistance(): number {
      if ((this as any).position?.zoom !== (this as any).lastZoom) {
        (this as any).lastZoom = (this as any).position?.zoom;
        (this as any).cachedPanDistance = PAN_DISTANCE_FACTOR * Math.pow(2, ZOOM_BASE_LEVEL - ((this as any).position?.zoom || 10));
      }
      return (this as any).cachedPanDistance || PAN_DISTANCE_FACTOR;
    },
  },

  methods: {
    /**
     * Handles key down events for panning and zooming.
     * Prevents default behavior for arrow keys and zoom keys.
     * @param {KeyboardEvent} event - The keyboard event
     */
    handleKeyDown(event: KeyboardEvent): void {
      if (this.isTypingInField()) return;

      const key = event.key;

      // Handle zoom keys
      if (key in ZOOM_KEYS) {
        event.preventDefault();

        // Ignore auto-repeat for zoom to prevent rapid zooming
        if (event.repeat) return;

        this.handleZoom(ZOOM_KEYS[key]);
        return;
      }

      // Handle arrow keys for panning
      if (!(key in ARROW_VEC)) return;

      event.preventDefault();
      (this as any).pressedKeys.add(key);

      // Ignore auto-repeat if the timer is already running
      if (event.repeat && (this as any).keyRepeatTimer) return;

      this.panFromPressedKeys();
      this.startKeyRepeat();
    },

    /**
     * Handles key up events to stop panning when keys are released.
     * @param {KeyboardEvent} event - The keyboard event
     */
    handleKeyUp(event: KeyboardEvent): void {
      (this as any).pressedKeys.delete(event.key);
      if ((this as any).pressedKeys.size === 0) {
        this.stopKeyRepeat();
        this.stopPanning();
      }
    },

    /**
     * Handles window blur events to stop all panning operations.
     * Useful when the user switches to another window or tab.
     */
    handleBlur(): void {
      this.stopKeyRepeat();
      this.stopPanning();
      (this as any).pressedKeys.clear();
    },

    /**
     * Stops all panning operations and clears the movement queue.
     * Cancels any ongoing pan animations.
     */
    stopPanning(): void {
      // Clear the queue and stop processing
      (this as any).panQueue = [];
      (this as any).isProcessingPan = false;
      this.clearQueueTimeout();
      
      // Cancel current animation directly if host exposes API; fall back to emit for legacy
      if (typeof (this as any).cancelPanAnimation === "function") {
        (this as any).cancelPanAnimation();
      } else if ((this as any).$refs?.map?.cancelPanAnimation) {
        (this as any).$refs.map.cancelPanAnimation();
      } else {
        (this as any).$emit("cancel-pan-animation");
      }
    },

    /**
     * Checks if the user is currently typing in an input field.
     * Prevents panning when user is interacting with form elements.
     * @returns {boolean} True if user is typing in a field
     */
    isTypingInField(): boolean {
      const activeElement = document.activeElement;
      return !!activeElement && (
        activeElement.matches('input, textarea, select, [role="textbox"]') || 
        (activeElement as HTMLElement).isContentEditable === true
      );
    },

    /**
     * Starts the key repeat timer for continuous panning while keys are held.
     * Clears any existing timer before starting a new one.
     */
    startKeyRepeat(): void {
      this.stopKeyRepeat();
      (this as any).keyRepeatTimer = setInterval(() => this.panFromPressedKeys(), KEY_REPEAT_INTERVAL);
    },

    /**
     * Stops the key repeat timer and clears the interval.
     */
    stopKeyRepeat(): void {
      if (!(this as any).keyRepeatTimer) return;
      clearInterval((this as any).keyRepeatTimer);
      (this as any).keyRepeatTimer = null;
    },

    /**
     * Clears the queue timeout timer to prevent stuck pan operations.
     */
    clearQueueTimeout(): void {
      if ((this as any).queueTimeoutTimer) {
        clearTimeout((this as any).queueTimeoutTimer);
        (this as any).queueTimeoutTimer = null;
      }
    },

    /**
     * Calculates the total movement vector from all currently pressed arrow keys.
     * Queues the movement for processing.
     */
    panFromPressedKeys(): void {
      let totalDeltaX = 0;
      let totalDeltaY = 0;
      
      for (const key of (this as any).pressedKeys) {
        const movementVector = ARROW_VEC[key];
        if (movementVector) {
          totalDeltaX += movementVector[0];
          totalDeltaY += movementVector[1];
        }
      }
      
      if (totalDeltaX || totalDeltaY) {
        this.queuePanMovement(totalDeltaX, totalDeltaY);
      }
    },

    /**
     * Adds a pan movement to the queue for processing.
     * Starts processing if not already in progress.
     * @param {number} deltaX - Horizontal movement direction (-1, 0, or 1)
     * @param {number} deltaY - Vertical movement direction (-1, 0, or 1)
     */
    queuePanMovement(deltaX: number, deltaY: number): void {
      (this as any).panQueue.push({ deltaX, deltaY });
      if (!(this as any).isProcessingPan) {
        this.processNextPan();
      }
    },

    /**
     * Processes the next pan movement in the queue.
     * Includes timeout protection to prevent stuck operations.
     */
    processNextPan(): void {
      if ((this as any).panQueue.length === 0) {
        (this as any).isProcessingPan = false;
        this.clearQueueTimeout();
        return;
      }

      (this as any).isProcessingPan = true;
      const { deltaX, deltaY } = (this as any).panQueue.shift()!;

      // Add timeout protection to prevent a stuck queue
      this.clearQueueTimeout();
      (this as any).queueTimeoutTimer = setTimeout(() => {
        if ((this as any).isProcessingPan) {
          (this as any).isProcessingPan = false;
          this.processNextPan();
        }
      }, QUEUE_TIMEOUT_MS);

      this.panMap(deltaX, deltaY);
    },

    /**
     * Executes the actual map panning operation.
     * Calculates new center position based on current position and movement deltas.
     * @param {number} deltaX - Horizontal movement direction (-1, 0, or 1)
     * @param {number} deltaY - Vertical movement direction (-1, 0, or 1)
     */
    panMap(deltaX: number, deltaY: number): void {
      const { center } = (this as any).position;
      const panDistance = (this as any).panDistance;
      
      // Handle both array and object center formats
      const [currentX, currentY] = Array.isArray(center) ? center : [center.x, center.y];
      const newCenter: [number, number] = [
        currentX + deltaX * panDistance, 
        currentY + deltaY * panDistance
      ];

      (this as any).setPosition({ ...(this as any).position, center: newCenter, animateFast: true }, true);
    },

    /**
     * Handles zoom operations with bounds checking.
     * @param {number} zoomDirection - Direction of zoom (1 for zoom in, -1 for zoom out)
     */
    handleZoom(zoomDirection: number): void {
      const currentZoom = (this as any).position?.zoom || 10;
      const newZoom = Math.max(1, Math.min(28, currentZoom + zoomDirection));

      // Only update if zoom level actually changes
      if (newZoom !== currentZoom) {
        (this as any).setPosition({ ...(this as any).position, zoom: newZoom }, true);
      }
    },
  },
};

export default panning;
