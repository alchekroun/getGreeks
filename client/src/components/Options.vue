<template>
  <v-main>
    <v-container>
      <v-row>
        <v-col>
          <h3> Values of an option</h3>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <h5>Inputs</h5>
            <v-select :items="types" label="Type of option"
                      item-text="value.name"
                      item-value="value.name"
                      v-model="typeSelect"
                      @input="verifType"
            >
            </v-select>
          <v-form v-model="isValid">
          <v-row align="center">
            <v-col class="d-flex" cols="12" sm="6">
              <v-text-field label="Spot" :rules="[rules.required, rules.gt0]"
                            hide-details="auto" id="spot" type="number">
              </v-text-field>
            </v-col>
            <v-col class="d-flex" cols="12" sm="6">
              <v-text-field label="Strike" :rules="[rules.required, rules.gt0]" type="number"
                            hide-details="auto" id="strike">
              </v-text-field>
            </v-col>
            <v-col class="d-flex" cols="12" sm="6">
              <v-text-field label="Drift" :rules="[rules.required, rules.gt0, rules.lte1]"
                            type="number"
                            hide-details="auto" id="drift">
              </v-text-field>
            </v-col>
            <v-col class="d-flex" cols="12" sm="6">
              <v-text-field label="Rate" :rules="[rules.required, rules.gt0, rules.lte1]"
                            type="number"
                            hide-details="auto" id="rate">
              </v-text-field>
            </v-col>
            <v-col class="d-flex" cols="12" sm="6">
              <v-text-field label="Expiration" :rules="[rules.required, rules.gt0]"
                            type="number"
                            hide-details="auto"
                            id="expiration">
              </v-text-field>
            </v-col>
            <v-col class="d-flex" cols="12" sm="6">
              <v-select :items="times" label="Unit"
                        item-text='value.name'
                        item-value='value.name'
                        v-model="timeSelect"
                        >
              </v-select>
            </v-col>
            <v-col class="d-flex" cols="12" sm="6">
              <v-text-field label="Dividend" :rules="[rules.required, rules.gt0]"
                            type="number"
                            hide-details="auto"
                            id="dividend" :disabled="isVanilla" value="1">
              </v-text-field>
            </v-col>
            <v-col class="d-flex" cols="12" sm="6">
              <v-btn :disabled="!isValid" class="ma-2"
                     outlined @click="calculateGreeks">Calculate</v-btn>
            </v-col>
          </v-row>
          </v-form>
        </v-col>
        <v-col>
          <h5>Result</h5>
          <v-data-iterator
            :items="pricingOption"
            :items-per-page="2"
            hide-default-footer
            >
            <template v-slot:default="items">
              <v-row>
                <v-col
                v-for="item in items.items"
                :key="item.name"
                cols="12"
                xs="6" sm="6" md="6" lg="6" xl="6">
                  <v-card>
                    <v-card-title>{{item.name}}</v-card-title>
                    <v-divider></v-divider>
                    <v-list dense>
                      <v-list-item>
                        <v-list-item-content>Price:</v-list-item-content>
                        <v-list-item-content class="align-end">{{item.price}}</v-list-item-content>
                      </v-list-item>
                      <v-list-item>
                        <v-list-item-content>Delta:</v-list-item-content>
                        <v-list-item-content class="align-end">{{item.delta}}</v-list-item-content>
                      </v-list-item>
                      <v-list-item>
                        <v-list-item-content>Theta:</v-list-item-content>
                        <v-list-item-content class="align-end">{{item.theta}}</v-list-item-content>
                      </v-list-item>
                      <v-list-item>
                        <v-list-item-content>Gamma:</v-list-item-content>
                        <v-list-item-content class="align-end">{{item.gamma}}</v-list-item-content>
                      </v-list-item>
                      <v-list-item>
                        <v-list-item-content>Vega:</v-list-item-content>
                        <v-list-item-content class="align-end">{{item.vega}}</v-list-item-content>
                      </v-list-item>
                      <v-list-item>
                        <v-list-item-content>Rho:</v-list-item-content>
                        <v-list-item-content class="align-end">{{item.rho}}</v-list-item-content>
                      </v-list-item>
                    </v-list>
                  </v-card>
                </v-col>
              </v-row>
            </template>
          </v-data-iterator>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Options',
  data() {
    return {
      isValid: false,
      rules: {
        required: (value) => !!value || 'Required.',
        gt0: (value) => value > 0 || 'Positive only',
        lte1: (value) => value <= 1 || 'Less than 1',
      },
      timeSelect: 'days',
      times: ['days', 'months', 'years'],
      typeSelect: 'vanilla',
      isVanilla: true,
      types: ['vanilla', 'dividend'],
      pricingOption: [
        {
          name: 'Call',
          price: 0,
          delta: 0,
          theta: 0,
          gamma: 0,
          vega: 0,
          rho: 0,
        },
        {
          name: 'Put',
          price: 0,
          delta: 0,
          theta: 0,
          gamma: 0,
          vega: 0,
          rho: 0,
        },
      ],
    };
  },
  methods: {
    async calculateGreeks() {
      const spot = document.getElementById('spot').value;
      const strike = document.getElementById('strike').value;
      const drift = document.getElementById('drift').value;
      const rate = document.getElementById('rate').value;
      const expiration = document.getElementById('expiration').value;
      const timeU = this.timeSelect;
      const type = this.typeSelect;
      let dividend;
      if (this.isVanilla) {
        dividend = -1;
      } else {
        dividend = document.getElementById('dividend').value;
      }
      if (spot && strike && drift && rate && expiration && timeU && type && dividend) {
        const path = `http://localhost:5000/api/calc/option/${type}/${spot}/${strike}/${drift}/${rate}/${expiration}/${timeU}/${dividend}/`;
        axios.get(path).then((res) => {
          this.pricingOption = res.data;
        }).catch((error) => {
          console.error(error);
        });
      }
    },
    verifType() {
      this.isVanilla = this.typeSelect === 'vanilla';
    },
  },
};
</script>

<style scoped>
</style>
