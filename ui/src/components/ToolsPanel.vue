<template>
    <div class="wrapper">
        <div class="buttons" :class="{ showMeasureMenu }">
            <button
                v-if="this.features.selectarea"
                class="iconbutton"
                :class="{ isActive: tool === 'SELECT_AREA' }"
                @click="toggleSelectArea"
                v-tippy="{ placement: 'bottom' }"
                content="Selecteer gebied"
                aria-label="Selecteer gebied"
            >
                <svg width="18" height="18" xmlns="http://www.w3.org/2000/svg">
                    <path
                        d="M14 2h-2V0h2v2zm-2 16h2v-2.59L16.59 18 18 16.59 15.41 14H18v-2h-6v6zm4-12h2V4h-2v2zm0 4h2V8h-2v2zm-8 8h2v-2H8v2zM4 2h2V0H4v2zM0 14h2v-2H0v2zm2 4v-2H0c0 1.1.9 2 2 2zM16 0v2h2c0-1.1-.9-2-2-2zM8 2h2V0H8v2zM0 6h2V4H0v2zm4 12h2v-2H4v2zm-4-8h2V8H0v2zm0-8h2V0C.9 0 0 .9 0 2z"
                        fill="currentColor"
                        fill-rule="nonzero"
                    />
                </svg>
            </button>

            <button
                v-if="this.features.measure"
                class="iconbutton"
                :class="{ isActive: tool === 'MEASURE_AREA' || tool === 'MEASURE_LINE' }"
                @click="toggleMeasure"
                v-tippy="{ placement: 'bottom' }"
                content="Opmeten"
                aria-label="Opmeten"
            >
                <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24">
                    <path d="M0 0h24v24H0z" fill="none" />
                    <path
                        fill="currentColor"
                        d="M21 6H3c-1.1 0-2 .9-2 2v8c0 1.1.9 2 2 2h18c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm0 10H3V8h2v4h2V8h2v4h2V8h2v4h2V8h2v4h2V8h2v8z"
                    />
                </svg>
            </button>
        </div>

        <transition name="fade">
            <div class="menu" v-if="showMeasureMenu">
                <ul class="list">
                    <li>
                        <button
                            @click="() => setMeasureTool('MEASURE_AREA')"
                            aria-label="Meet oppervlakte"
                        >
                            Oppervlakte
                        </button>
                    </li>
                    <li>
                        <button
                            @click="() => setMeasureTool('MEASURE_LINE')"
                            aria-label="Meet afstand"
                        >
                            Afstand
                        </button>
                    </li>
                </ul>
            </div>
        </transition>
    </div>
</template>

<script>
export default {
    name: 'ToolsPanel',
    data() {
        return {
            showMeasureMenu: false,
        }
    },
    methods: {
        toggleMeasure() {
            if (this.tool === 'MEASURE_AREA' || this.tool === 'MEASURE_LINE') {
                this.$emit('set-tool', '')
            } else {
                this.showMeasureMenu = !this.showMeasureMenu
            }
        },
        toggleSelectArea() {
            if (this.tool !== 'SELECT_AREA') {
                this.$emit('set-tool', 'SELECT_AREA')
            } else {
                // toggle off when the user is currently selecting an area
                this.$emit('set-tool', '')
                this.$emit('set-selected-area', null)
            }
        },
        setMeasureTool(chosenTool) {
            this.$emit('set-tool', this.tool !== chosenTool ? chosenTool : '')
            this.showMeasureMenu = false
        },
    },
    props: {
        tool: String,
        features: {
            type: Object,
            default: () => {
                return {
                    selectarea: true,
                    measure: true,
                }
            },
        },
    },
}
</script>

<style scoped>
.wrapper {
    position: relative;
    margin-right: 12px;
}

.buttons {
    display: flex;
    background: white;
    overflow: hidden;
    border-radius: var(--radius-normal);
    box-shadow: var(--shadow-normal);
}

.buttons.showMeasureMenu {
    border-bottom-left-radius: 0;
    border-bottom-right-radius: 0;
}

.iconbutton {
    width: var(--width-button-large);
    height: var(--width-button-large);
}

.iconbutton:not(:last-child) {
    border-right: 1px solid var(--color-grey-50);
}

.iconbutton.isActive {
    color: var(--color-primary);
}

.menu {
    position: absolute;
    top: var(--width-button-large);
    right: 0;
    padding: 6px 0;
    background: white;
    border-radius: var(--radius-small);
    border-top-right-radius: 0;
    box-shadow: var(--shadow-normal);
}

.list a,
.list button {
    display: block;
    width: 100%;
    color: black;
    text-decoration: none;
    padding: 4px 12px;
    font-size: var(--font-size-small);
}

.list a:hover,
.list button:hover {
    background: var(--color-grey-40);
}

.list a:active,
.list button:active {
    background: var(--color-grey-50);
}
</style>
