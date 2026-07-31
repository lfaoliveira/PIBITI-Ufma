import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { nodePolyfills } from 'vite-plugin-node-polyfills'
import tailwindcss from '@tailwindcss/vite'

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [vue(), nodePolyfills({ protocolImports: true, }), tailwindcss(),],
    server: {
        host: true,        // or '0.0.0.0'
        port: 5173,         // default or custom
        watch: {
            usePolling: true // improves HMR inside Docker
        }
    },

})
