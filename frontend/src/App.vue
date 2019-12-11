<template>
  <div id="app">
    <div class="header">
      <span><a href="/">Evaluation System</a></span>
      <el-button style="float:right;margin-top:10px;margin-right: 1%;" round @click="signout">Sign out </el-button>
    </div>
    <router-view></router-view>  </div>
</template>

<script>
import * as d3 from "d3"
import axios from './assets/js/http'
export default {
  name: 'app',
  components: {
  },
  data() {
    return {
    }
  },
  mounted() {
    this.$nextTick(() => {
    })
  },
  beforeDestroy() {
    axios.get('/signout/')
      .then(response => {
      })
  },
  methods: {
    signout() {
      axios.get('/signout/')
        .then(response => {
          if(response.data == 'OK') {
            alert("sign out")
            window.location.href="/";
          }
        })
    }
  }
}
</script>

<style>
/* * {
  border: 1px solid red;
} */
html, body {
  width: 100%;
  height: 100%;
  margin: 0 auto;
  overflow-x: hidden;
  /* overflow: hidden; */
}
.header {
  width: 100%;
  height: 20%;
  background-color: #ccc;
}
.header a {
  font-size: 25px;
  font-weight: bold;
  line-height: 60px;
  color: white;
  margin-left: 1%;
  text-decoration: none;
}
.signout{
  float: right;
}
/* .graph_img {
  border: black solid 1px;
  text-align: center;
  padding-top: 20px;
}
.body img {
  display: inline-block;
  width: 500px;
} */
</style>
