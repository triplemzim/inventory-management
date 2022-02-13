<script>
// @ is an alias to /src
// import AutoComplete from "@/components/AutoComplete";
import { COMPANY_NAME } from "@/common/strings";
import {
  getWarehouseList,
  postSale,
  getStockAndExpiryWithBarcode,
  salesmanAutocomplete,
  getSaleInvoiceList,
  getNextOrPrevList,
} from "@/common/apis";
import utils from "@/common/util";
import Datepicker from "vue3-datepicker";

export default {
  props: ["rootCustomerList", "rootProductList", "rootWarehouseList"],
  components: {
    // AutoComplete
    Datepicker,
  },
  data: function () {
    return {
      companyName: COMPANY_NAME,
      customerList: null,
      rawCustomerList: null,
      rawProductList: null,
      selectedCustomer: "",
      componentName: ":salesReturn:",
      productList: null,
      address: null,
      contact: null,
      barcode: null,
      quantity: null,
      price: null,
      discount: null,
      totalPrice: null,
      warehouse: "1",
      invoiceNo: null,
      dateSelected: null,
      due: null,
      invoiceData: [],
      productName: null,
      customerName: null,
      paymentReceived: null,
      productImage: null,
      warehouseList: null,
      productTable: [],
      paymentType: null,
      transactionId: null,
      stockAmount: null,
      expiryDate: null,
      salesman: null,
      salesmanList: null,
      salesDiscount: null,
      salesDiscountInPercent: null,
      salesmanId: null,
      searchResult: [],
      searchCount: null,
      nextSearch: null,
      previousSearch: null,
      radioSelected: "sale",
      searchText: "",
      grandTotal: 0,

      //New Vars

      allAvailableProducts: [],
      selectedInvoice: null,
      selectedProductId: "",
      selectedInvoiceNo: "",
    };
  },
  mounted: async function () {
    let warehouseListResponse = this.rootWarehouseList;
    if (warehouseListResponse == null || warehouseListResponse.data == null) {
      warehouseListResponse = await getWarehouseList();
    }
    console.log(
      this.componentName,
      "warehouse-list",
      warehouseListResponse.data
    );
    this.warehouseList = warehouseListResponse.data;
    if (this.warehouseList.length > 0) {
      this.warehouse = this.warehouseList[0].id;
    }
  },
  computed: {
    productCanBeDeleted: function () {
      const idx = this.productTable.findIndex(
        (x) => x.barcode === this.barcode
      );
      if (idx !== -1) return true;
      return false;
    },
    maxQuantity: function () {
      const totalPurchased = this.allAvailableProducts.find(
        (entry) => entry.product.barcode == this.barcode
      );
      if (totalPurchased) {
        const addedToInvoice = this.productTable.find(
          (entry) => (entry.barcode = this.barcode)
        );
        if (addedToInvoice) {
          return totalPurchased.quantity - addedToInvoice.quantity;
        }
        return totalPurchased.quantity;
      }
      return 0;
    },
  },
  watch: {
    selectedProductId(id) {
      const item = this.allAvailableProducts.find(
        (entry) => entry.product.id == id
      );
      if (item) {
        this.setProductFromInvoice(item);
      } else {
        this.resetProduct();
      }
    },
    quantity(new_value, old_value) {
      if (new_value > this.maxQuantity) {
        this.quantity = old_value;
      }
    },
  },
  methods: {
    handleSelectCustomer: function (customer) {
      if (customer == null) return;
      this.selectedCustomer = this.rawCustomerList.find(
        (x) => x.custom_id === customer.id
      );
      this.customerName = this.selectedCustomer.name;
      this.address = this.selectedCustomer.address;
      this.contact = this.selectedCustomer.contact;
      this.$refs.barcodeInput.focus();
    },
    handleSelectProduct: function (event) {
      console.log(this.componentName, event.target.value);
      const selectedProduct = this.rawProductList.find(
        (x) => utils.getProductRep(x) === event.target.value
      );
      if (selectedProduct == null) return;
      this.productName = utils.getProductRep(selectedProduct);
      this.productImage = selectedProduct.photo;
      this.barcode = selectedProduct.barcode;
      this.quantity = 1;
      this.price = selectedProduct.default_sales_price;
      this.discount = 0;
      this.totalPrice = this.price;
      this.handleStock(this.barcode, this.warehouse);
    },
    handleSelectProductWithBarcode: async function (event) {
      if (event.target.value.toString().trim() == "") return;

      const splittedCode = event.target.value.toString().split("_");
      this.barcode = splittedCode[0].trim();
      let expiryString = null;
      if (splittedCode.length > 1) {
        expiryString = splittedCode[1].trim();
      }

      const selectedProduct = this.rawProductList.find(
        (x) => x.barcode.toString() === this.barcode
      );
      console.log(selectedProduct);
      if (selectedProduct == null) return;
      this.productName = utils.getProductRep(selectedProduct);
      this.productImage = selectedProduct.photo;
      this.quantity = 1;
      this.price = selectedProduct.default_sales_price;
      this.discount = 0;
      this.totalPrice = this.price;
      await this.handleStock(this.barcode, this.warehouse);
      if (expiryString != null) {
        this.expiryDate = new Date(Date.parse(expiryString));
        console.log("parsed date: ", new Date(Date.parse(expiryString)));
      }
    },
    handleStock: async function (barcode, whouse) {
      const stock = await getStockAndExpiryWithBarcode(barcode, whouse);
      console.log(stock.data);
      this.stockAmount = stock.data.quantity;
      if (isNaN(Date.parse(stock.data.expiry_date))) {
        this.expiryDate = null;
      } else {
        this.expiryDate = new Date(Date.parse(stock.data.expiry_date));
      }
      this.$refs.barcodeInput.focus();
    },
    getTotalPrice: function () {
      if (this.barcode == null) return 0;
      let totalPrice = this.price * this.quantity;
      totalPrice = totalPrice - (totalPrice * this.discount) / 100.0;
      return totalPrice;
    },
    addProduct: function () {
      const row = {};
      if (this.quantity > this.stockAmount) {
        alert("Product low in stock!");
        return;
      }
      row.productName = this.productName;
      row.quantity = this.quantity;
      row.discount = this.discount;
      row.salesDiscount = this.salesDiscount;
      row.price = this.price;
      row.totalPrice = this.getTotalPrice();
      row.barcode = this.barcode;
      const idx = this.productTable.findIndex(
        (x) => x.productName === row.productName
      );
      if (idx !== -1) this.productTable.splice(idx, 1);
      if (row.quantity === 0) return;
      this.productTable.push(row);
      this.paymentReceived = this.getGrandTotal();

      this.resetProduct();
      this.selectedProductId = "";
    },
    getGrandTotal: function () {
      let gt = 0;
      this.productTable.forEach((x) => (gt = gt + x.totalPrice));
      return Math.floor(gt);
    },
    getTotalComission: function () {
      let tc = 0;
      this.productTable.forEach((x) => (tc = tc + x.salesDiscount));
      return tc;
    },
    getAmountDue: function () {
      // return Number.parseFloat(this.getGrandTotal() - this.paymentReceived).toFixed(2);
      let due = this.getGrandTotal() - this.paymentReceived;
      if (due != null) due = Number.parseFloat(due);
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
      this.stockAmount = "";
      this.expiryDate = null;
      this.$refs.barcodeInput.focus();
      this.salesDiscountInPercent = 0;
      this.salesDiscount = 0;
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
      this.selectedProductId = this.allAvailableProducts.find(
        (entry) => entry.product.barcode == row.barcode
      ).product.id;
      this.productName = row.productName;
      this.quantity = row.quantity;
      this.discount = row.discount;
      this.price = row.price;
      this.barcode = row.barcode;
      this.handleStock(this.barcode, this.warehouse);
      this.totalPrice = this.getTotalPrice();
    },
    submitSale: async function () {
      if (!confirm("Do you confirm to submit Sale?")) {
        return;
      }
      if (this.isValidSale() == false) return;
      // basic info
      const requestBody = {};
      requestBody.name = this.customerName;
      requestBody.contact = this.contact;
      requestBody.address = this.address;
      requestBody.invoice_no = this.invoiceNo;
      requestBody.payment_received_gt = this.paymentReceived;
      requestBody.payment_due_gt = this.getAmountDue();
      requestBody.date = this.dateSelected;
      requestBody.salesman = this.salesmanId;
      if (this.selectedCustomer != null) {
        requestBody.customer = this.selectedCustomer.id;
      }
      requestBody.warehouse = this.warehouse;

      // Payment
      const payment = [];
      const onePayment = {};
      onePayment.debit_or_credit = "DEBIT";
      onePayment.amount = this.getGrandTotal();
      onePayment.date = this.dateSelected;
      onePayment.payment_type = this.paymentType;
      onePayment.invoice_no = this.invoiceNo;
      onePayment.transaction_id = this.transactionId;
      if (this.selectedCustomer != null) {
        onePayment.customer = this.selectedCustomer.id;
      }
      payment.push(onePayment);
      requestBody.payment = payment;

      // Products
      const productList = [];
      this.productTable.forEach((x) => {
        const temp = {};
        temp.product = x.barcode;
        temp.invoice_no = this.invoiceNo;
        temp.quantity = x.quantity;
        temp.discount_in_percent = x.discount;
        temp.price = x.price;
        temp.salesman_discount = x.salesDiscount;
        productList.push(temp);
      });
      requestBody.productAndQuantity = productList;
      console.log(
        this.componentName,
        "sale-payload: ",
        JSON.stringify(requestBody)
      );
      const response = await postSale(requestBody); // Write down the Api for sales return
      if (response.status === 201) {
        alert("Sale Record Complete!");
        await this.printInvoice();
        this.resetAll();
        this.allAvailableProducts = [];
        this.selectedInvoice = null;
        this.selectedProductId = "";
        this.selectedInvoiceNo = "";
      }
    },
    resetAll: function () {
      this.resetProduct();
      this.selectedCustomer = "";
      this.customerName = "";
      this.address = "";
      this.contact = "";
      this.invoiceNo = "";
      this.paymentReceived = "";
      this.productTable = [];
      this.paymentType = "Cash";
    },
    isValidSale: function () {
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
      this.selectedProductId = "";
    },
    handleSalesmanInput: async function (event) {
      if (event.target.value == "") {
        return;
      }
      this.salesman = event.target.value;
      this.salesmanId = null;
      const response = await salesmanAutocomplete(
        utils.getSalesmanName(event.target.value)
      );
      this.salesmanList = response.data;
      if (this.salesmanList == null) return;

      const selectedItem = this.salesmanList.find(
        (x) => utils.getSalesmanRep(x) === event.target.value
      );

      if (selectedItem == null) return;

      this.salesman = utils.getSalesmanRep(selectedItem);
      this.salesmanId = selectedItem.id;
    },
    calculateSalesDiscount: function () {
      this.salesDiscount =
        (this.getTotalPrice() * this.salesDiscountInPercent) / 100.0;
    },
    printInvoice: async function () {
      await this.$htmlToPaper("invoiceToPrint");
    },

    // Invoice methods
    goToInvoice: async function (event) {
      this.resetAll();
      this.selectedInvoiceNo = event.invoice_no;
      this.selectedProductId = "";
      this.selectedInvoice = event;
      this.allAvailableProducts = event.productAndQuantity;
      this.customerName = event.customer.name;
      this.address = event.customer.address;
      this.contact = event.customer.contact;
    },
    findInvoice: async function (endpoint) {
      let response = null;
      if (endpoint) {
        response = await getNextOrPrevList(endpoint);
      } else {
        response = await getSaleInvoiceList(this.searchText);
      }
      console.log("response for findInvoice", response);

      this.searchCount = response.data.count;
      this.searchResult = response.data.results;
      this.nextSearch = response.data.next;
      this.previousSearch = response.data.previous;

      console.log("search count", this.searchCount);
    },
    totalPriceForSingleProduct: function (row) {
      let priceNoDic = row.price * row.quantity;
      return priceNoDic - (priceNoDic * row.discount_in_percent) / 100.0;
    },
    setProductFromInvoice: function (row) {
      this.resetProduct();
      console.log("hello world", row);
      this.productName = row.product.name;
      this.quantity = row.quantity;
      this.discount = row.discount;
      this.price = row.price;
      this.barcode = row.product.barcode;
      this.handleStock(this.barcode, this.warehouse);
      this.discount = row.discount_in_percent;
      this.salesDiscount = row.salesman_discount;
      this.salesDiscountInPercent =
        (this.salesDiscount * 100) / this.getTotalPrice();
    },
  },
};
</script>

