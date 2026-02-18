import { defineConfig } from "vite";
// import react from "@vitejs/plugin-react-swc";
import path from "path";
import react from "@vitejs/plugin-react";


// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    port: 5174,
    watch: {
      usePolling: true,
      interval: 300,
    },
    hmr: {
      protocol: "ws",
      host: "localhost",
      port: 5174,
    },
    proxy: {
      "/api": {
        target: "http://0.0.0.0:8001",
        changeOrigin: true,
      },
    },
  },
});
