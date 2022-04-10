<template>
    <form method="POST" @submit="this.submitForm">
        <h1>
            <svg
                xmlns="http://www.w3.org/2000/svg"
                height="24px"
                viewBox="0 0 24 24"
                width="24px"
                fill="#000000"
            >
                <path d="M0 0h24v24H0V0z" fill="none" />
                <path
                    d="M20.5 3l-.16.03L15 5.1 9 3 3.36 4.9c-.21.07-.36.25-.36.48V20.5c0 .28.22.5.5.5l.16-.03L9 18.9l6 2.1 5.64-1.9c.21-.07.36-.25.36-.48V3.5c0-.28-.22-.5-.5-.5zM10 5.47l4 1.4v11.66l-4-1.4V5.47zm-5 .99l3-1.01v11.7l-3 1.16V6.46zm14 11.08l-3 1.01V6.86l3-1.16v11.84z"
                />
            </svg>
            Kaart
        </h1>
        <input
            type="text"
            name="title"
            class="input"
            placeholder="Titel van de kaart"
            v-model="data.title"
            required
        />

        <div class="settings">
            <button type="button" @click="() => this.$emit('show-layers')" class="setting">
                <svg
                    class="setting-icon"
                    width="28px"
                    height="28px"
                    viewBox="0 0 28 28"
                    version="1.1"
                    xmlns="http://www.w3.org/2000/svg"
                    xmlns:xlink="http://www.w3.org/1999/xlink"
                >
                    <title>icon/layers</title>
                    <g
                        id="icon/layers"
                        stroke="none"
                        stroke-width="1"
                        fill="none"
                        fill-rule="evenodd"
                    >
                        <path
                            d="M13.99,21.7805 L6.62,15.62075 L5,16.97525 L14,24.50025 L23,16.97525 L21.37,15.61 L13.99,21.7805 Z M14,19.05 L21.36,12.89025 L23,11.525 L14,4 L5,11.525 L6.63,12.89025 L14,19.05 Z M14,6.71975 L19.74,11.525 L14,16.33025 L8.26,11.525 L14,6.71975 Z"
                            id="Shape"
                            fill="#000000"
                            fill-rule="nonzero"
                        ></path>
                    </g>
                </svg>
                Lagen
                <svg
                    class="setting-chevron"
                    width="6px"
                    height="9px"
                    viewBox="0 0 6 9"
                    version="1.1"
                    xmlns="http://www.w3.org/2000/svg"
                    xmlns:xlink="http://www.w3.org/1999/xlink"
                >
                    <title>icon/chevron-right</title>
                    <g id="Symbols" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
                        <g
                            id="setting-icon"
                            transform="translate(-284.000000, -16.000000)"
                            fill="#000000"
                            fill-rule="nonzero"
                        >
                            <g id="Path" transform="translate(284.000000, 16.000000)">
                                <polygon
                                    points="1.0575 0 0 1.0575 3.435 4.5 0 7.9425 1.0575 9 5.5575 4.5"
                                ></polygon>
                            </g>
                        </g>
                    </g>
                </svg>
            </button>
        </div>

        <div class="settings">
            <div class="setting">
                <input
                    id="features.searchbar"
                    type="checkbox"
                    name="features.searchbar"
                    v-model="data.features.searchbar"
                />
                <label for="features.searchbar">Toon zoekbalk</label>
            </div>

            <div class="setting">
                <input
                    id="features.selectarea"
                    type="checkbox"
                    name="features.selectarea"
                    v-model="data.features.selectarea"
                />
                <label for="features.selectarea">Selecteer gebied</label>
            </div>

            <div class="setting">
                <input
                    id="features.measure"
                    type="checkbox"
                    name="features.measure"
                    v-model="data.features.measure"
                />
                <label for="features.measure">Opmeten</label>
            </div>

            <div class="setting">
                <input
                    id="features.gps"
                    type="checkbox"
                    name="features.gps"
                    v-model="data.features.gps"
                />
                <label for="features.gps">GPS knop</label>
            </div>

            <div class="setting">
                <input
                    id="features.streetview"
                    type="checkbox"
                    name="features.streetview"
                    v-model="data.features.streetview"
                />
                <label for="features.streetview">Rondkijkfoto / obliek</label>
            </div>

            <div class="setting">
                <input
                    id="features.zoom"
                    type="checkbox"
                    name="features.zoom"
                    v-model="data.features.zoom"
                />
                <label for="features.zoom">Zoomfunctie</label>
            </div>

            <div class="setting">
                <input
                    id="features.scale"
                    type="checkbox"
                    name="features.scale"
                    v-model="data.features.scale"
                />
                <label for="features.scale">Toon schaal</label>
            </div>

            <div class="setting">
                <input
                    id="features.layerlist"
                    type="checkbox"
                    name="features.layerlist"
                    v-model="data.features.layerlist"
                />
                <label for="features.layerlist">Lagenlijst</label>
            </div>
        </div>

        <div class="flexer">
            <router-link to="/maps" class="button __tertiary">Annuleer</router-link>
            <button type="submit" class="button __primary">Opslaan</button>
        </div>
    </form>
</template>

<script>
export default {
    name: 'MapForm',
    props: {
        initialData: Object,
    },
    methods: {
        submitForm(e) {
            e.preventDefault()
            this.$emit('submit', this.data)
        },
    },
    data() {
        return {
            data: this.initialData || { features: {} },
        }
    },
}
</script>

<style scoped>
.map-form {
    width: 100%;
}

.flexer {
    position: absolute;
    bottom: var(--padding-screen);
    left: 0;
    right: 0;
}

.settings {
    margin: 32px calc(var(--padding-screen) * -1) 0;
}

.setting {
    width: 100%;
    height: 40px;
    padding: 0 16px;
    display: flex;
    align-items: center;
    font-weight: var(--font-weight-bold);
    border-top: 1px solid var(--color-grey-60);
}

.setting:last-child {
    border-bottom: 1px solid var(--color-grey-60);
}

.setting-icon {
    margin-right: 10px;
}

.setting-chevron {
    margin-left: auto;
}

.setting input[type='checkbox'] {
    width: 28px;
    margin-right: 10px;
    cursor: pointer;
}

.setting input[type='checkbox'] + label {
    flex-grow: 1;
    align-self: stretch;
    display: flex;
    align-items: center;
    cursor: pointer;
}
</style>
