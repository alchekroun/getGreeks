import Vue from 'vue';
import VueApexCharts from 'vue-apexcharts';
import App from './App.vue';
import router from './router';
import 'bootstrap/dist/css/bootstrap.css';
import vuetify from './plugins/vuetify';

Vue.config.productionTip = false;

Vue.component('apexchart', VueApexCharts);

new Vue({
  router,
  vuetify,
  render: (h) => h(App),
}).$mount('#app');
