/* eslint-disable */
<script>
// @ is an alias to /src
// import AutoComplete from "@/components/AutoComplete";
import { onMounted, ref } from "vue";
import { getStockAndExpiryWithBarcode, postPurchase } from "@/common/apis";
import { COMPANY_NAME } from "@/common/strings";
import {
  getSupplierList,
  getProductList,
  getWarehouseList,
} from "@/common/apis";
import utils from "@/common/util";

export default {
  name: "Purchase",
  components: {
    // AutoComplete
  },
  props: ["rootSupplierList", "rootProductList", "rootWarehouseList"],
  setup(props) {
    const supplierList = ref(null);
    const rawSupplierList = ref(null);
    const rawProductList = ref(null);
    const selectedSupplier = ref("");
    const componentName = ":home:";
    const productList = ref(null);
    const address = ref(null);
    const contact = ref(null);
    const barcode = ref(null);
    const quantity = ref(null);
    const price = ref(null);
    const discount = ref(null);
    const totalPrice = ref(null);
    const warehouse = ref("1");
    const invoiceNo = ref(null);
    const dateSelected = ref(null);
    const due = ref(null);
    const invoiceData = ref([]);
    const productName = ref(null);
    const supplierName = ref(null);
    const paymentReceived = ref(null);
    const productImage = ref(null);
    const warehouseList = ref(null);
    const productTable = ref(null);
    const paymentType = ref(null);
    const transactionId = ref(null);
    const stockAmount = ref(null);
    const expiryDate = ref(null);

    paymentType.value = "Cash";

    productTable.value = [];
    const today = new Date();
    dateSelected.value =
      today.getDate() +
      "/" +
      (today.getMonth() + 1) +
      "/" +
      today.getFullYear();

    onMounted(async () => {
      const returnData = [];
      const jq = window.jQuery;
      //DatePicker
      jq("#warhouseDatepicker").datepicker();
      jq("#productExpiryDatepicker").datepicker();

      // Supplier list
      let response = props.rootSupplierList;
      if (response.data == null) {
        response = await getSupplierList();
      }
      console.log(componentName, "api-supplier-list", response.data);
      response.data.forEach((supplier) => {
        const temp = {};
        temp.value = supplier.name;
        temp.id = supplier.custom_id;
        returnData.push(temp);
      });
      rawSupplierList.value = response.data;
      supplierList.value = returnData;

      //Product-List
      const productData = [];
      let anotherResponse = props.rootProductList;
      if (anotherResponse.data == null) {
        anotherResponse = await getProductList();
      }
      console.log(componentName, "api-product-list", anotherResponse.data);
      anotherResponse.data.forEach((product) => {
        const temp = {};
        temp.value = utils.getProductRep(product);
        temp.id = product.barcode;
        productData.push(temp);
      });
      rawProductList.value = anotherResponse.data;
      productList.value = productData;

      //Warehouse-list
      let warehouseListResponse = props.rootWarehouseList;
      if (warehouseListResponse.data == null) {
        warehouseListResponse = await getWarehouseList();
      }
      console.log(
        componentName,
        "api-warehouse-list",
        warehouseListResponse.data
      );
      warehouseList.value = warehouseListResponse.data;
      if (warehouseList.value.length > 0) {
        warehouse.value = warehouseList.value[0].id;
      }
    });

    return {
      supplierList,
      selectedSupplier,
      componentName,
      COMPANY_NAME,
      productList,
      address,
      contact,
      barcode,
      quantity,
      price,
      discount,
      totalPrice,
      warehouse,
      invoiceNo,
      dateSelected,
      due,
      invoiceData,
      productName,
      supplierName,
      paymentReceived,
      productImage,
      warehouseList,
      rawProductList,
      rawSupplierList,
      productTable,
      paymentType,
      transactionId,
      stockAmount,
      utils,
      expiryDate,
    };
  },
  methods: {
    handleSelectSupplier: function (supplier) {
      if (supplier == null) return;
      this.selectedSupplier = this.rawSupplierList.find(
        (x) => x.custom_id === supplier.id
      );
      this.supplierName = this.selectedSupplier.name;
      this.address = this.selectedSupplier.address;
      this.contact = this.selectedSupplier.contact;
    },
    handleSelectProduct: function (event) {
      console.log(this.componentName, event.target.value);
      const selectedProduct = this.rawProductList.find(
        (x) => utils.getProductRep(x) === event.target.value
      );
      // if(selectedProduct == null) {
      //   selectedProduct = this.rawProductList.find(x => x.barcode === event.target.value);
      // }
      if (selectedProduct == null) return;
      this.productName = utils.getProductRep(selectedProduct);
      this.productImage = selectedProduct.photo;
      this.barcode = selectedProduct.barcode;
      this.quantity = 1;
      this.price = selectedProduct.default_purchase_price;
      this.discount = 0;
      this.totalPrice = this.price;
      this.handleStock(this.barcode, this.warehouse);
    },
    handleSelectProductWithBarcode: function (event) {
      console.log(this.componentName, event.target.value);
      const selectedProduct = this.rawProductList.find(
        (x) => x.barcode.toString() === event.target.value.toString()
      );
      console.log(selectedProduct);
      if (selectedProduct == null) return;
      this.productName = utils.getProductRep(selectedProduct);
      this.productImage = selectedProduct.photo;
      this.quantity = 1;
      this.price = selectedProduct.default_purchase_price;
      this.discount = 0;
      this.totalPrice = this.price;
      this.handleStock(this.barcode, this.warehouse);
    },
    handleStock: async function (barcode, whouse) {
      const stock = await getStockAndExpiryWithBarcode(barcode, whouse);
      console.log(stock.data);
      this.stockAmount = stock.data.quantity;
      this.expiryDate = new Date(Date.parse(stock.data.expiry_date)).toLocaleDateString();
    },
    getTotalPrice: function () {
      if (this.barcode == null) return 0;
      let totalPrice = this.price * this.quantity;
      totalPrice = totalPrice - (totalPrice * this.discount) / 100.0;
      return totalPrice;
    },
    addProduct: function () {
      const row = {};
      row.productName = this.productName;
      row.quantity = this.quantity;
      row.discount = this.discount;
      row.price = this.price;
      row.totalPrice = this.getTotalPrice();
      row.barcode = this.barcode;
      const idx = this.productTable.findIndex(
        (x) => x.productName === row.productName
      );
      if (idx !== -1) this.productTable.splice(idx, 1);
      if (row.quantity === 0) {
        this.resetProduct();
        return;
      }
      this.productTable.push(row);
      this.paymentReceived = this.getGrandTotal();
      console.log("table", ...this.productTable);

      this.resetProduct();
    },
    getGrandTotal: function () {
      let gt = 0;
      this.productTable.forEach((x) => (gt = gt + x.totalPrice));
      return Math.floor(gt);
    },
    getAmountDue: function () {
      // return Number.parseFloat(this.getGrandTotal() - this.paymentReceived).toFixed(2);
      let due = this.getGrandTotal() - this.paymentReceived;
      if (due != null) due = Number.parseFloat(due).toFixed(2);
      return due;
    },
    resetProduct: function () {
      this.productName = "";
      this.quantity = 0;
      this.discount = 0;
      this.productImage = "";
      this.barcode = "";
      this.price = 0;
      this.paymentReceived = this.getGrandTotal();
      this.expiryDate = '';
    },
    getDateToday: function () {
      const today = new Date();
      return (
        today.getDate() +
        "/" +
        (today.getMonth() + 1) +
        "/" +
        today.getFullYear()
      );
    },
    setProductFromTable: function (row) {
      this.productName = row.productName;
      this.quantity = row.quantity;
      this.discount = row.discount;
      this.price = row.price;
      this.barcode = row.barcode;
      this.totalPrice = this.getTotalPrice();
    },
    submitPurchase: async function () {
      if (!confirm("Do you confirm to submit Purchase?")) {
        return;
      }
      if (this.isValidPurchase() == false) return;
      // basic info
      const requestBody = {};
      requestBody.name = this.supplierName;
      requestBody.contact = this.contact;
      requestBody.address = this.address;
      requestBody.invoice_no = this.invoiceNo;
      requestBody.payment_paid_gt = this.paymentReceived;
      requestBody.payment_due_gt = this.getAmountDue();
      requestBody.date = this.dateSelected;
      if (this.selectedSupplier != null) {
        requestBody.supplier = this.selectedSupplier.id;
      }
      requestBody.warehouse = this.warehouse;

      // Payment
      const payment = [];
      const onePayment = {};
      onePayment.debit_or_credit = "CREDIT";
      onePayment.amount = this.getGrandTotal();
      onePayment.date = this.dateSelected;
      onePayment.payment_type = this.paymentType;
      onePayment.invoice_no = this.invoiceNo;
      onePayment.transaction_id = this.transactionId;
      if (this.selectedSupplier != null) {
        onePayment.supplier = this.selectedSupplier.id;
      }
      payment.push(onePayment);
      requestBody.p_payment = payment;

      // Products
      const productList = [];
      this.productTable.forEach((x) => {
        const temp = {};
        temp.product = x.barcode;
        temp.invoice_no = this.invoiceNo;
        temp.quantity = x.quantity;
        temp.discount_in_percent = x.discount;
        temp.price = x.price;
        productList.push(temp);
      });
      requestBody.productAndQuantity = productList;
      console.log(
        this.componentName,
        "purchase-payload: ",
        JSON.stringify(requestBody)
      );
      const response = await postPurchase(requestBody);
      if (response.status === 201) {
        alert("Purchase Record Complete!");
        this.resetAll();
      }
    },
    resetAll: function () {
      this.resetProduct();
      this.selectedSupplier = "";
      this.supplierName = "";
      this.address = "";
      this.contact = "";
      this.invoiceNo = "";
      this.paymentReceived = "";
      this.productTable = [];
      this.paymentType = "Cash";
    },
    isValidPurchase: function () {
      if (this.productTable.length == 0) {
        alert("Please add some product!");
        return false;
      }
      return true;
    },
    deleteProduct: function () {
      const idx = this.productTable.findIndex(
        (x) => x.barcode === this.barcode
      );
      if (idx !== -1) this.productTable.splice(idx, 1);
      this.resetProduct();
    },
  },
};
</script>

