/* eslint-disable */
<script>
import {getPurchaseInvoiceList, getSaleInvoiceList, getNextInvoiceList} from '@/common/apis';

export default {
  data() {
    return {
      searchResult: [],
      searchCount: 0,
      nextSearch: null,
      previousSearch: null,
      radioSelected: 'sale',
      searchText: ''
    }
  },
  methods: {
    goToSales: function () {
      this.$router.push({name: 'sales'});
    },
    goToPurchase: function () {
      this.$router.push({name: 'purchase'});
    },
    goToInvoice: async function (event) {
      // this.resetSearch();
      // this.searchText = '';
      this.$router.push({
        name: 'invoice',
        params: {
          invoice: JSON.stringify(event),
          type: this.radioSelected === 'sale' ? 'Sale Invoice' : 'Purchase Invoice'
        }
      });
    },
    findInvoice: async function (endpoint) {
      let response = null;
      if (endpoint) {
        response = await getNextInvoiceList(endpoint);
      } else if (this.radioSelected == 'sale') {
        response = await getSaleInvoiceList(this.searchText);
      } else {
        response = await getPurchaseInvoiceList(this.searchText);
      }

      this.searchCount = response.data.count;
      this.searchResult = response.data.results;
      this.nextSearch = response.data.next;
      this.previousSearch = response.data.previous;
    },
    resetSearch: function () {
      this.searchCount = 0;
      this.searchResult = [];
      this.nextSearch = null;
      this.previousSearch = null;
    }
  }
}
</script>


