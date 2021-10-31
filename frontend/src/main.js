// This is the main.js file. Import global CSS and scripts here.
// The Client API can be used here. Learn more: gridsome.org/docs/client-api

import axios from "axios"

import 'chota'

import DefaultLayout from '~/layouts/Default.vue'

import { Chart, registerables } from 'chart.js';

import Notifications from 'vue-notification/dist/ssr.js'

import { apiClient, showNotification } from './api'

Chart.register(...registerables);

export default function (Vue, { router, head, isClient }) {
  // Set default layout as a global component
  Vue.component('Layout', DefaultLayout)

  Vue.prototype.$api = apiClient

  // notifications
  Vue.use(Notifications)

  // connect notifications with apiClient
  showNotification(Vue.prototype.$notify)
}