<template>
  <div class="containerRoot" id="home">
    <h3 class="col-lg text-center mt-3" style="font-weight: bold">
      <span>Purchase</span>
    </h3>
    <section class="supplier">
      <div class="container">
        <div class="row">
          <div class="col-lg-6">
            <div class="sticky-top">
              <form @submit.prevent="submitPurchase">
                <div class="supplier-information">
                  <div class="supplier-info-box">
                    <div class="card">
                      <div class="card-header">
                        <h5>Supplier</h5>
                      </div>
                      <div class="card-body">
                        <div class="form-group row">
                          <AutoComplete
                            :dataList="supplierList"
                            :title="'Search Supplier'"
                            @selectedData="handleSelectSupplier"
                            key="supplier"
                            :bindValue="supplierName"
                          />
                        </div>
                        <div class="form-group row">
                          <label
                            for="supplierAddress"
                            class="col-lg-4 col-form-label"
                            >Supplier Name</label
                          >
                          <div class="col-lg-8">
                            <input
                              type="text"
                              required
                              class="form-control"
                              id="supplierName"
                              v-model="supplierName"
                            />
                          </div>
                        </div>
                        <div class="form-group row">
                          <label
                            for="supplierAddress"
                            class="col-lg-4 col-form-label"
                            >Address</label
                          >
                          <div class="col-lg-8">
                            <input
                              type="text"
                              class="form-control"
                              id="supplierAddress"
                              v-model="address"
                            />
                          </div>
                        </div>
                        <div class="form-group row">
                          <label
                            for="supplierContact"
                            class="col-lg-4 col-form-label"
                            >Contact</label
                          >
                          <div class="col-lg-8">
                            <input
                              type="text"
                              required
                              class="form-control"
                              id="supplierContact"
                              v-model="contact"
                            />
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="product-information">
                  <div class="product-info-box">
                    <div class="card">
                      <div class="card-header">
                        <h5>Product</h5>
                      </div>
                      <div class="card-body">
                        <div class="form-group row">
                          <label
                            for="productName"
                            class="col-lg-4 col-form-label"
                            >Product Name</label
                          >
                          <div class="col-lg-8">
                            <input
                              class="form-control"
                              list="datalistOptions2"
                              id="productName"
                              placeholder="Type to search..."
                              v-on:input="handleSelectProduct($event)"
                              v-bind:value="productName"
                              autocomplete="off"
                            />
                            <datalist id="datalistOptions2">
                              <option
                                v-for="item in productList"
                                :key="item.id"
                                :value="item.value"
                              />
                            </datalist>
                          </div>
                        </div>
                        <div class="row product-image">
                          <div class="col-lg-4 col-form-label">
                            <p>Product Image</p>
                          </div>
                          <div class="col-lg-8">
                            <img src="{{ productImage }}" class="" />
                          </div>
                        </div>
                        <div class="row">
                          <div class="col-lg-6">
                            <div class="form-group row">
                              <label
                                for="productBarcode"
                                class="col-lg-4 col-form-label"
                                >Barcode</label
                              >
                              <div class="col-lg-8">
                                <input
                                  @keydown.enter.prevent="
                                    handleSelectProductWithBarcode($event)
                                  "
                                  type="text"
                                  class="form-control"
                                  id="productBarcode"
                                  v-model="barcode"
                                />
                              </div>
                            </div>
                          </div>
                           <div class="col-lg-6">
                            <div class="form-group row">
                              <label
                                for="expiryDate"
                                class="col-lg-4 col-form-label"
                                >Expiry Date</label
                              >
                              <div class="col-lg-8">
                                <input
                                  type="text"
                                  class="form-control"
                                  id="productExpiryDatepicker"
                                  v-model="expiryDate"
                                  readonly
                                />
                              </div>
                            </div>
                          </div>
                        </div>
                        <div class="row">
                          <div class="col-lg-6">
                            <div class="form-group row">
                              <label
                                for="productQuantity"
                                class="col-lg-4 col-form-label"
                                >Quantity</label
                              >
                              <div class="col-lg-8">
                                <input
                                  type="number"
                                  class="form-control"
                                  id="productQuantity"
                                  v-model="quantity"
                                />
                              </div>
                            </div>
                          </div>
                          <div class="col-lg-6">
                            <div class="form-group row">
                              <label
                                for="availableStock"
                                class="col-lg-4 col-form-label"
                                >In Stock</label
                              >
                              <div class="col-lg-8">
                                <input
                                  type="number"
                                  readonly
                                  class="form-control"
                                  id="stockAmount"
                                  v-model="stockAmount"
                                />
                              </div>
                            </div>
                          </div>
                        </div>
                        <div class="row">
                          <div class="col-lg-6">
                            <div class="form-group row">
                              <label
                                for="productPrice"
                                class="col-lg-4 col-form-label"
                                >Price</label
                              >
                              <div class="col-lg-8">
                                <input
                                  type="text"
                                  class="form-control"
                                  id="productPrice"
                                  v-model="price"
                                />
                              </div>
                            </div>
                          </div>
                          <div class="col-lg-6">
                            <div class="form-group row">
                              <label
                                for="productDiscount"
                                class="col-lg-4 col-form-label"
                                >Discount (%)</label
                              >
                              <div class="col-lg-8">
                                <input
                                  type="number"
                                  class="form-control"
                                  id="productDiscount"
                                  v-model="discount"
                                />
                              </div>
                            </div>
                          </div>
                          <div class="col-lg-6">
                            <div class="form-group row">
                              <label
                                for="productPrice"
                                class="col-lg-4 col-form-label"
                                >Total Price</label
                              >
                              <div class="col-lg-8">
                                <input
                                  type="number"
                                  class="form-control"
                                  id="productPrice"
                                  readonly
                                  v-bind:value="getTotalPrice()"
                                />
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                      <div class="card-footer">
                        <div class="product-button">
                          <button
                            class="btn btn-danger mx-2"
                            :disabled="barcode == null || barcode === ''"
                            type="button"
                            @click="deleteProduct()"
                          >
                            Delete
                          </button>
                          <button
                            class="btn btn-success"
                            type="button"
                            @click="addProduct()"
                          >
                            Add / Update
                          </button>
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
                          <label class="col-lg-4 col-form-label"
                            >Warehouse Name</label
                          >
                          <div class="col-lg-8">
                            <select class="form-select" v-model="warehouse">
                              <!--                        <option selected value="4">Warhouse One</option>-->
                              <option
                                v-for="whouse in warehouseList"
                                :key="whouse.id"
                                :value="whouse.id"
                              >
                                {{ whouse.name }}
                              </option>
                              <!--                        <option value="1">Warhouse Two</option>-->
                              <!--                        <option value="2">Warhouse Three</option>-->
                              <!--                        <option value="3">Warhouse Four</option>-->
                            </select>
                          </div>
                        </div>
                        <div class="form-group row">
                          <label
                            for="warehouseInvoice"
                            class="col-lg-4 col-form-label"
                            >Invoice No</label
                          >
                          <div class="col-lg-8">
                            <input
                              type="text"
                              required
                              class="form-control"
                              id="warehouseInvoice"
                              v-model="invoiceNo"
                            />
                          </div>
                        </div>
                        <div class="form-group row">
                          <label
                            for="warehouseDate"
                            class="col-lg-4 col-form-label"
                            >Date</label
                          >
                          <div class="col-lg-8">
                            <input
                              type="text"
                              class="form-control"
                              id="warhouseDatepicker"
                              v-model="dateSelected"
                              readonly
                            />
                          </div>
                        </div>
                        <div class="form-group row">
                          <label class="col-lg-4 col-form-label"
                            >Payment Type</label
                          >
                          <div class="col-lg-8">
                            <select class="form-select" v-model="paymentType">
                              <option value="Cash">Cash</option>
                              <option value="Card">Card</option>
                              <option value="bKash">bKash</option>
                            </select>
                          </div>
                        </div>
                        <div class="form-group row">
                          <label
                            for="warehousePayment"
                            class="col-lg-4 col-form-label"
                            >Payment</label
                          >
                          <div class="col-lg-8">
                            <input
                              type="number"
                              class="form-control"
                              id="warhousePayment"
                              v-model="paymentReceived"
                            />
                          </div>
                        </div>
                        <div class="form-group row">
                          <label
                            for="transactionId"
                            class="col-lg-4 col-form-label"
                            >Transaction ID</label
                          >
                          <div class="col-lg-8">
                            <input
                              type="text"
                              class="form-control"
                              id="transactionId"
                              v-model="transactionId"
                              :required="paymentType !== 'Cash'"
                            />
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="sell-submit-btn">
                  <button type="submit" class="btn btn-success">Submit</button>
                </div>
              </form>
            </div>
          </div>
          <div class="col-lg-6">
            <div class="invoice-information">
              <h5>Invoice</h5>
              <div class="invoice-info-box">
                <div class="invoice-heading card-header">
                  <h5>{{ COMPANY_NAME }}</h5>
                  <p><strong>Registration no:</strong> [Reg No/Vat No]</p>
                </div>
                <div class="invoice-info">
                  <div class="row">
                    <div class="col-lg-6">
                      <p><strong>Supplier Name:</strong> {{ supplierName }}</p>
                    </div>
                    <div class="col-lg-6 text-right-align">
                      <p><strong>Invoice Number:</strong> {{ invoiceNo }}</p>
                    </div>
                    <div class="col-lg-6">
                      <p><strong>Address:</strong> {{ address }}</p>
                    </div>
                    <div class="col-lg-6 text-right-align">
                      <p><strong>Contact No:</strong> [Contact_No]</p>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-lg-6">
                      <p><strong>Contact:</strong> {{ contact }}</p>
                    </div>
                    <div class="col-lg-6 text-right-align">
                      <p><strong>Invoice Type:</strong> Supplier</p>
                    </div>
                    <div class="col-lg-6">
                      <p><strong>Paid By:</strong> {{ paymentType }}</p>
                    </div>
                    <div class="col-lg-6 text-right-align">
                      <p><strong>Address:</strong> Bogra Sadar</p>
                    </div>
                    <div class="col-6">
                      <p v-if="paymentType !== 'Cash'">
                        <strong>Transaction ID: </strong> {{ transactionId }}
                      </p>
                    </div>
                    <div class="col-lg-6 text-right-align">
                      <p><strong>Date:</strong>{{ dateSelected }}</p>
                    </div>
                  </div>
                </div>
                <div class="invoice-table">
                  <h6>Product List</h6>
                  <table class="table table-bordered">
                    <thead class="card-header">
                      <tr>
                        <th scope="col">Name</th>
                        <th scope="col">Quantity</th>
                        <th scope="col">Price</th>
                        <th scope="col">Discount</th>
                        <th scope="col">Total</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr
                        v-for="row in productTable"
                        :key="row.barcode"
                        @click="setProductFromTable(row)"
                      >
                        <th scope="row">
                          <div class="product-name">
                            {{ row.productName }}
                            <div class="product-name-hover">
                              <span><i class="bi bi-pencil-square"></i></span>
                            </div>
                          </div>
                        </th>
                        <td>{{ row.quantity }}</td>
                        <td>{{ row.price }}</td>
                        <td>{{ row.discount }}</td>
                        <td>{{ row.totalPrice }}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                <div class="invoice-subtotal">
                  <div class="row">
                    <div class="col-6 offset-6">
                      <table class="table">
                        <tbody>
                          <tr>
                            <td><strong>Grand Total:</strong></td>
                            <td>{{ getGrandTotal() }}</td>
                          </tr>
                          <tr>
                            <td><strong>Amount Paid:</strong></td>
                            <td>{{ paymentReceived }}</td>
                          </tr>
                          <tr>
                            <td><strong>Amount Due:</strong></td>
                            <td>{{ getAmountDue() }}</td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  </div>
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
  transition: all 0.3s;
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
