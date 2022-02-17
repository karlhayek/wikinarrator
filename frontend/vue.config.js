// vue.config.js
module.exports = {
    // Reverse proxy to access the backend during development (without Docker)
    devServer: {
        proxy: {
            "/api/*": {
                target: "http://localhost:8000",
                secure: false,
                changeOrigin: true,
            }
        },
        // reduce output logs when building dev server
        progress: false,
    },
    pages: {
        index: {
            entry: 'src/main.js',
            title: process.env.VUE_APP_NAME
        }
    }
};