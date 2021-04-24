<template>
  <v-main>
    <v-container>
      <v-row>
        <h3>Graphs</h3>
      </v-row>
      <v-row>
        <v-col class="d-flex" cols="12" sm="12">
          <v-subheader class="p1-0">
            Stock price range
          </v-subheader>
          <v-range-slider v-model="ranges.rangeStock.range"
                          :min="ranges.rangeStock.min"
                          :max="ranges.rangeStock.max"
                          hide-details class="align-center">
            <template v-slot:prepend>
              <v-text-field
                :value="ranges.rangeStock.range[0]"
                class="mt-0 pt-0"
                hide-details
                single-line
                type="number"
                style="width: 60px"
                @change="$set(ranges.rangeStock.range, 0, $event)"
              ></v-text-field>
            </template>
            <template v-slot:append>
              <v-text-field
                :value="ranges.rangeStock.range[1]"
                class="mt-0 pt-0"
                hide-details
                single-line
                type="number"
                style="width: 60px"
                @change="$set(ranges.rangeStock.range, 1, $event)"
              ></v-text-field>
            </template>
          </v-range-slider>
        </v-col>
        <v-col class="d-flex" cols="12" sm="12">
          <v-subheader class="p1-0">
            Strike
          </v-subheader>
          <v-slider
            v-model="ranges.rangeStrike.slider"
            class="align-center"
            :max="ranges.rangeStrike.max"
            :min="ranges.rangeStrike.min"
            hide-details
          >
            <template v-slot:append>
              <v-text-field
                v-model="ranges.rangeStrike.slider"
                class="mt-0 pt-0"
                hide-details
                single-line
                type="number"
                style="width: 60px;">
              </v-text-field>
            </template>
          </v-slider>
        </v-col>
        <v-col class="d-flex" cols="12" sm="12">
          <v-subheader class="p1-0">
            Rate
          </v-subheader>
          <v-slider
            v-model="ranges.rangeRate.slider"
            class="align-center"
            :max="ranges.rangeRate.max"
            :min="ranges.rangeRate.min"
            hide-details
            step="0.05"
          >
            <template v-slot:append>
              <v-text-field
                v-model="ranges.rangeRate.slider"
                class="mt-0 pt-0"
                hide-details
                single-line
                type="number"
                style="width: 60px;">
              </v-text-field>
            </template>
          </v-slider>
        </v-col>
        <v-col class="d-flex" cols="12" sm="12">
          <v-subheader class="p1-0">
            Drift
          </v-subheader>
          <v-slider
            v-model="ranges.rangeDrift.slider"
            class="align-center"
            :max="ranges.rangeDrift.max"
            :min="ranges.rangeDrift.min"
            hide-details
            step="0.05"
          >
            <template v-slot:append>
              <v-text-field
                v-model="ranges.rangeDrift.slider"
                class="mt-0 pt-0"
                hide-details
                single-line
                type="number"
                style="width: 60px;">
              </v-text-field>
            </template>
          </v-slider>
        </v-col>
        <v-col class="d-flex" cols="12" sm="12">
          <v-subheader class="p1-0">
            Expiration
          </v-subheader>
          <v-slider
            v-model="ranges.rangeExpiration.slider"
            class="align-center"
            :max="ranges.rangeExpiration.max"
            :min="ranges.rangeExpiration.min"
            hide-details
          >
            <template v-slot:append>
              <v-text-field
                v-model="ranges.rangeExpiration.slider"
                class="mt-0 pt-0"
                hide-details
                single-line
                type="number"
                style="width: 60px;">
              </v-text-field>
            </template>
          </v-slider>
        </v-col>
      </v-row>
    </v-container>
    <v-container>
      <v-card>
        <v-tabs
          v-model="tab"
          background-color="transparent"
          centered
          dark
          grow
        >
          <v-tabs-slider></v-tabs-slider>
          <v-tab>
            Delta
          </v-tab>
          <v-tab>
            Theta
          </v-tab>
          <v-tab>
            Gamma
          </v-tab>
          <v-tab>
            Vega
          </v-tab>
          <v-tab>
            Rho
          </v-tab>
        </v-tabs>
        <v-card flat>
          <Graph :tab="tab" :ranges="ranges"/>
        </v-card>
      </v-card>
    </v-container>
  </v-main>
</template>

<script>
import Graph from '@/components/Graph.vue';

export default {
  name: 'RangeSelect',
  components: {
    Graph,
  },
  data() {
    return {
      series: [],
      ranges: {
        rangeStock: {
          min: 1,
          max: 100,
          range: [20, 80],
        },
        rangeStrike: {
          min: 1,
          max: 100,
          slider: 50,
        },
        rangeRate: {
          min: 0.1,
          max: 1,
          slider: 0.5,
        },
        rangeDrift: {
          min: 0.1,
          max: 1,
          slider: 0.5,
        },
        rangeExpiration: {
          min: 1,
          max: 365,
          slider: 30,
        },
      },
      tab: null,
    };
  },
};
</script>
