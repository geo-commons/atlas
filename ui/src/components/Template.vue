<template>
    <Markdown :source="parsedSource" />
</template>

<script>
import ejs from 'ejs'
import Markdown from './Markdown'

export default {
    name: 'Template',
    components: {
        Markdown,
    },
    computed: {
        parsedSource() {
            try {
                return ejs.render(this.source, this.data)
            } catch (e) {
                return ''
            }
        },
    },
    props: {
        source: String,
        data: Object,
    },
}
</script>
