<template>
    <aside class="wrapper" :class="{ large, fullScreen }" v-if="showPanel">
        <button
            v-if="this.$listeners['toggle-side-panel']"
            @click="toggleSidePanel"
            v-tippy="{ placement: 'right' }"
            content="Verberg paneel"
            aria-label="Verberg paneel"
            class="iconbutton resize-button"
        >
            <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24">
                <path d="M0 0h24v24H0V0z" fill="none" />
                <path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12l4.58-4.59z" />
            </svg>
        </button>
        <button
            v-if="large && !fullScreen"
            @click="toggleFullScreen"
            v-tippy="{ placement: 'right' }"
            content="Vergroot paneel"
            aria-label="Vergroot paneel"
            class="iconbutton resize-button"
        >
            <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24">
                <path d="M0 0h24v24H0z" fill="none" />
                <path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z" />
            </svg>
        </button>
        <button
            @click="toggleFullScreen"
            v-tippy="{ placement: 'bottom' }"
            :content="fullScreen ? 'Verklein paneel' : 'Vergroot paneel'"
            :aria-label="fullScreen ? 'Verklein paneel' : 'Vergroot paneel'"
            class="iconbutton expand-mobile-button"
        >
            <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24">
                <path d="M0 0h24v24H0z" fill="none" />
                <path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z" />
            </svg>
        </button>
        <button
            v-if="large && fullScreen"
            @click="toggleFullScreen"
            v-tippy="{ placement: 'left' }"
            content="Verklein paneel"
            aria-label="Verklein paneel"
            class="iconbutton resize-button exit-fullscreen"
        >
            <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24">
                <path d="M0 0h24v24H0V0z" fill="none" />
                <path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12l4.58-4.59z" />
            </svg>
        </button>

        <div class="header">
            <slot name="search"></slot>
        </div>

        <div class="content">
            <slot></slot>
        </div>
    </aside>
</template>

<script>
export default {
    name: 'SidePanel',
    methods: {
        toggleSidePanel() {
            this.$emit('toggle-side-panel')
        },
        toggleFullScreen() {
            this.fullScreen = !this.fullScreen
        },
    },
    data() {
        return {
            fullScreen: false,
        }
    },
    props: {
        large: Boolean,
        showPanel: Boolean,
    },
}
</script>

<style scoped>
.wrapper {
    position: relative;
    flex-shrink: 0;
    z-index: 1;
    width: 100%;
    background: white;
    box-shadow: var(--shadow-normal);
    display: flex;
    flex-direction: column;
}

@media (max-width: 575px) {
    .wrapper {
        height: calc(40 * var(--vh));
    }

    .wrapper.fullScreen {
        height: 100%;
    }
}

@media (min-width: 576px) {
    .wrapper {
        height: 100%;
        max-width: var(--width-detail);
    }

    .wrapper.large {
        max-width: 50%;
    }

    .wrapper.fullScreen {
        max-width: 100%;
    }
}

.header {
    width: 100%;
    padding: var(--padding-screen);
    padding-bottom: 0;
}

.content {
    position: relative;
    flex-grow: 1;
    overflow-y: auto;
    padding: 16px 0;
}

.resize-button {
    position: absolute;
    top: var(--padding-screen);
    right: -24px;
    width: 24px;
    height: var(--width-button-large);
    border-top-right-radius: var(--radius-small);
    border-bottom-right-radius: var(--radius-small);
    background: white;
    box-shadow: var(--shadow-normal);
}

.resize-button:before {
    content: '';
    position: absolute;
    top: -8px;
    bottom: -8px;
    width: 8px;
    left: -8px;
    background: white;
    pointer-events: none;
}

@media (max-width: 575px) {
    .resize-button {
        display: none;
    }
}

.expand-mobile-button {
    position: absolute;
    background: white;
    box-shadow: var(--shadow-normal);
    width: var(--width-button-large);
    height: 24px;
    top: -24px;
    left: 0;
    right: 0;
    margin: 0 auto;
    border-top-left-radius: var(--radius-small);
    border-top-right-radius: var(--radius-small);
    z-index: 1;
}

.wrapper.fullScreen .expand-mobile-button {
    top: 0;
    border: 1px solid var(--color-grey-60);
    border-top: none;
    box-shadow: none;
    border-radius: 0;
    border-bottom-left-radius: var(--radius-small);
    border-bottom-right-radius: var(--radius-small);
}

.wrapper.fullScreen .expand-mobile-button svg {
    transform: rotate(90deg);
}

.wrapper.fullScreen .expand-mobile-button:before {
    content: none;
}

@media (min-width: 576px) {
    .expand-mobile-button {
        display: none;
    }
}

.expand-mobile-button svg {
    transform: rotate(-90deg);
}

.expand-mobile-button:before {
    content: '';
    position: absolute;
    left: -8px;
    right: -8px;
    height: 8px;
    bottom: -8px;
    background: white;
    pointer-events: none;
}

.exit-fullscreen {
    right: 0;
    border-top-right-radius: 0;
    border-bottom-right-radius: 0;
    border-top-left-radius: var(--radius-small);
    border-bottom-left-radius: var(--radius-small);
    border: 1px solid var(--color-grey-60);
    border-right: none;
    box-shadow: none;
}

.exit-fullscreen:before {
    content: none;
}
</style>
