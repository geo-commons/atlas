<template>
    <div class="app">
        <Header />
        <Content>
            <router-view></router-view>
        </Content>
    </div>
</template>

<script>
import Header from './components/Header.vue'
import Content from './components/Content.vue'

export default {
    name: 'App',
    components: {
        Header,
        Content,
    },
}
</script>

<style>
:root {
    --color-text-grey: rgba(0, 0, 0, 0.55);

    --color-grey-40: #f5f5f5;
    --color-grey-50: #eaeaea;
    --color-grey-60: #dadada;

    --color-icon-grey: rgba(0, 0, 0, 0.42);

    --color-tooltip-dark: #222222;

    --color-alert: #eb0000;

    --font-size-tiny: 12px;
    --font-size-small: 14px;
    --font-size-normal: 16px;
    --font-size-medium: 20px;

    --font-weight-normal: 400;
    --font-weight-bold: 700;

    --radius-small: 3px;
    --radius-normal: 6px;

    --shadow-normal: 0 0 1px rgba(0, 0, 0, 0.2), 0 0 8px rgba(0, 0, 0, 0.15);

    --padding-screen: 8px;

    --width-detail: 100vw;
    --width-button-small: 24px;
    --width-button-normal: 32px;
    --width-button-large: 40px;
}

@media (min-width: 576px) {
    :root {
        --width-detail: 300px;
        --padding-screen: 16px;
    }
}

@media (min-width: 768px) {
    :root {
        --width-detail: 350px;
    }
}

@media (min-width: 1200px) {
    :root {
        --width-detail: 400px;
        --padding-screen: 20px;
    }
}

@import url('https://fonts.googleapis.com/css2?family=PT+Sans:wght@400;700&display=swap');

html {
    font-family: 'PT Sans', sans-serif;
    letter-spacing: -0.005em;
    font-size: var(--font-size-normal);
    font-weight: var(--font-weight-normal);
}

*,
*:after,
*:before {
    box-sizing: border-box;
}

/* Remove outline from all focused elements */
*:focus {
    outline: none;
    outline-offset: -2px;
}

/* Remove highlight color on Android */
* {
    -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
}

html.keyboard-user *:focus {
    outline: 2px solid var(--color-primary);
}

input,
button {
    margin: 0;
    padding: 0;
    border: none;
    color: inherit;
    background: transparent;
    font: inherit;
    letter-spacing: inherit;
    text-align: left;
}

input::placeholder {
    color: var(--color-text-grey);
}

button:not([disabled]) {
    cursor: pointer;
}

ul {
    margin: 0;
    padding: 0;
    list-style-type: none;
}

svg {
    flex-shrink: 0;
}
</style>

<style scoped>
.app {
    display: flex;
    flex-direction: column;
}
</style>
