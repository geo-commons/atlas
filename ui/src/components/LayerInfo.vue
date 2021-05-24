<template>
    <tippy arrow placement="right-start" theme="light-border" trigger="click" :delay="[0, 0]">
        <template v-slot:trigger>
            <button class="button" aria-label="Toon meer informatie">
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    height="18px"
                    viewBox="0 0 24 24"
                    width="18px"
                    fill="#000000"
                >
                    <path d="M0 0h24v24H0V0z" fill="none" />
                    <path
                        d="M11 7h2v2h-2zm0 4h2v6h-2zm1-9C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z"
                    />
                </svg>
            </button>
        </template>
        <div class="container">
            <div class="heading">
                <h3 class="title">{{ layer.title }}</h3>
                <span class="description">{{ layer.metadata.description }}</span>
            </div>
            <Table class="table">
                <table>
                    <tbody>
                        <tr>
                            <td>Beheerder</td>
                            <td class="value">{{ layer.metadata.organization }}</td>
                        </tr>
                        <tr>
                            <td>Bijgewerkt</td>
                            <td class="value">{{ layer.metadata.updated }}</td>
                        </tr>
                    </tbody>
                </table>
            </Table>
        </div>
    </tippy>
</template>

<script>
import Table from './Table'

export default {
    name: 'LayerInfo',
    components: {
        Table,
    },
    props: {
        layer: Object,
    },
}
</script>

<style scoped>
.button {
    color: var(--color-primary);
    width: 24px;
    height: 24px;
    border-radius: 50%;
}

.container {
    max-width: 300px;
    font-weight: normal;
    text-align: left;
}

.heading {
    text-align: center;
    border-bottom: 1px solid var(--color-grey-50);
    padding-bottom: 12px;
}

.title {
    margin-bottom: 4px;
    font-weight: bold;
    font-size: 16px;
}

.table {
    margin: 5px;
}

.value {
    text-align: right;
}
</style>
