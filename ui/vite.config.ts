import { defineConfig } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
    plugins: [svelte(), tailwindcss()],
    base: '/app/',  // Important: Set base path
    build: {
        outDir: 'static',  // Build to ui/static folder
        emptyOutDir: true,
        rollupOptions: {
            output: {
                entryFileNames: 'assets/[name]-[hash].js',
                chunkFileNames: 'assets/[name]-[hash].js',
                assetFileNames: 'assets/[name]-[hash].[ext]'
            }
        }
    },
    server: {
        port: 5173,
        proxy: {
            '/api': 'http://localhost:8000',
            '/login': 'http://localhost:8000',
            '/register': 'http://localhost:8000',
            '/logout': 'http://localhost:8000',
            '/add-habit': 'http://localhost:8000',
            '/delete-habit': 'http://localhost:8000',
            '/check-habit': 'http://localhost:8000'
        }
    }
});