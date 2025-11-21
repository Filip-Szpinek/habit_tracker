import svelte from 'rollup-plugin-svelte';
import resolve from '@rollup/plugin-node-resolve';
import commonjs from '@rollup/plugin-commonjs';
import typescript from '@rollup/plugin-typescript';
import sveltePreprocess from 'svelte-preprocess';


export default {
    input: 'src/main.ts',
    output: {
        file: '../built/static/bundle.js',
        format: 'iife',
        name: 'app',
        sourcemap: true
    },
    plugins: [
        svelte({ preprocess: sveltePreprocess(), compilerOptions: { dev: true } }),
        resolve({ browser: true }),
        commonjs(),
        typescript()
    ],
    watch: {
        clearScreen: false
    }
};