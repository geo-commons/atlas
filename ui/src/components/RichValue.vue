<template>
    <div>
        <span v-if="this.valueType === 'NUMBER'">{{ dataValue }}</span>
        <span v-if="this.valueType === 'UNKNOWN'">{{ dataValue }}</span>
        <markdown v-if="this.valueType === 'STRING'" :source="dataValue" />
        <a v-if="this.valueType === 'URL'" :href="dataValue" target="_blank" rel="noopener">{{
            dataValue.length >= 75
                ? `${dataValue.substring(0, 36)}...${dataValue.substring(dataValue.length - 36)}`
                : dataValue
        }}</a>
        <a v-if="this.valueType === 'IMAGE'" :href="dataValue" target="_blank" rel="noopener">
            <img
                :src="dataValue"
                :alt="`Afbeelding ${dataKey}`"
                v-bind:style="{ maxWidth: '100%' }"
            />
        </a>
    </div>
</template>

<script>
import Markdown from './Markdown'

const imageRegex = /^(http|https).*(\.jpg|\.jpeg|\.png|\.gif)/
const urlRegex = /^(http|https)/

export default {
    name: 'RichValue',
    components: {
        Markdown,
    },
    computed: {
        valueType() {
            if (this.dataValue === null) {
                return 'NULL'
            }

            if (typeof this.dataValue === 'number') {
                return 'NUMBER'
            }

            if (typeof this.dataValue !== 'string') {
                return 'UNKNOWN'
            }

            if (this.dataValue.match(imageRegex)) {
                return 'IMAGE'
            }

            if (this.dataValue.match(urlRegex)) {
                return 'URL'
            }

            return 'STRING'
        },
    },
    props: {
        dataKey: String,
        dataValue: [String, Number],
    },
}
</script>
