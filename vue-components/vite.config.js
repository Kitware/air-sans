export default {
  base: "./",
  build: {
    lib: {
      entry: "./src/main.js",
      name: "air_sans",
      formats: ["umd"],
      fileName: "air_sans",
    },
    rollupOptions: {
      external: ["vue"],
      output: {
        globals: {
          vue: "Vue",
        },
      },
    },
    outDir: "../air_sans/module/serve",
    assetsDir: ".",
  },
};
