<template>
  <div id="app">
    <router-view></router-view>
  </div>
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
  created () {
    // 在页面加载时读取sessionStorage
    if (sessionStorage.getItem('store')) {
      this.$store.replaceState(Object.assign({}, this.$store.state, JSON.parse(sessionStorage.getItem('store'))))
    }
    // 在页面刷新时将store保存到sessionStorage里
    window.addEventListener('beforeunload', () => {
      sessionStorage.setItem('store', JSON.stringify(this.$store.state))
    })
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
  font-family: Arial, Helvetica, sans-serif;
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

#app{
  width: 1450px;
  height:750px;
  position: relative;
  top:50%;
  margin: 0 auto;
  margin-top: -375px;
  border: 2px solid #b4b4b4;
  box-sizing: border-box;
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
