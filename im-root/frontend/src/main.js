import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import AutoComplete from "@/components/AutoComplete";
import VueHtmlToPaper from "vue-html-to-paper";

const base_url = window.location.origin;

const options = {
  name: "_blank",
  specs: ["fullscreen=yes", "titlebar=yes", "scrollbars=yes"],
  styles: [
    "https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css",
    "https://unpkg.com/kidlat-css/css/kidlat.css",
    // window.location.origin + "/styles/Sale.css"
    base_url + "/static/dist/styles/Sale.css",
    base_url + "/styles/Sale.css",
  ],
  timeout: 1000, // default timeout before the print window appears
  autoClose: true, // if false, the window will not close after printing
  windowTitle: window.document.title, // override the window title
};

const app = createApp(App);
app.component("AutoComplete", AutoComplete);
app.use(VueHtmlToPaper, options);
app.use(router).mount("#app");

// For V3 html-to-paper
// Link: https://stackoverflow.com/questions/66049945/vue-html-to-paper-with-vue3
// It uses Vue.prototype so it won't work with Vue 3 unless that's fixed. You could fork the repo if you wanted to fix it yourself.
//
// To do so, replace this ❌:
//
// install (Vue, options = {}) {
//     Vue.prototype.$htmlToPaper = (el, localOptions, cb = () => true) => {
// with this ✅ which will work for both Vue 2 and Vue 3:
//
// install (_i, options = {}) {
//     let globals = _i.prototype || _i.config.globalProperties;
//     globals.$htmlToPaper = (el, localOptions, cb = () => true) => {
// When installing the plugin with Vue 3, follow the docs but replace Vue.use with app.use.
