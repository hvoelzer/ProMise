import {createRouter,createWebHistory} from "vue-router"

import GraphView from "./components/GraphView.vue"
import FilterView from "./components/FilterView.vue"

const menu_fields = [
    {
        path: "/",
        component: GraphView,
        name: "GraphView"
    },

    {
        path: "/filter",
        component: FilterView,
        name: "FilterView"
    }
]

const menu = createRouter({

    history: createWebHistory(),
    menu_fields
}
)

export default menu