import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import AutoComplete from "@/components/AutoComplete";

const app = createApp(App)
app.component('AutoComplete', AutoComplete);
app.use(router).mount("#app");
