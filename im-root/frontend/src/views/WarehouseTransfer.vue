<script>
import {
  getWarehouseTransferList,
  getNextOrPrevList,
  getProductList,
  getWarehouseList,
  postTransfer, getStockListWithBarcode
} from "@/common/apis";
import {COMPANY_NAME} from "@/common/strings"

export default {
  props: ['rootProductList', 'rootWarehouseList'],
  data() {
    const today = new Date();

    return {
      warehouseTransfers: [],
      transferCount: 0,
      nextList: null,
      prevList: null,
      selectedProduct: null,
      quantity: 0,
      barcode: null,
      toWarehouse: null,
      fromWarehouse: null,
      dateSelected: today.getDate() + '/' + (today.getMonth() + 1) + '/' + today.getFullYear(),
      comment: null,
      productList: [],
      warehouseList: [],
      componentName: 'Warehouse Transfer ',
      productName: null,
      COMPANY_NAME,
      productTable: [],
      stockAmount: null,
    }
  },
  async mounted() {
    const jq = window.jQuery;
    //DatePicker
    jq("#warhouseDatepicker").datepicker();
    const wtResponse = await getWarehouseTransferList();
    this.warehouseTransfers = wtResponse.data;
    console.log(this.componentName, 'transfer-list', this.warehouseTransfers.results[0]);

    if (this.rootProductList.data == null) {
      const response = await getProductList();
      this.productList = response.data;
    } else {
      this.productList = this.rootProductList.data;
    }

    if (this.rootWarehouseList.data == null) {
      const response = await getWarehouseList();
      this.warehouseList = response.data;
    } else {
      this.warehouseList = this.rootWarehouseList.data;
    }
  },
  methods: {
    handleSelectProduct: function (event) {
      console.log(this.componentName, event.target.value);
      const selectedProduct = this.productList.find(x => x.product_name.name + ' - ' + x.category.name === event.target.value);
      // if(selectedProduct == null) {
      //   selectedProduct = this.rawProductList.find(x => x.barcode === event.target.value);
      // }
      if (selectedProduct == null) return;
      this.productName = selectedProduct.product_name.name + ' - ' + selectedProduct.category.name;
      this.barcode = selectedProduct.barcode;
      this.quantity = 1;
      this.handleStock(this.barcode);
    },
    handleSelectProductWithBarcode: function (event) {
      event.preventDefault();
      console.log(this.componentName, event.target.value);
      const selectedProduct = this.productList.find(x => x.barcode.toString() === event.target.value.toString());
      if (selectedProduct == null) return;
      this.productName = selectedProduct.product_name.name + ' - ' + selectedProduct.category.name;
      this.quantity = 1;
      this.handleStock(this.barcode);
    },
    handleStock: async function (barcode) {
      const stockList = await getStockListWithBarcode(barcode);
      console.log(stockList.data);
      this.stockAmount = stockList.data.find(x => x.warehouse === this.fromWarehouse).quantity;
    },
    addProduct: function () {
      const row = {};
      row.productName = this.productName;
      row.quantity = this.quantity;
      row.barcode = this.barcode;
      const idx = this.productTable.findIndex(x => x.productName === row.productName);
      if (idx !== -1) this.productTable.splice(idx, 1);
      if (row.quantity === 0) return;
      this.productTable.push(row);

      console.log('table', ...this.productTable);

      this.resetProduct();
    },
    resetProduct: function () {
      this.productName = '';
      this.quantity = 0;
      this.barcode = '';
      this.stockAmount = null;
    },
    submitTransfer: async function () {
      if (!confirm("Do you confirm to submit Sale?")) {
        return;
      }
      if (!this.isValidTransfer()) {
        return;
      }
      const requestBody = {};
      requestBody.warehouse_source = this.fromWarehouse;
      requestBody.warehouse_dest = this.toWarehouse;
      requestBody.date = this.dateSelected;
      requestBody.comment = this.comment;
      const requestProductList = [];
      this.productTable.forEach(x => {
        const oneProduct = {};
        oneProduct.product = x.barcode;
        oneProduct.quantity = x.quantity;
        requestProductList.push(oneProduct);
      });
      requestBody.product_list = requestProductList;

      console.log(this.componentName, 'transfer-payload: ', JSON.stringify(requestBody));
      const response = await postTransfer(requestBody);
      if (response.status === 201) {
        alert('Transfer Record Complete!');
        this.resetAll();
      }
    },
    resetAll: async function () {
      this.resetProduct();
      this.productTable = [];
      this.comment = '';
      const wtResponse = await getWarehouseTransferList();
      this.warehouseTransfers = wtResponse.data;
    },
    isValidTransfer: function () {
      if (this.productTable.length === 0) {
        alert('Please add some product');
        return false;
      }
      if (this.fromWarehouse === this.toWarehouse) {
        alert('Please add different warehouses');
        return false;
      }
      return true;
    },
    findNextOrPrev: async function (endpoint) {
      const response = await getNextOrPrevList(endpoint);
      this.warehouseTransfers = response.data;
    },
    setProductFromTable: function (row) {
      this.productName = row.productName;
      this.quantity = row.quantity;
      this.barcode = row.barcode;
    },
    getWarehouseNameFromId: function (id) {
      const warehouse = this.warehouseList.find(x => x.id === id);
      if (warehouse != null) {
        return warehouse.name;
      }
      return '';
    },
    deleteProduct: function () {
      const idx = this.productTable.findIndex(x => x.barcode === this.barcode);
      if (idx !== -1) this.productTable.splice(idx, 1);
      this.resetProduct()
    }
  }
}
</script>


