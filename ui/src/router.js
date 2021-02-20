import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import NewQuote from "./views/NewQuote.vue"
import Autocomplete from 'v-autocomplete'
import 'v-autocomplete/dist/v-autocomplete.css'

Vue.use(Autocomplete)
Vue.use(Router)

export default new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [{
            path: '/',
            name: 'home',
            component: Home
        },
        {
            path: '/new',
            name: 'new-quote',
            component: NewQuote
        }

    ]
})