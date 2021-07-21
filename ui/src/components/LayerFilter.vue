<template>
    <div>
        <div v-if="filter.kind == 'ATTRIBUTE'">
            <b>{{ filter.title }}</b>
            <div v-for="(option, index) in filter.values" v-bind:key="index">
                <input
                    type="checkbox"
                    :name="`filter-${filter.field}`"
                    :id="`filter-${filter.field}-${option}`"
                    v-model="selected[index]"
                />
                <label :for="`filter-${filter.field}-${option}`">
                    {{ option }}
                </label>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'LayerFilter',
    props: {
        layer: Object,
        filter: Object,
    },
    data() {
        return {
            selected: [],
        }
    },
    watch: {
        selected(selectedValue) {
            const filterValues = this.filter.values.filter((_, i) => selectedValue[i])
            this.$store.commit('setAppliedFilter', [
                this.layer.id,
                {
                    ...this.layer.appliedFilter,
                    [this.filter.field]: filterValues,
                },
            ])
        },
    },
}
</script>
