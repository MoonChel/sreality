import axios from "axios"

const apiClient = axios.create({
    baseURL: process.env.GRIDSOME_PROJECT_BACKEND_DOMAIN,
    withCredentials: true
})

function showNotification(notify) {
    apiClient.interceptors.response.use(
        function (response) {
            notify({ type: 'success', text: "Successfully completed" })
            return response
        },
        function (error) {
            if (!error.response) {
                notify({ type: 'error', text: 'Network error, try again later' })
                return Promise.reject(error);
            }

            if (error.code === 'ECONNABORTED') {
                notify({ type: 'error', text: 'Timeout error, try again later' })
                return Promise.reject(error);
            }

            switch (error.response.status) {
                case 404:
                    notify({ type: 'error', text: error.response.data.message })
                    break;
                case 401:
                    notify({ type: 'error', text: error.response.data.message })
                    break;
                case 400:
                    notify({ type: 'error', text: error.response.data.detail })
                    break;
                default:
                    notify({ type: 'error', text: "Oh, There is an issue" })
                    break;
            }

            return Promise.reject(error);
        }
    )
}

export {
    apiClient, showNotification
}