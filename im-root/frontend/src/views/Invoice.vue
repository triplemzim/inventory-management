<script>
import {ref} from "vue";
import {COMPANY_NAME} from "@/common/strings";

export default {
  setup() {
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
    const grandTotal = ref(null);
    const invoiceType = ref(null);
    const paymentType = ref(null);

    return {
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
      grandTotal,
      invoiceType,
      paymentType,
    }
  },
  created() {
    const data = JSON.parse(this.$route.params.invoice);
    console.log(data);
    this.invoiceType = this.$route.params.type;

    if (this.invoiceType === 'Sale Invoice') {
      this.customerName = data.customer.name;
      this.address = data.customer.address;
      this.contact = data.customer.contact;
      this.due = data.payment_due_gt;
      this.paymentReceived = data.payment_received_gt;
      this.grandTotal = data.payment_received_gt + data.payment_due_gt;
    } else {
      this.customerName = data.supplier.name;
      this.address = data.supplier.address;
      this.contact = data.supplier.contact;
      this.due = data.payment_due_gt;
      this.paymentReceived = data.payment_paid_gt;
      this.grandTotal = data.payment_paid_gt + data.payment_due_gt;

    }

    this.warehouse = data.warehouse.name;
    this.invoiceNo = data.invoice_no;
    this.dateSelected = data.date;
    this.productTable = data.productAndQuantity;
    this.paymentType = data.payment[0].payment_type;
  },
  methods: {
    getTotalPrice: function (row) {
      let priceNoDic = row.price * row.quantity;
      return priceNoDic - (priceNoDic * row.discount_in_percent / 100.0);
    },
    // getGrandTotal: function () {
    //   let sum = 0;
    //   this.productTable.forEach(x => {
    //     sum = sum + this.getTotalPrice(x);
    //   });
    //   return Math.floor(sum);
    // }
  }
}
</script>

<template>
  <div>
    <section class="customer">
      <div class="container">
        <div class="row">
          <div class="offset-0 col-12 offset-sm-2 col-sm-8">
            <div class="invoice-information">
              <div class="invoice-info-box">
                <div class="invoice-heading card-header">
                  <h5>{{ COMPANY_NAME }}</h5>
                  <h6>{{ invoiceType }}</h6>
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
                      <p><strong>Paid By:</strong> {{paymentType}}</p>
                    </div>
                    <div class="col-6 text-right-align">
                      <p><strong>Address:</strong> Bogra Sadar</p>
                    </div>
                    <div class="col-6">
                      <p></p>
                    </div>
                    <div class="col-6 text-right-align">
                      <p><strong>Date: </strong>{{ dateSelected }}</p>
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
                    <tr v-for="row in productTable" :key="row.product.barcode">
                      <th scope="row">
                        <div class="product-name">
                          {{ row.product.product_name.name }}
                          <div class="product-name-hover">
                            <span><i class="bi bi-pencil-square"></i></span>
                          </div>
                        </div>
                      </th>
                      <td>{{ row.quantity }}</td>
                      <td>{{ row.price }}</td>
                      <td>{{ row.discount_in_percent }}</td>
                      <td>{{ getTotalPrice(row) }}</td>
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
                          <td>{{ grandTotal }}</td>
                        </tr>
                        <tr>
                          <td><strong>Amount Paid:</strong></td>
                          <td>{{ paymentReceived }}</td>
                        </tr>
                        <tr>
                          <td><strong>Amount Due:</strong></td>
                          <td>{{ due }}</td>
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