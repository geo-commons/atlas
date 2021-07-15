<template>
    <tippy
        placement="right-start"
        theme="popover"
        trigger="click"
        :delay="[0, 0]"
        :a11y="false"
        :animateFill="false"
        :touch="true"
        :touchHold="false"
    >
        <template v-slot:trigger>
            <button class="iconbutton" aria-label="Toon meer informatie">
                <svg
                    width="16px"
                    height="16px"
                    viewBox="0 0 16 16"
                    version="1.1"
                    xmlns="http://www.w3.org/2000/svg"
                    xmlns:xlink="http://www.w3.org/1999/xlink"
                >
                    <g id="Page-1" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
                        <g
                            id="info_black_18dp"
                            transform="translate(-1.000000, -1.000000)"
                            fill="#000000"
                            fill-rule="nonzero"
                        >
                            <path
                                d="M8.25,5.25 L9.75,5.25 L9.75,6.75 L8.25,6.75 L8.25,5.25 Z M8.25,8.25 L9.75,8.25 L9.75,12.75 L8.25,12.75 L8.25,8.25 Z M9,1.5 C4.86,1.5 1.5,4.86 1.5,9 C1.5,13.14 4.86,16.5 9,16.5 C13.14,16.5 16.5,13.14 16.5,9 C16.5,4.86 13.14,1.5 9,1.5 Z M9,15 C5.6925,15 3,12.3075 3,9 C3,5.6925 5.6925,3 9,3 C12.3075,3 15,5.6925 15,9 C15,12.3075 12.3075,15 9,15 Z"
                                id="Shape"
                            ></path>
                        </g>
                    </g>
                </svg>
            </button>
        </template>
        <div class="container">
            <div class="heading">
                <h3 class="title">{{ layer.title }}</h3>
                <span class="description">{{ layer.metadata.description }}</span>
            </div>
            <div class="properties">
                <div class="property">
                    <div class="key">Beheerder</div>
                    <div class="value">{{ layer.metadata.organization }}</div>
                </div>
                <div class="property">
                    <div class="key">Bijgewerkt</div>
                    <div class="value">{{ layer.metadata.updated }}</div>
                </div>
            </div>
        </div>
    </tippy>
</template>

<script>
export default {
    name: 'LayerInfo',
    props: {
        layer: Object,
    },
}
</script>

<style scoped>
.iconbutton {
    margin-right: 5px;
    width: 24px;
    height: 24px;
    border-radius: 50%;
}

@media (min-width: 768px) {
    .iconbutton {
        opacity: 0;
    }
}

.sublayer:hover .iconbutton,
.tippy-active > .iconbutton,
.keyboard-user .iconbutton:focus {
    opacity: 1;
}

.container {
    min-width: 240px;
    max-width: 300px;
    font-weight: normal;
    text-align: left;
    font-size: var(--font-size-small);
}

.heading {
    padding: 10px 16px;
    text-align: center;
    border-bottom: 1px solid var(--color-grey-60);
}

.title {
    margin: 0 0 4px;
    font-size: var(--font-size-normal);
    font-weight: var(--font-weight-bold);
}

.properties {
    padding: 8px 16px;
}

.property {
    display: flex;
    justify-content: space-between;
    padding: 3px 0;
}

.key {
    padding-right: 8px;
    color: var(--color-text-grey);
}

.value {
    text-align: right;
}
</style>
