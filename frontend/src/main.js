// This is the main.js file. Import global CSS and scripts here.
// The Client API can be used here. Learn more: gridsome.org/docs/client-api

import axios from "axios"

import 'chota'

import DefaultLayout from '~/layouts/Default.vue'

import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

const apiClient = axios.create({
  baseURL: process.env.GRIDSOME_PROJECT_BACKEND_DOMAIN,
  withCredentials: true
})


export default function (Vue, { router, head, isClient }) {
  // Set default layout as a global component
  Vue.component('Layout', DefaultLayout)

  Vue.prototype.$api = apiClient
}
