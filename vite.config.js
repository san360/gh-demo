import { defineConfig } from 'vite';

export default defineConfig({
  root: 'src/frontend',
  server: {
    port: 3000,
    host: true,
    open: true
  },
  build: {
    outDir: '../../dist',
    emptyOutDir: true
  },
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./test/setup.js']
  }
});
