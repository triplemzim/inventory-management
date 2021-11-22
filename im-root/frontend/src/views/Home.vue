/* eslint-disable */
<script>
export default {
  methods: {
    goToSales: function () {
      console.log('go to sales');
      this.$router.push({name : 'sales'});
    },
    goToPurchase: function () {
      console.log('go to purchase');
      this.$router.push({name : 'purchase'});
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
            <div class="dashboard-search-input-box">
              <input type="search" class="form-control" placeholder="Invoice/ Phone/ Name">
              <button type="submit" class="dashboard-search-icon">
                <i class="bi bi-search"></i>
              </button>
            </div>
          </div>
          <div class="dashboard-card">
            <div class="row">
              <div class="col-md-4">
                <div class="dashboard-card-box">
                  <div class="dashboard-card-box-image">
                    <img src="@/assets/sale.jpg" alt="">
                  </div>
                  <div class="dashboard-card-box-body">
<!--                    <h6>Sales Form</h6>-->
                    <a @click="goToSales" class="btn btn-outline-secondary">Sales</a>
                  </div>
                </div>
              </div>
              <div class="col-md-4">
                <div class="dashboard-card-box">
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
                <div class="dashboard-card-box">
                  <div class="dashboard-card-box-image">
                    <img src="@/assets/default.jpg" alt="">
                  </div>
                  <div class="dashboard-card-box-body">
<!--                    <h6>Card Heading</h6>-->
                    <a @click="doNothing" class="btn btn-outline-secondary">Warehouse Transfer</a>
                  </div>
                </div>
              </div>
              <div class="col-md-4">
                <div class="dashboard-card-box">
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
                <div class="dashboard-card-box">
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
                <div class="dashboard-card-box">
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
.dashboard-right-box>h6 {
  font-weight: bold;
}
</style>
