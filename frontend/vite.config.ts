import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  base: "./",
  plugins: [react()],
  server: {
    host: "0.0.0.0",
    port: 5173,
    allowedHosts: [
      "1034ac32b8b292157750666977a46ece.app.az.nuvolos.cloud",
    ],
    proxy: {
      "/api": {
        target: "http://nv-service-9f8921efeca6d41f4cda2558a6b29bed:8500",
        changeOrigin: true,
      },
    },
  },
  preview: {
    host: "0.0.0.0",
    port: 5173,
    allowedHosts: [
      "1034ac32b8b292157750666977a46ece.app.az.nuvolos.cloud",
    ],
    proxy: {
      "/api": {
        target: "http://nv-service-9f8921efeca6d41f4cda2558a6b29bed:8500",
        changeOrigin: true,
      },
    },
  },
});