<template>
  <div class="containerRoot" id="home">
    <h3 class="col-lg text-center mt-3" style="font-weight: bold">
      <span>Warehouse Transfer</span>
    </h3>
    <section class="supplier">
      <div class="container">
        <div class="row">
          <div class="col-lg-6">
            <div class="sticky-top">
              <form @submit.prevent="submitTransfer">

                <div class="product-information">

                  <div class="product-info-box">
                    <div class="card">
                      <div class="card-header">
                        <h5>Product</h5>
                      </div>
                      <div class="card-body">
                        <div class="form-group row">
                          <div class="col-lg-6">
                            <div class="form-group row">
                              <label for="productName" class="col-lg-4 col-form-label">Product Name</label>
                              <div class="col-lg-8">
                                <input class="form-control" list="datalistOptions2" id="productName"
                                       placeholder="Type to search..." v-on:input="handleSelectProduct($event)"
                                       v-bind:value="productName">
                                <datalist id="datalistOptions2">
                                  <option v-for="item in productList" :key="item.id"
                                          :value="item.product_name.name + ' - ' + item.category.name"/>
                                </datalist>
                              </div>
                            </div>
                          </div>
                          <div class="col-lg-6">
                            <div class="form-group row">
                              <label for="productBarcode" class="col-lg-4 col-form-label">Barcode</label>
                              <div class="col-lg-8">
                                <input @keydown.enter.prevent="handleSelectProductWithBarcode($event)" type="text"
                                       class="form-control" id="productBarcode" v-model="barcode">
                              </div>
                            </div>
                          </div>
                        </div>
                        <div class="row">
                          <div class="col-lg-6">
                            <div class="form-group row">
                              <label for="productQuantity" class="col-lg-4 col-form-label">Quantity</label>
                              <div class="col-lg-8">
                                <input type="number" class="form-control" id="productQuantity" v-model="quantity">
                              </div>
                            </div>
                          </div>
                          <div class="col-lg-6">
                            <div class="form-group row">
                              <label for="productStock" class="col-lg-4 col-form-label">In Stock</label>
                              <div class="col-lg-8">
                                <input type="number" readonly class="form-control" id="stockamount"
                                       v-model="stockAmount">
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                      <div class="card-footer">
                        <div class="product-button">
                          <button class="btn btn-danger mx-2" :disabled="barcode == null || barcode === ''"
                                  type="button"
                                  @click="deleteProduct()">Delete
                          </button>
                          <button class="btn btn-success" type="button" @click="addProduct()">Add / Update</button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="warehouse-information">
                  <div class="warehouse-info-box">
                    <div class="card">
                      <div class="card-header">
                        <h5>Warehouse</h5>
                      </div>
                      <div class="card-body">
                        <div class="form-group row">
                          <label class="col-lg-4 col-form-label">Source Warehouse</label>
                          <div class="col-lg-8">
                            <select class="form-select" v-model="fromWarehouse" required>
                              <!--                        <option selected value="4">Warhouse One</option>-->
                              <option v-for="whouse in warehouseList" :key="whouse.id" :value="whouse.id">{{
                                  whouse.name
                                }}
                              </option>
                            </select>
                          </div>
                        </div>
                        <div class="form-group row">
                          <label class="col-lg-4 col-form-label">Destination Warehouse</label>
                          <div class="col-lg-8">
                            <select class="form-select" v-model="toWarehouse" required>
                              <option v-for="whouse in warehouseList" :key="whouse.id" :value="whouse.id">{{
                                  whouse.name
                                }}
                              </option>
                            </select>
                          </div>
                        </div>

                        <div class="form-group row">
                          <label for="warehouseDate" class="col-lg-4 col-form-label">Date</label>
                          <div class="col-lg-8">
                            <input type="text" class="form-control" id="warhouseDatepicker" v-model="dateSelected"
                                   readonly/>
                          </div>
                        </div>
                        <div class="form-group row">
                          <label for="warehouseComment" class="col-lg-4 col-form-label">Comment</label>
                          <div class="col-lg-8">
                            <input type="text" class="form-control" id="warhouseComment" v-model="comment">
                          </div>
                        </div>
                      </div>
                    </div>

                  </div>
                </div>
                <div class="sell-submit-btn">
                  <button type="submit" class="btn btn-success mb-4">Submit Transfer</button>
                </div>
                <div class="supplier-information">
                  <div class="supplier-info-box">
                    <div class="card">
                      <div class="card-header">
                        <h5>History</h5>
                      </div>
                      <div class="card-body">
                        <table class="table table-bordered">
                          <thead class="card-header">
                          <tr>
                            <td>
                              Date
                            </td>
                            <td>
                              From
                            </td>
                            <td>
                              To
                            </td>
                            <td>
                              Product
                            </td>
                            <td>
                              Quantity
                            </td>
                            <td>
                              Comment
                            </td>
                          </tr>
                          </thead>
                          <tbody>
                          <template v-for="item in warehouseTransfers.results" :key="item.id">
                            <!--                          <tr v-for="item in warehouseTransfers.results" :key="item.id">-->
                            <tr v-for="(row, key) in item.product_list" :key="key">
                              <td
                                  v-if="key === 0"
                                  :rowspan="item.product_list.length"
                                  style="text-align: center; vertical-align: middle"
                              >{{ item.date }}
                              </td>
                              <td
                                  v-if="key === 0"
                                  :rowspan="item.product_list.length"
                                  style="text-align: center; vertical-align: middle"
                              >{{ item.warehouse_source.name }}
                              </td>
                              <td
                                  v-if="key === 0"
                                  :rowspan="item.product_list.length"
                                  style="text-align: center; vertical-align: middle"
                              >{{ item.warehouse_dest.name }}
                              </td>
                              <td
                                  style="text-align: center; vertical-align: middle"
                              >{{ row.product.product_name.name + ' - ' + row.product.category.name }}
                              </td>
                              <td
                                  style="text-align: center; vertical-align: middle"
                              >{{ row.quantity }}
                              </td>
                              <td
                                  v-if="key === 0"
                                  :rowspan="item.product_list.length"
                                  style="text-align: center; vertical-align: middle"
                              >{{ item.comment }}
                              </td>
                            </tr>
                          </template>
                          </tbody>
                        </table>
                        <div class="dashboard-search-result-button">
                          <button type="button" class="btn btn-outline-secondary bi bi-arrow-left" aria-label="Close"
                                  @click="findNextOrPrev(warehouseTransfers.previous)"
                                  :disabled="warehouseTransfers.previous=== null"></button>
                          <button type="button" class="btn btn-outline-secondary bi bi-arrow-right" aria-label="Close"
                                  @click="findNextOrPrev(warehouseTransfers.next)"
                                  :disabled="warehouseTransfers.next === null"></button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </form>
            </div>
          </div>
          <div class="col-lg-6">
            <div class="invoice-information">
              <div class="row">
                <div class="col-lg-6" style="margin: auto">
                  <h5>Invoice</h5>
                </div>
                <div class="col-lg-6">
                  <button class="btn btn-outline-primary mb-2" style="float: right" type="button">Print</button>
                </div>
              </div>
              <div class="invoice-info-box">
                <div class="invoice-heading card-header">
                  <h5>{{ COMPANY_NAME }}</h5>
                  <p><strong>Registration no:</strong> [Reg No/Vat No]</p>
                </div>
                <div class="invoice-info">
                  <div class="row">
                    <div class="col-lg-6">
                      <p><strong>Source Warehouse: </strong> {{ getWarehouseNameFromId(fromWarehouse) }} </p>
                    </div>
                    <div class="col-lg-6 text-right-align">
                      <p></p>
                    </div>
                    <div class="col-lg-6">
                      <p><strong>Destination Warehouse: </strong> {{ getWarehouseNameFromId(toWarehouse) }} </p>
                    </div>
                    <div class="col-lg-6 text-right-align">
                      <p></p>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-lg-6">
                      <p><strong>Date: </strong> {{ dateSelected }}</p>
                    </div>
                    <div class="col-lg-6 text-right-align">
                    </div>
                  </div>
                </div>
                <div class="invoice-table">
                  <h6>Product List</h6>
                  <table class="table table-bordered ">
                    <thead class="card-header">
                    <tr>
                      <th scope="col">Name</th>
                      <th scope="col">Quantity</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr v-for="row in productTable" :key="row.barcode" @click="setProductFromTable(row)">
                      <th scope="row">
                        <div class="product-name">
                          {{ row.productName }}
                          <div class="product-name-hover">
                            <span><i class="bi bi-pencil-square"></i></span>
                          </div>
                        </div>
                      </th>
                      <td>{{ row.quantity }}</td>
                    </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>


