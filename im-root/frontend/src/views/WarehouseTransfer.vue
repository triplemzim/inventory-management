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
              <form @submit.prevent="submitPurchase">

                <div class="product-information">

                  <div class="product-info-box">
                    <div class="card">
                      <div class="card-header">
                        <h6>Product</h6>
                      </div>
                      <div class="card-body">
                        <div class="form-group row">
                          <label for="productName" class="col-lg-4 col-form-label">Product Name</label>
                          <div class="col-lg-8">
                            <input class="form-control" list="datalistOptions2" id="productName"
                                   placeholder="Type to search..." v-on:input="handleSelectProduct($event)"
                                   v-bind:value="productName">
                            <datalist id="datalistOptions2">
                              <option v-for="item in productList" :key="item.id" :value="item.value"/>
                            </datalist>
                          </div>
                        </div>
                        <div class="row">
                          <div class="col-lg-6">
                            <div class="form-group row">
                              <label for="productBarcode" class="col-lg-4 col-form-label">Barcode</label>
                              <div class="col-lg-8">
                                <input @keyup.enter="handleSelectProductWithBarcode($event)" type="text"
                                       class="form-control" id="productBarcode" v-model="barcode">
                              </div>
                            </div>
                          </div>
                          <div class="col-lg-6">
                            <div class="form-group row">
                              <label for="productQuantity" class="col-lg-4 col-form-label">Quantity</label>
                              <div class="col-lg-8">
                                <input type="number" class="form-control" id="productQuantity" v-model="quantity">
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                      <div class="card-footer">
                        <div class="product-button">
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
                        <h6>Warehouse</h6>
                      </div>
                      <div class="card-body">
                        <div class="form-group row">
                          <label class="col-lg-4 col-form-label">Source Warehouse</label>
                          <div class="col-lg-8">
                            <select class="form-select" v-model="fromWarehouse">
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
                            <select class="form-select" v-model="toWarehouse">
                              <!--                        <option selected value="4">Warhouse One</option>-->
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
                            <input type="text" class="form-control" id="warhouseComment" v-model="warehouseComment">
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
                        <h6>History</h6>
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
                              Comment
                            </td>
                          </tr>
                          </thead>
                          <tbody>
                          <tr>
                            <td>{{ 'wa' }}</td>
                            <td>{{ 'wb' }}</td>
                            <td>{{ '11' }}</td>
                            <td>{{ 'no comment' }}</td>
                          </tr>
                          </tbody>
                        </table>
                        <div class="dashboard-search-result-button">
                          <button type="button" class="btn btn-outline-secondary bi bi-arrow-left" aria-label="Close"
                                  @click="findInvoice(previousSearch)" :disabled="previousSearch === null"></button>
                          <button type="button" class="btn btn-outline-secondary bi bi-arrow-right" aria-label="Close"
                                  @click="findInvoice(nextSearch)" :disabled="nextSearch === null"></button>
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
              <h5>Invoice</h5>
              <div class="invoice-info-box">
                <div class="invoice-heading card-header">
                  <h6>{{ COMPANY_NAME }}</h6>
                  <p><strong>Registration no:</strong> [Reg No/Vat No]</p>
                </div>
                <div class="invoice-info">
                  <div class="row">
                    <div class="col-lg-6">
                      <p><strong>Source Warehouse: </strong> {{ fromWarehouse }}</p>
                    </div>
                    <div class="col-lg-6 text-right-align">
                      <p></p>
                    </div>
                    <div class="col-lg-6">
                      <p><strong>Destination Warehouse: </strong> {{ toWarehouse }}</p>
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
                      <th scope="col">Price</th>
                      <th scope="col">Discount</th>
                      <th scope="col">Total</th>
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
                      <td>{{ row.price }}</td>
                      <td>{{ row.discount }}</td>
                      <td>{{ row.totalPrice }}</td>
                    </tr>
                    <!--                    <tr>-->
                    <!--                      <th scope="row">-->
                    <!--                        <div class="product-name">-->
                    <!--                          Product one-->
                    <!--                          <div class="product-name-hover">-->
                    <!--                            <span><i class="bi bi-pencil-square"></i></span>-->
                    <!--                          </div>-->
                    <!--                        </div>-->
                    <!--                      </th>-->
                    <!--                      <td>2</td>-->
                    <!--                      <td>100</td>-->
                    <!--                      <td>10</td>-->
                    <!--                      <td>90</td>-->
                    <!--                    </tr>-->
                    <!--                    <tr>-->
                    <!--                      <th scope="row">-->
                    <!--                        <div class="product-name">-->
                    <!--                          Product Two-->
                    <!--                          <div class="product-name-hover">-->
                    <!--                            <span><i class="bi bi-pencil-square"></i></span>-->
                    <!--                          </div>-->
                    <!--                        </div>-->
                    <!--                      </th>-->
                    <!--                      <td>2</td>-->
                    <!--                      <td>100</td>-->
                    <!--                      <td>10</td>-->
                    <!--                      <td>90</td>-->
                    <!--                    </tr>-->
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
</style>
