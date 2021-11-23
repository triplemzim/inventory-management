<template>
  <div id="nav">
    <NavbarComponent/>
  </div>
  <router-view :rootCustomerList="customerList" :rootSupplierList="supplierList" :rootProductList="productList"
               :rootWarehouseList="warehouseList"/>
</template>
<script>
import NavbarComponent from "@/components/Navbar";
import {getCustomerList, getProductList, getWarehouseList, getSupplierList} from '@/common/apis';

export default {
  name: "App",
  components: {
    NavbarComponent
  },
  data() {
    return {
      productList: [],
      customerList: [],
      supplierList: [],
      warehouseList: [],
    }
  },
  async created() {
    this.customerList = await getCustomerList();
    this.supplierList = await getSupplierList();
    this.productList = await getProductList();
    this.warehouseList = await getWarehouseList();
  }
}
</script>
<style>
body {
  font-family: "Noto Sans JP", sans-serif;
  font-weight: 400;
}
</style>
