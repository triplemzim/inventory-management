/* eslint-disable */
<template>
  <div class="container">
    <div class="row">
      <div class="col">
        <AutoComplete :data="customerList" :title="`Customer`" v-on:selectedData="handleSelectCustomer"/>
      </div>
      <div class="col">
        Column
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import AutoComplete from "@/components/AutoComplete";
import {onMounted, ref} from "vue";
import { getCustomerList, getProductList, getStockListWithBarcode } from "@/common/apis";

export default {
  name: "Home",
  components: {
    AutoComplete
  },
  setup() {
    const customerList = ref([]);
    const selectedCustomer = ref('');
    const componentName = ':home:';

    onMounted(async () => {
      const returnData = [];
      // Customer list
      let response = await getCustomerList();
      console.log(componentName, 'api-customer-list', response.data);
      response.data.forEach(customer => {
        const temp = {};
        temp.value = customer.name;
        temp.id = customer.id;
        returnData.push(temp);
      });
      customerList.value = returnData;

      //Product-List
      response = await getProductList();
      let productList = response.data;
      console.log(componentName, 'api-product-list', productList);

      console.log(await getStockListWithBarcode('123'));
    });

    return {
      customerList,
      selectedCustomer,
      componentName,
    }
  },
  methods: {
    handleSelectCustomer: function (event) {
      console.log(this.componentName, 'from home: ', event);
    }
  }
};
</script>
