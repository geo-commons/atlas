<template>
    <Markdown :source="parsedSource" />
</template>

<script>
import nunjucks from 'nunjucks'
import Markdown from './Markdown'

nunjucks.configure({ autoescaping: true })

export default {
    name: 'Template',
    components: {
        Markdown,
    },
    computed: {
        parsedSource() {
            try {
                return nunjucks.renderString(this.source, this.data)
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
