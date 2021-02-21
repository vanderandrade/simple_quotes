import Vue from 'vue'
import App from './App.vue'
import router from './router'
import Toast from 'vue-easy-toast'
import Autocomplete from 'v-autocomplete'
import 'v-autocomplete/dist/v-autocomplete.css'


Vue.config.productionTip = false
Vue.use(Toast);
Vue.use(Autocomplete)

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
