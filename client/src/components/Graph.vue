<template>
  <v-container>
    <div id="chart">
      <apexchart type="line" height="350" :options="chartOptions" :series="series">
      </apexchart>
    </div>
  </v-container>
</template>

<script>
import VueApexCharts from 'vue-apexcharts';
import axios from 'axios';

export default {
  name: 'Graph',
  components: {
    apexchart: VueApexCharts,
  },
  props: {
    tab: {
      required: true,
      type: Number,
    },
    ranges: {
      required: true,
      type: Object,
    },
  },
  data() {
    return {
      type: null,
      series: [],
      chartOptions: {
        tooltip: {
          enabled: true,
          theme: 'dark',
        },
        chart: {
          height: 350,
          type: 'line',
          zoom: {
            enabled: true,
          },
        },
        dataLabels: {
          enabled: false,
        },
        noData: {
          text: 'Loading...',
        },
        yaxis: {
          tickAmount: 5,
        },
        xaxis: {
          type: 'numeric',
          labels: {
            show: true,
          },
          axisTicks: {
            show: true,
          },
          axisBorder: {
            show: true,
          },
          cosshairs: {
            show: true,
          },
        },
      },
    };
  },
  watch: {
    tab: {
      immediate: true,
      handler() {
        // eslint-disable-next-line default-case
        switch (this.tab) {
          case 0:
            this.type = 'delta';
            break;
          case 1:
            this.type = 'theta';
            break;
          case 2:
            this.type = 'gamma';
            break;
          case 3:
            this.type = 'vega';
            break;
          case 4:
            this.type = 'rho';
            break;
        }
        this.calculate();
      },
    },
    ranges: {
      immediate: true,
      deep: true,
      handler() {
        this.calculate();
      },
    },
  },
  methods: {
    async calculate() {
      const spotB = this.ranges.rangeStock.range[0];
      const spotE = this.ranges.rangeStock.range[1];
      const strike = this.ranges.rangeStrike.slider;
      const drift = this.ranges.rangeDrift.slider;
      const rate = this.ranges.rangeRate.slider;
      const expiration = this.ranges.rangeExpiration.slider;
      const { type } = this;
      if (spotB && spotE && strike && drift && rate && expiration && type) {
        const path = `http://localhost:5000/api/calc/${type}/${spotB}/${spotE}/${strike}/${drift}/${rate}/${expiration}/`;
        axios.get(path).then((res) => {
          this.series = [{
            name: 'call',
            data: res.data.call,
          }, {
            name: 'put',
            data: res.data.put,
          }];
        }).catch((error) => {
          console.error(error);
        });
      }
    },
  },
};

</script>
