<script>
import {ref} from "vue";
import {COMPANY_NAME} from "@/common/strings";

export default {
  props: ['invoice'],
  setup(props) {
    const selectedCustomer = ref('');
    const componentName = ':invoice:';
    const address = ref(null);
    const contact = ref(null);
    const totalPrice = ref(null);
    const warehouse = ref(null);
    const invoiceNo = ref(null);
    const dateSelected = ref(null);
    const due = ref(null);
    const customerName = ref(null);
    const paymentReceived = ref(null);
    const productTable = ref(null);

    console.log(props.invoice);


    return {
      selectedCustomer,
      componentName,
      COMPANY_NAME,
      address,
      contact,
      totalPrice,
      warehouse,
      invoiceNo,
      dateSelected,
      due,
      customerName,
      paymentReceived,
      productTable,
    }
  },
  methods: {}
}
</script>

<template>
  <div>
    <section class="customer">
      <div class="container">
        <div class="row">
          <div class="offset-0 col-12 offset-sm-2 col-sm-8">
            <div class="invoice-information">
              <h4>Invoice</h4>
              <div class="invoice-info-box">
                <div class="invoice-heading card-header">
                  <h5>{{ COMPANY_NAME }}</h5>
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
                    <div class="col-6">
                      <p><strong>Contact:</strong> {{ contact }}</p>
                    </div>
                    <div class="col-6 text-right-align">
                      <p><strong>Registration no:</strong> [Reg No/Vat No]</p>
                    </div>
                    <div class="col-6">
                      <p></p>
                    </div>
                    <div class="col-6 text-right-align">
                      <p><strong>Address:</strong> Bogra Sadar</p>
                    </div>
                    <div class="col-6">
                      <p></p>
                    </div>
                    <div class="col-6 text-right-align">
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
                    <!-- <tr v-for="row in productTable" :key="row.barcode" @click="setProductFromTable(row)">
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
</tr> -->
                    <tr>
                      <th scope="row">
                        <div class="product-name">
                          Product one
                          <div class="product-name-hover">
                            <span><i class="bi bi-pencil-square"></i></span>
                          </div>
                        </div>
                      </th>
                      <td>2</td>
                      <td>100</td>
                      <td>10</td>
                      <td>90</td>
                    </tr>
                    <tr>
                      <th scope="row">
                        <div class="product-name">
                          Product Two
                          <div class="product-name-hover">
                            <span><i class="bi bi-pencil-square"></i></span>
                          </div>
                        </div>
                      </th>
                      <td>2</td>
                      <td>100</td>
                      <td>10</td>
                      <td>90</td>
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
                          <!--                          <td>{{ getGrandTotal() }}</td>-->
                        </tr>
                        <tr>
                          <td><strong>Amount Paid:</strong></td>
                          <!--                          <td>{{ paymentReceived }}</td>-->
                        </tr>
                        <tr>
                          <td><strong>Amount Due:</strong></td>
                          <!--                          <td>{{ getAmountDue() }}</td>-->
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
body,
html {
  height: 100%;
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
  font-size: 11px;
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
  font-size: 12px;
}

.invoice-info p {
  font-size: 11px;
}

.text-right-align {
  text-align: right;
}
</style>