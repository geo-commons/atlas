<template>
    <tippy
        placement="bottom-end"
        theme="popover"
        trigger="click"
        :distance="1"
        :delay="[0, 0]"
        :a11y="false"
        :animateFill="false"
        :touch="true"
        :touchHold="false"
    >
        <template v-slot:trigger>
            <button
                class="iconbutton"
                v-tippy="{ placement: 'bottom' }"
                content="opties"
                aria-label="Toon meer opties"
            >
                <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24">
                    <path d="M0 0h24v24H0V0z" fill="none" />
                    <path
                        d="M12 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"
                    />
                </svg>
            </button>
        </template>
        <ul class="list">
            <li v-if="!user">
                <a :href="`/atlas/login?next=${encodeURIComponent(this.nextUrl)}`">Log in</a>
            </li>
            <li v-if="user">
                <a :href="`/atlas/logout?next=${encodeURIComponent(this.nextUrl)}`">Log uit</a>
            </li>
            <li><a href="/atlas/help" target="_blank">Help</a></li>
            <li><button @click="() => toggleModal('embed')">Embed</button></li>
        </ul>
    </tippy>
</template>

<script>
export default {
    name: 'MorePanel',
    computed: {
        nextUrl() {
            return window.location.pathname
        },
    },
    methods: {
        toggleModal(modal) {
            this.$emit('toggle-modal', modal)
        },
    },
    props: {
        user: Object,
    },
}
</script>

<style scoped>
.wrapper {
    position: relative;
}

.iconbutton {
    width: var(--width-button-large);
    height: var(--width-button-large);
    background: white;
    border-radius: 50%;
    box-shadow: var(--shadow-normal);
}
</style>
