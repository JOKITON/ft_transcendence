const { defineConfig } = require("@vue/cli-service");

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: "http://autentication:3001",
  },
  configureWebpack: {
    resolve: {
      alias: {
        vue$: "vue/dist/vue.esm-bundler.js",
      },
      extensions: ["*", ".js", ".vue", ".json"],
    },
  },
});
