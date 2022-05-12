<template>
    <div class="content">
        <div class="header">
            <button
                class="iconbutton __normal __outline"
                type="button"
                aria-label="Ga terug"
                v-tippy="{ placement: 'bottom' }"
                content="Terug"
                @click="() => this.$emit('show-form')"
            >
                <svg
                    width="24px"
                    height="24px"
                    viewBox="0 0 24 24"
                    version="1.1"
                    xmlns="http://www.w3.org/2000/svg"
                    xmlns:xlink="http://www.w3.org/1999/xlink"
                >
                    <title>arrow_back_black_24dp</title>
                    <g id="Admin" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
                        <g id="Kaart---Zoekbalk" transform="translate(-24.000000, -24.000000)">
                            <g
                                id="arrow_back_black_24dp"
                                transform="translate(16.000000, 16.000000)"
                            >
                                <g transform="translate(8.000000, 8.000000)">
                                    <polygon id="Path" points="0 0 24 0 24 24 0 24"></polygon>
                                    <polygon
                                        id="Path"
                                        fill="#000000"
                                        fill-rule="nonzero"
                                        points="20 11 7.83 11 13.42 5.41 12 4 4 12 12 20 13.41 18.59 7.83 13 20 13"
                                    ></polygon>
                                </g>
                            </g>
                        </g>
                    </g>
                </svg>
            </button>
            <h1>
                <svg
                    width="24px"
                    height="24px"
                    viewBox="0 0 24 24"
                    version="1.1"
                    xmlns="http://www.w3.org/2000/svg"
                    xmlns:xlink="http://www.w3.org/1999/xlink"
                >
                    <title>Artboard</title>
                    <g id="Artboard" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
                        <g
                            id="lagen"
                            transform="translate(3.000000, 2.000000)"
                            fill="#000000"
                            fill-rule="nonzero"
                        >
                            <path
                                d="M8.99,17.7805 L1.62,11.62075 L0,12.97525 L9,20.50025 L18,12.97525 L16.37,11.61 L8.99,17.7805 Z M9,15.05 L16.36,8.89025 L18,7.525 L9,0 L0,7.525 L1.63,8.89025 L9,15.05 Z M9,2.71975 L14.74,7.525 L9,12.33025 L3.26,7.525 L9,2.71975 Z"
                                id="Shape"
                            ></path>
                        </g>
                    </g>
                </svg>
                Lijstweergave
            </h1>
            <div class="header-spacer" />
        </div>

        <input
            type="text"
            name="title"
            class="title-input"
            placeholder="Template titel"
            v-model="data.settings.title"
        />

        <textarea
            type="text"
            name="title"
            class="short-description-input"
            placeholder="Template korte beschrijving"
            v-model="data.settings.short_description"
        />
    </div>
</template>

<script>
export default {
    name: 'ListPanelAdmin',
    props: {
        initialData: Object,
    },
    methods: {},
    computed: {},
    data() {
        return {
            data: this.initialData,
        }
    },
}
</script>

<style scoped>
.header {
    display: flex;
    justify-content: space-between;
}

.header-spacer {
    width: 40px;
}

.settings {
    margin-top: 24px;
}

.settings + .settings {
    margin-top: 40px;
}

.setting .iconbutton {
    margin-left: auto;
}

.search-wrapper {
    position: relative;
    border-top: 1px solid var(--color-grey-80);
    border-bottom: 1px solid var(--color-grey-80);
    margin-bottom: -1px;
}

.search-wrapper svg {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 16px;
    margin: auto 0;
    pointer-events: none;
}

.search-wrapper input {
    width: 100%;
    height: 48px;
    padding: 0 0 0 48px;
}

.short-description-input {
    width: 100%;
    min-height: 100px;
}
</style>
