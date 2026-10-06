import { fileURLToPath } from 'node:url'
import babel from '@rolldown/plugin-babel'
import { tanstackRouter } from '@tanstack/router-plugin/vite'
import react, { reactCompilerPreset } from '@vitejs/plugin-react'
import { defineConfig } from 'vitest/config'

const src = (dir: string): string => fileURLToPath(new URL(`./src/${dir}`, import.meta.url))

export default defineConfig({
  plugins: [tanstackRouter({ target: 'react', autoCodeSplitting: true }), react(), babel({ presets: [reactCompilerPreset()] })],
  resolve: {
    alias: {
      api: src('api'),
      components: src('components'),
      lib: src('lib'),
      pages: src('pages'),
      styles: src('styles'),
      types: src('types'),
      utils: src('utils'),
    },
  },
  server: {
    host: '127.0.0.1',
    port: 3000,
  },
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./vitest.setup.ts'],
  },
})
