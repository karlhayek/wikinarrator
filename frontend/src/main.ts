import { createApp } from 'vue'

// import { BootstrapVue } from 'bootstrap-vue'
import BootstrapVue3 from 'bootstrap-vue-3'

// Optional, since every component import their Bootstrap funcionality
// the following line is not necessary
// import 'bootstrap'

// import "bootstrap/dist/css/bootstrap.min.css"
// import "bootstrap"
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue-3/dist/bootstrap-vue-3.css'


import App from './App.vue'

const app = createApp(App)
app.use(BootstrapVue3)
app.mount('#app')