/* eslint-disable */
<template>
  <div class="container">
    <div class="row">
      <div class="col">
        <label for="dataList" class="form-label m-1">{{props.title}}</label>
        <input class="form-control-sm m-1" list="datalistOptions" id="exampleDataList" placeholder="Type to search..." v-on:input="handleInput($event)">
        <datalist id="datalistOptions">
          <option v-for="item in props.data" data :key="item.id" :data-value="item.id" :value="item.value"/>
        </datalist>
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src


export default {
  name: "AutoComplete",
  props: {
    data: {
      type: Array
    },
    title: {
      type: String
    },
  },
  emits: ['selectedData'],
  setup(props) {
    console.log(props.data);

    return {
      props,
    }
  },
  methods: {
    handleInput: function (event) {
      const item = this.props.data.filter(item =>
        item.value === event.target.value
      )[0];
      this.$emit('selectedData', item);
    }
  }

};
</script>
