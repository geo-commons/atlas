<template>
    <div class="wrapper">
        <button @click="closeThemes">Sluiten</button>
        <ul>
            <li v-bind:key="theme.id" v-for="theme in themes">
                <button>
                    <img :src="theme.icon" />
                    {{ theme.title }}
                </button>
            </li>
        </ul>
    </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
    name: 'Themes',
    computed: mapState({
        themes: (state) => state.themes,
    }),
    methods: {
        closeThemes() {
            this.$emit('close-themes')
        },
    },
}
</script>

<style scoped>
.wrapper {
    position: fixed;
    z-index: 1;
    left: 0;
    top: 500;
    width: 100%;
    background: white;
    box-shadow: var(--shadow-normal);
    display: flex;
    flex-direction: column;
}
</style>
