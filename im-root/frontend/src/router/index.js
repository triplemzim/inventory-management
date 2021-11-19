import {createRouter, createWebHistory} from "vue-router";
import Home from "../views/Home.vue";
import Sale from "../views/Sale";
import Purchase from "../views/Purchase";


const routes = [
    {
        path: "/",
        name: "home",
        component: Home,
    },
    {
        path:"/sales/",
        name: "sales",
        component: Sale,
    },
    {
        path:"/purchase/",
        name: "purchase",
        component: Purchase,
    },
    // {
    //   path: "/about",
    //   name: "About",
    //   // route level code-splitting
    //   // this generates a separate chunk (about.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () =>
    //     import(/* webpackChunkName: "about" */ "../views/About.vue"),
    // },
];

const router = createRouter({
    history: createWebHistory("/"),
    routes,
});

export default router;
