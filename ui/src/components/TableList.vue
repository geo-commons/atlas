<template>
  <div class="table-wrapper">
    <slot></slot>
  </div>
</template>

<script>
export default {
  name: "TableList",
};
</script>

<style scoped>
.table-wrapper {
  overflow: auto;
  word-wrap: break-word;
}

.table-wrapper table {
  width: 100%;
  font-size: var(--font-size-normal);
  border-collapse: collapse;
}

.table-wrapper thead tr {
  background: var(--color-grey-50);
}

.table-wrapper thead tr th {
  font-weight: var(--font-weight-normal);
  text-align: left;
  padding: 12px 4px;
}

.table-wrapper th,
.table-wrapper td {
  padding: 8px 4px;
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
