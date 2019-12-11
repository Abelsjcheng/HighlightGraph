<template>
  <div class="body">
    <div class="content">
      <div class="progress-container">
        <el-progress :percentage="percent"></el-progress>
      </div>
      <div style="display: flex;justify-content: center;">
        <el-card class="box-card">
            <P>图的名称：{{graphinfo.graphname}} </P>
            <P>图的类别标签：{{graphinfo.label}} </P>
            <P>背景信息：{{graphinfo.background}} </P>
        </el-card>
        <div class="main-container">
          <div class="graph-container">
              <el-image
                        class="graphselect"
                        :src="images[current]"
                        fit="contain"
                      ></el-image> 
          </div>
          <div class="control-container">
            <div class="button-container">
              <input type="button" id="previous" class="button" value="Previous" @click="previous();">
              <input type="button" id="next" class="button" value="Next" @click="next();">
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as d3 from "d3"
import axios from '../assets/js/http'
export default {
  name: 'Test',
  props: {
  },
  data() {
    return {
      images: [
          'static/images/kapmine.svg',
          'static/images/sawmill.svg',
          'static/images/kan.svg',
          'static/images/Mexican.svg',
          'static/images/studentgov.svg',
          'static/images/PloActor.svg'],
      current: 0,
      percentage: 0,
      testNum: 6,
      graphinfo: ''
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.setContainerSize();
      this.getBcakground();
    })
  },
  methods: {
    setContainerSize() {
      let screenWidth = document.documentElement.clientWidth ||  document.body.clientWidth;
      let screenHeight = document.documentElement.clientHeight || document.body.clientHeight;
      document.querySelector(".graph-container").style.height = screenHeight * 0.68 + "px";
    },
    previous() {
      this.percentage -= (100 / this.testNum);
        if (this.percentage < 0) {
          this.percentage = 0;
        }
      if(this.current <= 0) {
        alert("第一张...");
        return;
      }
      this.current -= 1;
      setTimeout(() => {
             this.getBcakground();
      }, 1000)
    },
    next() {
        this.percentage += (100 / this.testNum);
        if (this.percentage > 100) {
          this.percentage = 100;
        }
        if(this.current >= this.testNum-1) {
            setTimeout(() => {
            this.$router.push({ name: 'home', params: { msg: 'study' }});
            }, 1000)
            return;
        } else {
            this.current += 1;
            this.graphinfo = "";
            setTimeout(() => {
                this.getBcakground();
            }, 1000)
        }
        
      },
    getBcakground() {
        axios.post("/getBackground/", {
                name: this.imageName
            }).then(response => {
                let responseData = response.data
                this.graphinfo = responseData.datum[0]
                console.log(this.graphinfo.background)
            })
    }
  },
  computed: {
    imageName: function() {
      let arr = this.images[this.current].split("/");
      return arr[arr.length-1];
    },
    percent: function() {
      if(this.percentage >= 100) {
        return 100;
      } else {
        return Math.floor(this.percentage);
      }
    },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.body {
  width: 100%;
}
.content {
  width: 100%;
}
.progress-container {
  text-align: center;
}
#second {
  position: absolute;
  left: 33%;
  top: 7%;
  font-size: 30px;
  font-weight: bold;
  color: #ccc;
}

.main-container{
  width: 60%;
}
.graph-container {
  width: 80%;
  height: 720px;
  margin: 3% auto;
  border: 1px solid black;
  position: relative;
}
.graphselect{
  width: 100%; 
  height: 100%;
}
.graph-container >>> .selected {
 fill: red;
}
.button-container {
  width: 500px;
  margin: 0 auto;
}
.button {
  width: 100px;
  height: 50px;
  font-size: 18px;
  margin-bottom: 20px;
}
#redo {
  float: left;
}
#next {
  float: right;
}
.box-card{
  width: 500px;
  margin: 3% auto;
  font-size: 16px;
}
.background-container{
  float: left;
  width: 30%;
}
</style>