<template>
  <div class="containerRoot" id="home">
    <h3 class="col-lg text-center mt-3" style="font-weight: bold">
      <span>Sales Return</span>
    </h3>
    <section class="customer">
      <div class="container">
        <div class="row">
          <div class="col-lg-6">
            <div class="dashboard-search">
              <h6 style="font-weight: bold">Search Invoice</h6>
              <div class="dashboard-search-input-box">
                <input
                  @keyup.enter="findInvoice()"
                  type="search"
                  class="form-control"
                  placeholder="Invoice/ Phone/ Name"
                  v-model="searchText"
                />
                <button
                  type="button"
                  @click="findInvoice()"
                  class="dashboard-search-icon"
                >
                  <i class="bi bi-search m-2"></i>
                </button>
              </div>
              <div
                class="dashboard-search-result search-box"
                style="font-size: 11px"
                v-if="searchCount > 0 && searchText !== ''"
              >
                <div
                  class="dashboard-search-result-box rounded"
                  v-for="item in searchResult"
                  :key="item.id"
                  @click="() => goToInvoice(item)"
                >
                  <h6>{{ item.name }}</h6>
                  <p>
                    <b>Date:</b> {{ item.date }} -- <b>Invoice:</b>
                    {{ item.invoice_no }} -- <b>Contact:</b> {{ item.contact }}
                  </p>
                  <p><b>Warhouse name:</b> {{ item.warehouse.name }}</p>
                </div>
                <div class="dashboard-search-result-button">
                  <button
                    type="button"
                    class="btn btn-outline-secondary bi bi-arrow-left"
                    aria-label="Close"
                    @click="findInvoice(previousSearch)"
                    :disabled="previousSearch === null"
                  ></button>
                  <button
                    type="button"
                    class="btn btn-outline-secondary bi bi-arrow-right"
                    aria-label="Close"
                    @click="findInvoice(nextSearch)"
                    :disabled="nextSearch === null"
                  ></button>
                </div>
              </div>
            </div>
          </div>
        </div>
        <p v-if="selectedInvoiceNo">Invoice No {{ selectedInvoiceNo }}</p>
        <div class="row">
          <div class="col-lg-6">
            <div class="sticky-top">
              <form @submit.prevent="submitSale">
                <div class="product-information">
                  <div class="product-info-box">
                    <div class="card">
                      <div class="card-header">
                        <h5>Product</h5>
                      </div>
                      <div class="card-body">
                        <div class="form-group row">
                          <label class="col-lg-4 col-form-label">Product</label>
                          <div class="col-lg-8">
                            <select
                              class="form-select"
                              v-model="selectedProductId"
                              :disabled="allAvailableProducts.length == 0"
                            >
                              <option value="">Select a product</option>
                              <option
                                v-for="item in allAvailableProducts"
                                :key="item.product.id"
                                :value="item.product.id"
                              >
                                {{ item.product.name }}
                              </option>
                            </select>
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
                                  ref="barcodeInput"
                                  v-on:keydown.enter.prevent="
                                    handleSelectProductWithBarcode($event)
                                  "
                                  type="text"
                                  class="form-control"
                                  id="productBarcode"
                                  v-model="barcode"
                                  autocomplete="off"
                                />
                              </div>
                            </div>
                          </div>
                          <div class="col-lg-6">
                            <div class="form-group row">
                              <label
                                for="productExpiry"
                                class="col-lg-4 col-form-label"
                                >Expiry Date</label
                              >
                              <div class="col-lg-8">
                                <datepicker
                                  class="form-control"
                                  id="productExpiryDatepicker"
                                  v-model="expiryDate"
                                  inputFormat="dd-MMM-yyyy"
                                  disabled
                                  v-bind:style="
                                    expiryDate == '' || expiryDate > new Date()
                                      ? ''
                                      : 'border-color: red'
                                  "
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
                                  min="0"
                                  :max="maxQuantity"
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
                        </div>
                        <div class="row">
                          <div class="col-lg-6">
                            <div class="form-group row">
                              <label
                                for="productPrice"
                                class="col-lg-4 col-form-label"
                                >Commission (%)
                              </label>
                              <div class="col-lg-8">
                                <input
                                  type="number"
                                  class="form-control"
                                  id="sales_discount"
                                  v-on:input="calculateSalesDiscount()"
                                  v-model="salesDiscountInPercent"
                                />
                              </div>
                            </div>
                          </div>
                          <div class="col-lg-6">
                            <div class="form-group row">
                              <label
                                for="productPrice"
                                class="col-lg-4 col-form-label"
                                >In BDT</label
                              >
                              <div class="col-lg-8">
                                <input
                                  type="number"
                                  class="form-control"
                                  id="sales_discount"
                                  readonly
                                  v-model="salesDiscount"
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
                            v-if="productCanBeDeleted"
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
                              <option
                                v-for="whouse in warehouseList"
                                :key="whouse.id"
                                :value="whouse.id"
                              >
                                {{ whouse.name }}
                              </option>
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
                            <datepicker
                              v-model="dateSelected"
                              class="form-control"
                              inputFormat="dd-MMM-yyyy"
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
                        <div
                          class="form-group row"
                          v-if="paymentType != 'Cash'"
                        >
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

          <div class="col-6">
            <div class="report-print-button text-right">
              <button class="btn btn-outline-danger" @click="printInvoice()">
                Print
              </button>
            </div>
            <div id="invoiceToPrint" class="invoice-information">
              <h5>Return Invoice</h5>
              <div class="invoice-info-box">
                <div class="invoice-heading card-header">
                  <h5>{{ COMPANY_NAME }}</h5>
                  <p><strong>Registration no:</strong> [Reg No/Vat No]</p>
                </div>
                <div class="invoice-info">
                  <div class="row">
                    <div class="col-6">
                      <p><strong>Customer Name:</strong> {{ customerName }}</p>
                    </div>
                    <div class="col-6 text-right-align">
                      <p><strong>Invoice Number:</strong> {{ invoiceNo }}</p>
                    </div>
                    <div class="col-6">
                      <p><strong>Address:</strong> {{ address }}</p>
                    </div>
                    <div class="col-6 text-right-align">
                      <p><strong>Contact No:</strong> [Contact_No]</p>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-6">
                      <p><strong>Contact:</strong> {{ contact }}</p>
                    </div>
                    <div class="col-6 text-right-align">
                      <p><strong>Invoice Type:</strong> Customer</p>
                    </div>
                    <div class="col-6">
                      <p><strong>Paid By:</strong> {{ paymentType }}</p>
                    </div>
                    <div class="col-6 text-right-align">
                      <p><strong>Address:</strong> Bogra Sadar</p>
                    </div>
                    <div class="col-6">
                      <p v-if="paymentType !== 'Cash'">
                        <strong>Transaction ID: </strong> {{ transactionId }}
                      </p>
                    </div>
                    <div class="col-6 text-right-align">
                      <p><strong>Date:</strong>{{ dateSelected }}</p>
                    </div>
                  </div>
                </div>
                <div class="invoice-table">
                  <h5>Product List</h5>
                  <table class="table table-bordered">
                    <thead class="card-header">
                      <tr>
                        <th scope="col">Name</th>
                        <th scope="col">Quantity</th>
                        <th scope="col">Price</th>
                        <th scope="col">Discount</th>
                        <th scope="col">Commission</th>
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
                        <td>{{ row.salesDiscount }}</td>
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
                          <tr>
                            <td><strong>Total Commission:</strong></td>
                            <td>{{ getTotalComission() }}</td>
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
===== Customer Page CSS ==========
*/
body,
html {
  height: 100%;
  font-size: 12px;
}

