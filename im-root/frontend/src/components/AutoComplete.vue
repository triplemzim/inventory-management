/* eslint-disable */
<template>
<!--  <div class="container">-->
<!--    <div class="row">-->
<!--      <div class="col">-->
        <label for="customerDataList" class="col-lg-4 col-form-label">{{ title }}</label>
        <div class="col-lg-8">
          <input class="form-control" list="datalistOptions" id="exampleDataList" placeholder="Type to search..." v-on:input="handleInput($event)" :value="bindValue">
          <datalist id="datalistOptions">
            <option v-for="item in dataList" :key="item.id" :value="item.value">{{'Phone: ' + item.id}}</option>
          </datalist>
        </div>
<!--      </div>-->
<!--    </div>-->
<!--  </div>-->
</template>

<script>
// @ is an alias to /src


export default {
  name: "AutoComplete",
  props: ['dataList', 'title', 'bindValue'],
  // data() {
  //   return {
  //     ds: this.dataList,
  //     ts: this.title,
  //   }
  // },
  emits: ['selectedData'],
  methods: {
    handleInput: function (event) {
      console.log(this.dataList);
      const item = this.dataList.filter(item =>
        item.value === event.target.value
      )[0];
      this.$emit('selectedData', item);
    }
  }

};
</script>
