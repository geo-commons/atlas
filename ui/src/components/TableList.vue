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
  word-wrap: break-word;
  overflow: auto;
  flex: 1 1 auto;
}

:slotted(.table-wrapper table) {
  width: 100%;
  font-size: var(--font-size-normal);
  border-collapse: collapse;
}

:slotted(.table-wrapper thead tr) {
  background: var(--color-grey-50);
}

:slotted(.table-wrapper thead tr th) {
  background: var(--color-grey-50);
  position: sticky;
  top: 0;
  font-weight: var(--font-weight-normal);
  text-align: left;
  padding: 12px 4px;
}

:slotted(.table-wrapper th),
:slotted(.table-wrapper td) {
  padding: 8px 4px;
  vertical-align: top;
}

:slotted(.table-wrapper th:first-child),
:slotted(.table-wrapper td:first-child) {
  padding-left: 20px;
}

:slotted(.table-wrapper th:last-child),
:slotted(.table-wrapper td:last-child) {
  padding-right: 20px;
}
</style>
