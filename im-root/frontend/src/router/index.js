import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import Sale from "../views/Sale";
import Purchase from "../views/Purchase";
import Invoice from "../views/Invoice";
import WarehouseTransfer from "../views/WarehouseTransfer";
import Payment from "../views/Payment";

const routes = [
  {
    path: "/",
    name: "home",
    component: Home,
  },
  {
    path: "/sales/",
    name: "sales",
    component: Sale,
  },
  {
    path: "/purchase/",
    name: "purchase",
    component: Purchase,
  },
  {
    name: "invoice",
    component: Invoice,
    path: "/invoice/",
    props: (route) => ({
      invoice: route.params.invoice,
    }),
  },
  {
    name: "warehouseTransfer",
    component: WarehouseTransfer,
    path: "/warehouse-transfer/",
  },
  {
    name: "payment",
    component: Payment,
    path: "/payment/",
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
