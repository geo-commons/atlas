const BundleTracker = require('webpack-bundle-tracker')

const DEPLOYMENT_PATH = '/atlas/static/dist/'

module.exports = {
    publicPath: process.env.NODE_ENV === 'production' ? DEPLOYMENT_PATH : 'http://localhost:8081/',
    outputDir: '../homepage/static/dist',

    devServer: {
        port: 8081,
        public: 'localhost:8081',
        headers: {
            'Access-Control-Allow-Origin': '*',
        },
    },

    configureWebpack: {
        plugins: [new BundleTracker({ path: __dirname, filename: 'webpack-stats.json' })],
    },

    css: {
        sourceMap: true,
    },

    pages: {
        app: { entry: 'src/app.js' },
        embed: { entry: 'src/embed.js' },
    },
}
