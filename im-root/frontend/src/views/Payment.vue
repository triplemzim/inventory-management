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
                            />
                            <datalist id="datalistOptions2">
                              <option
                                v-for="item in productList"
                                :key="item.id"
                                :value="
                                  item.product_name.name +
                                  ' - ' +
                                  item.category.name
                                "
                              />
                            </datalist>
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
                        </div>
                      </div>
                      <div class="card-footer">
                        <div class="product-button">
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
                            >Source Warehouse</label
                          >
                          <div class="col-lg-8">
                            <select
                              class="form-select"
                              v-model="fromWarehouse"
                              required
                            >
                              <!--                        <option selected value="4">Warhouse One</option>-->
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
                          <label class="col-lg-4 col-form-label"
                            >Destination Warehouse</label
                          >
                          <div class="col-lg-8">
                            <select
                              class="form-select"
                              v-model="toWarehouse"
                              required
                            >
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
                          <label
                            for="warehouseComment"
                            class="col-lg-4 col-form-label"
                            >Comment</label
                          >
                          <div class="col-lg-8">
                            <input
                              type="text"
                              class="form-control"
                              id="warhouseComment"
                              v-model="comment"
                            />
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="sell-submit-btn">
                  <button type="submit" class="btn btn-success mb-4">
                    Submit Transfer
                  </button>
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
                              <td>Date</td>
                              <td>From</td>
                              <td>To</td>
                              <td>Product</td>
                              <td>Quantity</td>
                              <td>Comment</td>
                            </tr>
                          </thead>
                          <tbody>
                            <template
                              v-for="item in warehouseTransfers.results"
                              :key="item.id"
                            >
                              <!--                          <tr v-for="item in warehouseTransfers.results" :key="item.id">-->
                              <tr
                                v-for="(row, key) in item.product_list"
                                :key="key"
                              >
                                <td
                                  v-if="key === 0"
                                  :rowspan="item.product_list.length"
                                  style="
                                    text-align: center;
                                    vertical-align: middle;
                                  "
                                >
                                  {{ item.date }}
                                </td>
                                <td
                                  v-if="key === 0"
                                  :rowspan="item.product_list.length"
                                  style="
                                    text-align: center;
                                    vertical-align: middle;
                                  "
                                >
                                  {{ item.warehouse_source.name }}
                                </td>
                                <td
                                  v-if="key === 0"
                                  :rowspan="item.product_list.length"
                                  style="
                                    text-align: center;
                                    vertical-align: middle;
                                  "
                                >
                                  {{ item.warehouse_dest.name }}
                                </td>
                                <td
                                  style="
                                    text-align: center;
                                    vertical-align: middle;
                                  "
                                >
                                  {{
                                    row.product.product_name.name +
                                    " - " +
                                    row.product.category.name
                                  }}
                                </td>
                                <td
                                  style="
                                    text-align: center;
                                    vertical-align: middle;
                                  "
                                >
                                  {{ row.quantity }}
                                </td>
                                <td
                                  v-if="key === 0"
                                  :rowspan="item.product_list.length"
                                  style="
                                    text-align: center;
                                    vertical-align: middle;
                                  "
                                >
                                  {{ item.comment }}
                                </td>
                              </tr>
                            </template>
                          </tbody>
                        </table>
                        <div class="dashboard-search-result-button">
                          <button
                            type="button"
                            class="btn btn-outline-secondary bi bi-arrow-left"
                            aria-label="Close"
                            @click="findNextOrPrev(warehouseTransfers.previous)"
                            :disabled="warehouseTransfers.previous === null"
                          ></button>
                          <button
                            type="button"
                            class="btn btn-outline-secondary bi bi-arrow-right"
                            aria-label="Close"
                            @click="findNextOrPrev(warehouseTransfers.next)"
                            :disabled="warehouseTransfers.next === null"
                          ></button>
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
                  <button
                    class="btn btn-outline-primary mb-2"
                    style="float: right"
                    type="button"
                  >
                    Print
                  </button>
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
                      <p>
                        <strong>Source Warehouse: </strong>
                        {{ getWarehouseNameFromId(fromWarehouse) }}
                      </p>
                    </div>
                    <div class="col-lg-6 text-right-align">
                      <p></p>
                    </div>
                    <div class="col-lg-6">
                      <p>
                        <strong>Destination Warehouse: </strong>
                        {{ getWarehouseNameFromId(toWarehouse) }}
                      </p>
                    </div>
                    <div class="col-lg-6 text-right-align">
                      <p></p>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-lg-6">
                      <p><strong>Date: </strong> {{ dateSelected }}</p>
                    </div>
                    <div class="col-lg-6 text-right-align"></div>
                  </div>
                </div>
                <div class="invoice-table">
                  <h6>Product List</h6>
                  <table class="table table-bordered">
                    <thead class="card-header">
                      <tr>
                        <th scope="col">Name</th>
                        <th scope="col">Quantity</th>
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