.customer {
  padding: 50px 0;
}

.customer-info-box,
.product-info-box,
.invoice-info-box,
.warehouse-info-box {
  padding: 5px;
  border: 1px solid #dfdfdf;
  box-shadow: 0 0 3px 0px #e9e9e9;
  border-radius: 5px;
  /*font-size: 11px;*/
}

.customer-info-box .form-group,
.product-info-box .form-group,
.warehouse-info-box .form-group {
  margin-bottom: 10px;
}

.customer-info-box .form-group label {
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

.customer .fixed-top {
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

.dashboard {
  padding: 50px 0;
}

.dashboard-card-box-image img {
  width: 100%;
  object-fit: cover;
  height: 100%;
  padding: 8px;
  padding-bottom: 0px;
}

.dashboard-card-box {
  box-shadow: 0px 7px 10px -2px #afafaf;
  margin-bottom: 40px;
  width: 90%;
  /*border-radius: 5%;*/
}

.dashboard-card-box-body {
  padding: 10px 5px;
}

.dashboard-right {
  border: 1px solid #ccc;
  padding: 10px;
  max-height: 540px;
  overflow-y: scroll;
  font-size: 13px;
}

.dashboard-right-box {
  border: 1px solid #f1f1f1;
  padding: 8px;
  margin-bottom: 24px;
  box-shadow: 0 0 2px 2px #e9e9e9;
  border-radius: 5px;
}

.dashboard-right-box p {
  margin-bottom: 0;
}

.dashboard-search {
  margin-bottom: 30px;
}

.dashboard-search-input-box {
  width: 99%;
  position: relative;
  padding-right: 12px;
}

.dashboard-search-icon {
  position: absolute;
  display: inline-block;
  top: 50%;
  right: 10px;
  transform: translateY(-50%);
  border: 0;
  background: transparent;
}

.dashboard-search-input-box input {
  padding-right: 40px;
}

.dashboard-card-box-body .btn {
  width: 100%;
  margin-top: 20px;
}

.dashboard-card-box-image {
  height: 108px;
}

.dashboard-right {
  margin-left: 30px;
}

.dashboard-right-box > h6 {
  font-weight: bold;
}

.dashboard-search-result {
  border: 1px solid #ccc;
  padding: 10px;
  /*background: #F3F2F2;*/
}

.dashboard-search-result-box {
  padding: 5px;
  margin-bottom: 15px;
  cursor: pointer;
  border-bottom: 1px solid grey;
  box-shadow: 0px 7px 10px -2px #e6e4e4;
}

.dashboard-search-result-box p {
  margin-bottom: 2px;
}

.dashboard-search-result-box h6 {
  margin-bottom: 0;
}

.dashboard-search-result-button {
  text-align: right;
}

.search-box {
  width: 97%;
}

.dashboard-search-result-box:hover {
  background: #e6e4e4;
}
</style>
