// Configuration constants
const PAN_DISTANCE_FACTOR = 2500;
const ZOOM_BASE_LEVEL = 13;
const KEY_REPEAT_INTERVAL = 200;
const QUEUE_TIMEOUT_MS = 0;

// Arrow key to movement vector
const ARROW_VEC = {
  ArrowUp: [0, 1],
  ArrowDown: [0, -1],
  ArrowLeft: [-1, 0],
  ArrowRight: [1, 0],
};

// Zoom keys
const ZOOM_KEYS = {
  "+": 1,
  "-": -1,
};

const panning = {
  data() {
    return {
      pressedKeys: new Set(),
      keyRepeatTimer: null,
      panQueue: [],
      isProcessingPan: false,
      queueTimeoutTimer: null,
      lastZoom: null,
      cachedPanDistance: null,
    };
  },

  computed: {
    // Cache pan distance based on current zoom level
    panDistance() {
      if (this.position?.zoom !== this.lastZoom) {
        this.lastZoom = this.position?.zoom;
        this.cachedPanDistance = PAN_DISTANCE_FACTOR * Math.pow(2, ZOOM_BASE_LEVEL - (this.position?.zoom || 10));
      }
      return this.cachedPanDistance || PAN_DISTANCE_FACTOR;
    },
  },

  methods: {
    handleKeyDown(event) {
      if (this.isTypingInField()) return;

      const key = event.key;

      // Handle zoom keys
      if (key in ZOOM_KEYS) {
        event.preventDefault();

        // Ignore auto-repeat for zoom
        if (event.repeat) return;

        this.handleZoom(ZOOM_KEYS[key]);
        return;
      }

      // Handle arrow keys for panning
      if (!(key in ARROW_VEC)) return;

      event.preventDefault();
      this.pressedKeys.add(key);

      // Ignore auto-repeat if the timer is already running
      if (event.repeat && this.keyRepeatTimer) return;

      this.panFromPressedKeys();
      this.startKeyRepeat();
    },

    handleKeyUp(event) {
      this.pressedKeys.delete(event.key);
      if (this.pressedKeys.size === 0) {
        this.stopKeyRepeat();
        this.stopPanning();
      }
    },

    handleBlur() {
      this.stopKeyRepeat();
      this.stopPanning();
      this.pressedKeys.clear();
    },

    stopPanning() {
      // Clear the queue and stop processing
      this.panQueue = [];
      this.isProcessingPan = false;
      this.clearQueueTimeout();
      // Emit event to cancel current animation
      this.$emit("cancel-pan-animation");
    },

    isTypingInField() {
      const el = document.activeElement;
      return !!el && (el.matches('input, textarea, select, [role="textbox"]') || el.isContentEditable === true);
    },

    startKeyRepeat() {
      this.stopKeyRepeat();
      this.keyRepeatTimer = setInterval(this.panFromPressedKeys, KEY_REPEAT_INTERVAL);
    },

    stopKeyRepeat() {
      if (!this.keyRepeatTimer) return;
      clearInterval(this.keyRepeatTimer);
      this.keyRepeatTimer = null;
    },

    clearQueueTimeout() {
      if (this.queueTimeoutTimer) {
        clearTimeout(this.queueTimeoutTimer);
        this.queueTimeoutTimer = null;
      }
    },

    panFromPressedKeys() {
      let dx = 0,
        dy = 0;
      for (const key of this.pressedKeys) {
        const v = ARROW_VEC[key];
        if (v) {
          dx += v[0];
          dy += v[1];
        }
      }
      if (dx || dy) this.queuePanMovement(dx, dy);
    },

    queuePanMovement(dx, dy) {
      this.panQueue.push({ dx, dy });
      if (!this.isProcessingPan) {
        this.processNextPan();
      }
    },

    processNextPan() {
      if (this.panQueue.length === 0) {
        this.isProcessingPan = false;
        this.clearQueueTimeout();
        return;
      }

      this.isProcessingPan = true;
      const { dx, dy } = this.panQueue.shift();

      // Add timeout protection to prevent stuck queue
      this.clearQueueTimeout();
      this.queueTimeoutTimer = setTimeout(() => {
        if (this.isProcessingPan && this.panQueue.length === 0) {
          console.warn("Pan queue timeout - resetting processing state");
          this.isProcessingPan = false;
        }
      }, QUEUE_TIMEOUT_MS);

      this.panMap(dx, dy);
    },

    panMap(dx, dy) {
      const { center } = this.position;
      const distance = this.panDistance;
      const [x, y] = Array.isArray(center) ? center : [center.x, center.y];
      const newCenter = [x + dx * distance, y + dy * distance];

      this.setPosition({ ...this.position, center: newCenter, animateFast: true }, true);
    },

    handleZoom(zoomDirection) {
      const currentZoom = this.position?.zoom || 10;
      const newZoom = Math.max(1, Math.min(20, currentZoom + zoomDirection));

      // Only update if zoom level actually changes
      if (newZoom !== currentZoom) {
        this.setPosition({ ...this.position, zoom: newZoom }, true);
      }
    },
  },
};

export default panning;