<style>
/*
===== Supplier Page CSS ==========
*/
body,
html {
  height: 100%;
  font-size: 12px;
}

.supplier {
  padding: 50px 0;
}


.supplier-info-box,
.product-info-box,
.invoice-info-box,
.warehouse-info-box {
  padding: 5px;
  border: 1px solid #dfdfdf;
  box-shadow: 0 0 3px 0px #e9e9e9;
  border-radius: 5px;
}

.supplier-info-box .form-group,
.product-info-box .form-group,
.warehouse-info-box .form-group {
  margin-bottom: 10px;
}

.supplier-info-box .form-group label {
  font-weight: 500;
}

.product-information,
.warehouse-information {
  margin-top: 20px;
}

.product-name {
  position: relative;
  cursor: pointer;
}

.product-name-hover {
  position: absolute;
  top: 0;
  right: 0;
  visibility: hidden;
  opacity: 0;
  transition: all .3s;
}

.product-name-hover span {
  display: inline-block;
}

.product-name:hover .product-name-hover {
  visibility: visible;
  opacity: 1;
}

.product-image {
  margin-bottom: 10px;
}

.supplier .fixed-top {
  top: 50px !important;
}

@media (max-width: 992px) {
  .invoice-information {
    margin-top: 20px;
  }
}

.invoice-table tr:hover {
  background: #f0f0f0;
}

.invoice-heading h4 {
  text-align: center;
  margin-bottom: 20px;
}

.product-button {
  display: flex;
  justify-content: flex-end;
}

.sell-submit-btn {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.invoice-info p {
  margin-bottom: 5px;
}

.invoice-info {
  margin-bottom: 20px;
}

#ui-datepicker-div {
  z-index: 10000 !important;
}

.col-form-label {
  font-size: 14px;
}

.invoice-info p {
  font-size: 13px;
}

.text-right-align {
  text-align: right;
}

.invoice-heading {
  text-align: center;
  padding-bottom: 5px;
  border-bottom: 1px solid #ccc;
}

.col-form-label {
  font-size: 12px;
}
</style>
