<template>
    <div class="container">
        <div class="left-items">
            <router-link to="/">
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    enable-background="new 0 0 24 24"
                    height="30px"
                    viewBox="0 0 24 24"
                    width="30px"
                    fill="#000000"
                >
                    <g><rect fill="none" height="24" width="24" /></g>
                    <g>
                        <g>
                            <path
                                d="M3,5v14c0,1.1,0.89,2,2,2h6V3H5C3.89,3,3,3.9,3,5z M9,19H5V5h4V19z"
                            />
                            <path d="M19,3h-6v8h8V5C21,3.9,20.1,3,19,3z M19,9h-4V5h4V9z" />
                            <path d="M13,21h6c1.1,0,2-0.9,2-2v-6h-8V21z M15,15h4v4h-4V15z" />
                        </g>
                    </g>
                </svg>
            </router-link>
            <svg
                v-if="this.$route.path !== '/'"
                xmlns="http://www.w3.org/2000/svg"
                height="24px"
                viewBox="0 0 24 24"
                width="24px"
                fill="#000000"
            >
                <path d="M0 0h24v24H0V0z" fill="none" />
                <path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6-6-6z" />
            </svg>
            <span class="title">{{ this.$route.meta.title }}</span>
        </div>
        <a href="/atlas/admin/logout/">
            <svg
                xmlns="http://www.w3.org/2000/svg"
                enable-background="new 0 0 24 24"
                height="24px"
                viewBox="0 0 24 24"
                width="24px"
                fill="#000000"
            >
                <g><path d="M0,0h24v24H0V0z" fill="none" /></g>
                <g>
                    <path
                        d="M17,8l-1.41,1.41L17.17,11H9v2h8.17l-1.58,1.58L17,16l4-4L17,8z M5,5h7V3H5C3.9,3,3,3.9,3,5v14c0,1.1,0.9,2,2,2h7v-2H5V5z"
                    />
                </g>
            </svg>
        </a>
    </div>
</template>

<script>
export default {
    name: 'Header',
}
</script>

<style scoped>
.container {
    display: flex;
    justify-content: space-between;
    border-bottom: 2px solid var(--color-grey-50);
    padding: 14px 32px;
}

.title {
    font-size: var(--font-size-medium);
    font-weight: var(--font-weight-bold);
}

.left-items {
    display: flex;
    align-items: center;
}
</style>
