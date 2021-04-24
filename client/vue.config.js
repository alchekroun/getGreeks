if (process.env.NODE_ENV === 'production') {
  module.exports = {
    outputDir: 'dist',
    assetsDir: 'static',
    publicPath: '',

    transpileDependencies: [
      'vuetify',
    ],
  };
}
