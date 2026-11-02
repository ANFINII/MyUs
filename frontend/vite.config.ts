import { fileURLToPath } from 'node:url'
import babel from '@rolldown/plugin-babel'
import react, { reactCompilerPreset } from '@vitejs/plugin-react'
import { Plugin } from 'vite'
import { defineConfig } from 'vitest/config'

const src = (dir: string): string => fileURLToPath(new URL(`./src/${dir}`, import.meta.url))

const appVersion = Date.now().toString(36)

const versionFile = (): Plugin => ({
  name: 'version-file',
  apply: 'build',
  generateBundle() {
    this.emitFile({ type: 'asset', fileName: 'version.json', source: JSON.stringify({ version: appVersion }) })
  },
})

export default defineConfig({
  plugins: [react(), babel({ presets: [reactCompilerPreset()] }), versionFile()],
  define: {
    'import.meta.env.VITE_APP_VERSION': JSON.stringify(appVersion),
  },
  resolve: {
    alias: {
      api: src('api'),
      components: src('components'),
      lib: src('lib'),
      styles: src('styles'),
      types: src('types'),
      utils: src('utils'),
    },
  },
  server: {
    host: '127.0.0.1',
    port: 3000,
    strictPort: true,
  },
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./vitest.setup.ts'],
  },
})