<template>
  <section class="dashboard">
    <div class="container">
      <div class="row">
        <div class="col-md-8">
          <div class="dashboard-search">
            <h6 style="font-weight: bold">Search Invoice</h6>
            <div style="font-size: 13px">
              <div class="form-check form-check-inline">
                <input class="form-check-input" type="radio" name="inlineRadioOptions" id="inlineRadio1" value="sale"
                       v-model="radioSelected" checked v-on:click="resetSearch">
                <label class="form-check-label" for="inlineRadio1">Sale</label>
              </div>
              <div class="form-check form-check-inline">
                <input class="form-check-input" type="radio" name="inlineRadioOptions" id="inlineRadio2"
                       value="purchase" v-model="radioSelected" v-on:click="resetSearch">
                <label class="form-check-label" for="inlineRadio2">Purchase</label>
              </div>
            </div>
            <div class="dashboard-search-input-box">
              <input @keyup.enter="findInvoice()" type="search" class="form-control" placeholder="Invoice/ Phone/ Name"
                     v-model="searchText">
              <button type="button" @click="findInvoice" class="dashboard-search-icon">
                <i class="bi bi-search m-2"></i>
              </button>
            </div>
            <div class="dashboard-search-result search-box" style="font-size: 11px"
                 v-if="searchCount > 0 && searchText !== ''">
              <div class="dashboard-search-result-box rounded" v-for="item in searchResult" :key="item.id"
                   @click="() => goToInvoice(item)">
                <h6>{{ item.name }}</h6>
                <p><b>Date:</b> {{ item.date }} -- <b>Invoice:</b> {{ item.invoice_no }} -- <b>Contact:</b>
                  {{ item.contact }}</p>
                <p><b>Warhouse
                  name:</b> {{ item.warehouse.name }}</p>
              </div>
              <!--              <div class="dashboard-search-result-box rounded">-->
              <!--                <h6>Muhim</h6>-->
              <!--                <p><b>date:</b> 23-23-2021 | <b>invoice:</b>23232 | <b>contact:</b>23232 | <b>warhouse-->
              <!--                  name:</b> one</p>-->
              <!--              </div>-->
              <!--              <div class="dashboard-search-result-box rounded">-->
              <!--                <h6>Muhim</h6>-->
              <!--                <p><b>date:</b>23-23-2021 | <b>invoice:</b>23232 | <b>contact:</b>23232 | <b>warhouse-->
              <!--                  name:</b> one</p>-->
              <!--              </div>-->
              <div class="dashboard-search-result-button">
                <button type="button" class="btn btn-outline-secondary bi bi-arrow-left" aria-label="Close"
                        @click="findInvoice(previousSearch)" :disabled="previousSearch === null"></button>
                <button type="button" class="btn btn-outline-secondary bi bi-arrow-right" aria-label="Close"
                        @click="findInvoice(nextSearch)" :disabled="nextSearch === null"></button>
              </div>
            </div>
          </div>
          <div class="dashboard-card">
            <div class="row">
              <div class="col-md-4">
                <div class="dashboard-card-box rounded">
                  <div class="dashboard-card-box-image rounded">
                    <img src="@/assets/sale.jpg" alt="">
                  </div>
                  <div class="dashboard-card-box-body">
                    <!--                    <h6>Sales Form</h6>-->
                    <a @click="goToSales" class="btn btn-outline-secondary">Sales</a>
                  </div>
                </div>
              </div>
              <div class="col-md-4">
                <div class="dashboard-card-box rounded">
                  <div class="dashboard-card-box-image">
                    <img src="@/assets/purchase.jpg" alt="">
                  </div>
                  <div class="dashboard-card-box-body">
                    <!--                    <h6>Card Heading</h6>-->
                    <a @click="goToPurchase" class="btn btn-outline-secondary">Purchase</a>
                  </div>
                </div>
              </div>
              <div class="col-md-4">
                <div class="dashboard-card-box rounded">
                  <div class="dashboard-card-box-image">
                    <img src="@/assets/default.jpg" alt="">
                  </div>
                  <div class="dashboard-card-box-body">
                    <!--                    <h6>Card Heading</h6>-->
                    <a @click="goToInvoice" class="btn btn-outline-secondary">Warehouse Transfer</a>
                  </div>
                </div>
              </div>
              <div class="col-md-4">
                <div class="dashboard-card-box rounded">
                  <div class="dashboard-card-box-image">
                    <img src="@/assets/default.jpg" alt="">
                  </div>
                  <div class="dashboard-card-box-body">
                    <!--                    <h6>Card Heading</h6>-->
                    <a @click="doNothing" class="btn btn-outline-secondary">Sales Return</a>
                  </div>
                </div>
              </div>
              <div class="col-md-4">
                <div class="dashboard-card-box rounded">
                  <div class="dashboard-card-box-image">
                    <img src="@/assets/default.jpg" alt="">
                  </div>
                  <div class="dashboard-card-box-body">
                    <!--                    <h6>Card Heading</h6>-->
                    <a @click="doNothing" class="btn btn-outline-secondary">Purchase Return</a>
                  </div>
                </div>
              </div>
              <div class="col-md-4">
                <div class="dashboard-card-box rounded">
                  <div class="dashboard-card-box-image">
                    <img src="@/assets/default.jpg" alt="">
                  </div>
                  <div class="dashboard-card-box-body">
                    <!--                    <h6>Card Heading</h6>-->
                    <a @click="doNothing" class="btn btn-outline-secondary">Reports</a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <h6 style="font-weight: bold; margin-left: 40px">Messages</h6>
          <div class="dashboard-right">
            <div class="dashboard-right-box">
              <h6>Stock</h6>
              <p>Rice Low in stock: 10 unit in Warehouse-A</p>
            </div>
            <div class="dashboard-right-box">
              <h6>Warehouse Transfer</h6>
              <p>Warehouse-A transferred items to Warehouse-B recently</p>
            </div>
            <div class="dashboard-right-box">
              <h6>Stock</h6>
              <p>Keyboard low in stock: 10 unit in Warehouse-B</p>
            </div>
            <div class="dashboard-right-box">
              <h6>Stock</h6>
              <p>Mice low in stock: 10 unit in Warehouse-B</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style>
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
  box-shadow: 0px 7px 10px -2px #E6E4E4;

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
  background: #E6E4E4;
}
</style>
