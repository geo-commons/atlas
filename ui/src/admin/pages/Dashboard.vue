<template>
    <div>
        <div class="buttons">
            <router-link to="/maps"><LargeButton>Kaarten</LargeButton></router-link>
            <router-link to="/sources"><LargeButton>Bronnen</LargeButton></router-link>
            <router-link to="/users"><LargeButton>Gebruikers</LargeButton></router-link>
        </div>
    </div>
</template>

<script>
import LargeButton from '../components/LargeButton.vue'

export default {
    name: 'Dashboard',
    components: {
        LargeButton,
    },
}
</script>

<style scoped>
.buttons {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    row-gap: 14px;
    column-gap: 14px;
}
</style>
