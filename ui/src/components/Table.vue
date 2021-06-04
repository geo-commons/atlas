<template>
    <div class="table-wrapper">
        <slot></slot>
    </div>
</template>

<script>
export default {
    name: 'Table',
}
</script>

<style scoped>
.table-wrapper {
    overflow: auto;
    word-wrap: break-word;
}

.table-wrapper table {
    width: 100%;
    font-size: var(--font-size-small);
    border-collapse: collapse;
}

.table-wrapper thead tr {
    background: var(--color-grey-40);
}

.table-wrapper th {
    font-weight: var(--font-weight-normal);
    color: var(--color-text-grey);
    text-align: left;
    padding-top: 7px !important;
    padding-bottom: 7px !important;
}

.table-wrapper th,
.table-wrapper td {
    padding: 4px;
    vertical-align: top;
}

.table-wrapper th:first-child,
.table-wrapper td:first-child {
    padding-left: 20px;
}

.table-wrapper th:last-child,
.table-wrapper td:last-child {
    padding-right: 20px;
}
</style>
