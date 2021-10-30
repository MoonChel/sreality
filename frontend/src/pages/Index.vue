<template>
  <Layout>
    <div class="row">
      <div class="col text-center">
        <input
          v-model="url"
          type="text"
          name="url"
          style="width: 50%; display: inline-block; margin: 10px; padding: 9px"
          placeholder="URL from sreality search"
        />
        <button @click="search">Search</button>
      </div>
    </div>

    <template v-if="isLoading">
      <h1 class="text-center">Loading...</h1>
    </template>
    <template>
      <h1 class="text-center"></h1>
    </template>

    <template v-if="estates">
      <h2>{{ estates.title }}</h2>

      <div class="row">
        <div class="col">
          <canvas id="chart-price-vs-district" height="400"></canvas>
        </div>
      </div>

      <div class="row">
        <div class="col">
          <canvas id="chart-et_type-vs-price" height="400"></canvas>
        </div>
        <div class="col">
          <canvas id="chart-size-vs-price" height="400"></canvas>
        </div>
      </div>
    </template>
  </Layout>
</template>

<script>
import { Chart } from "chart.js";

const minPriceWindow = 1000000;
const maxPriceWindow = 1000000;
const minSizeWindow = 10;
const maxSizeWindow = 10;

export default {
  data() {
    return {
      url: "https://www.sreality.cz/hledani/prodej/byty/brno?pois_in_place_distance=2&pois_in_place=2&navic=balkon&velikost=3%2Bkk,2%2Bkk,2%2B1,3%2B1&vlastnictvi=osobni&stav=velmi-dobry-stav&patro-od=1&patro-do=10&plocha-od=20&plocha-do=100&cena-od=0&cena-do=6000000",
      estates: null,
      isLoading: false,
    };
  },

  methods: {
    async getData() {
      this.isLoading = true;
      const params = {
        url: this.url,
      };

      const response = await this.$api.get("/estates", { params: params });

      this.estates = response.data;

      this.isLoading = false;
    },
    initPriceVsDistrictChart() {
      new Chart("chart-price-vs-district", {
        type: "scatter",
        data: {
          datasets: [
            {
              label: "Price in CZK vs District",
              data: this.estates.estates,
              backgroundColor: "rgba(255, 99, 132, 0.5)",
            },
          ],
        },
        options: {
          // responsive: false,
          maintainAspectRatio: false,
          parsing: {
            xAxisKey: "locality.district",
            yAxisKey: "price",
          },
          scales: {
            x: {
              type: "category",
            },
            y: {
              min: this.estates.min_price - minPriceWindow,
              max: this.estates.max_price + maxPriceWindow,
            },
          },
        },
      });
    },
    initEtTypeVsPrice() {
      new Chart("chart-et_type-vs-price", {
        type: "scatter",
        data: {
          datasets: [
            {
              label: "Type vs Price",
              data: this.estates.estates,
              backgroundColor: "rgba(255, 99, 132, 0.5)",
            },
          ],
        },
        options: {
          // responsive: false,
          maintainAspectRatio: false,
          parsing: {
            xAxisKey: "et_type",
            yAxisKey: "price",
          },
          scales: {
            x: {
              type: "category",
            },
            y: {
              min: this.estates.min_price - minPriceWindow,
              max: this.estates.max_price + maxPriceWindow,
            },
          },
        },
      });
    },
    initSizeVsPriceChart() {
      new Chart("chart-size-vs-price", {
        type: "scatter",
        data: {
          datasets: [
            {
              label: "Size in M2 vs Price",
              data: this.estates.estates,
              backgroundColor: "rgba(255, 99, 132, 0.5)",
            },
          ],
        },
        options: {
          // responsive: false,
          maintainAspectRatio: false,
          parsing: {
            xAxisKey: "size",
            yAxisKey: "price",
          },
          scales: {
            x: {
              min: this.estates.min_size - minSizeWindow,
              max: this.estates.max_size + maxSizeWindow,
            },
            y: {
              min: this.estates.min_price - minPriceWindow,
              max: this.estates.max_price + maxPriceWindow,
            },
          },
        },
      });
    },
    async search() {
      await this.getData();
      if (process.isClient) {
        this.initSizeVsPriceChart();
        this.initEtTypeVsPrice();
        this.initPriceVsDistrictChart();
      }
    },
  },

  async mounted() {
    if (this.url) {
      await this.search();
    }
  },
};
</script>
