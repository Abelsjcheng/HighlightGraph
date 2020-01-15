<template>
  <div class="body">
    <el-container>
        <el-main>
            <div class="graph-header">
                <span style="width:160px">Graph_ID: {{images[current].id}}</span>
                <span style="display: inline-block;text-align: center;width: 1176px;">请判断是不是熟悉的? </span>
                <span style="display: inline-block;text-align: right;width:160px;">{{current+1}}/{{images.length}}</span>
            </div>
            <div class="image-container"></div>
            <div class="control-container">
                <div class="button-container">
                    <input type="button" id="next" class="bt-button" value="Next" @click="next();">
                </div>
            </div>
        </el-main>
    </el-container>
  </div>
</template>

<script>
import * as d3 from "d3"
import axios from '../assets/js/http'
export default {
  name: 'Test3',
  props: {
  },
  data() {
    return {
      images: [
          { 'id':'','image':''},
        ],
      current: 0,
      width: null,
      height: null,
      svg: null,
      svgWidth: null,
      svgHeight: null,
      second: 40,
      interval: null,
      percentage: 0,
      msg: ''
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.msg = this.$route.params.msg;
      //this.setContainerSize();
      this.initImages();
      this.shuffle(this.images);
      this.loadSvg();
    })
  },
  methods: {
    initImages() {
      if(this.msg == 'formal'){
        this.images = [
          
          { 'id':1,'image':'got_M.svg'},
          { 'id':2,'image':'got_M_F.svg'},
          { 'id':3,'image':'got_M_S1.svg'},
          { 'id':4,'image':'got_M_S2.svg'},
          { 'id':5,'image':'quakers_M.svg'},
          { 'id':6,'image':'quakers_M_F.svg'},
          { 'id':7,'image':'quakers_M_S1.svg'},
          { 'id':8,'image':'quakers_M_S2.svg'},
          { 'id':9,'image':'foorball_M.svg'},
          { 'id':10,'image':'foorball_M_F.svg'},
          { 'id':11,'image':'football_M_S1.svg'},
          { 'id':12,'image':'football_M_S2.svg'},
          { 'id':13,'image':'karate_M.svg'},
          { 'id':14,'image':'karate_M_F.svg'},
          { 'id':15,'image':'karate_M_S1.svg'},
          { 'id':16,'image':'karate_M_S2.svg'},
          { 'id':17,'image':'plo_M.svg'},
          { 'id':18,'image':'plo_M_F.svg'},
          { 'id':19,'image':'plo_M_S1.svg'},
          { 'id':20,'image':'plo_M_S2.svg'},
          { 'id':21,'image':'high_M.svg'},
          { 'id':22,'image':'high_M_F.svg'},
          { 'id':23,'image':'high_M_S1.svg'},
          { 'id':24,'image':'high_M_S2.svg'},
          { 'id':25,'image':'TI_M.svg'},
          { 'id':26,'image':'TI_M_F.svg'},
          { 'id':27,'image':'TI_M_S1.svg'},
          { 'id':28,'image':'TI_M_S2.svg'},
          { 'id':29,'image':'strike_M.svg'},
          { 'id':30,'image':'strike_M_F.svg'},
          { 'id':31,'image':'strike_M_S1.svg'},
          { 'id':32,'image':'strike_M_S2.svg'},
          { 'id':33,'image':'polactor_M.svg'},
          { 'id':34,'image':'polactor_M_F.svg'},
          { 'id':35,'image':'polactor_M_S1.svg'},
          { 'id':36,'image':'polactor_M_S2.svg'},
          { 'id':37,'image':'dol_M.svg'},
          { 'id':38,'image':'dol_M_F.svg'},
          { 'id':39,'image':'dol_M_S1.svg'},
          { 'id':40,'image':'dol_M_S2.svg'},
        ]
      }
      else if(this.msg == 'train'){
        this.images=[
          { 'id':1,'image':'kan_M.svg'},
          { 'id':2,'image':'kan_M_F.svg'},
          { 'id':3,'image':'kan_M_S1.svg'},
          { 'id':4,'image':'kan_M_S2.svg'},
        ]
      }
    },
    setContainerSize() {
      let screenWidth = document.documentElement.clientWidth ||  document.body.clientWidth;
      let screenHeight = document.documentElement.clientHeight || document.body.clientHeight;
      //document.querySelector(".graph-container").style.height = screenHeight * 0.7 + "px";
      
      //document.querySelector(".body").style.height = screenHeight + "px";
    },
    initInterval() {
      this.second = 0;
      this.interval = setInterval(() => {
        this.second += 1;
      }, 1000)
    },
    getSize() {
      let parentNode = document.querySelector(".image-container");
      this.width = parentNode.clientWidth;
      this.height = parentNode.clientHeight;
    },
    shuffle(arr) {
      let iLength = arr.length,
          i = iLength,
          mTemp,
          iRandom;
      while(i--){
          if(i !== (iRandom = Math.floor(Math.random() * iLength))){
              mTemp = arr[i];
              arr[i] = arr[iRandom];
              arr[iRandom] = mTemp;
          }
      }
      // console.log(arr)
      // var arr2 = arr;
      // for(let j = 0;j<iLength;j++){
      //   iRandom = (Math.floor(Math.random() * 3) + 2)+j;
      //   arr.splice(iRandom,0,arr2[j])
      // }
      // console.log(arr)
      return arr;
    },
    loadSvg() {
      let _this = this;
      this.getSize();
      d3.xml(_this.imagePath).then(function(xml) {
        document.querySelector(".image-container").appendChild(xml.documentElement);
        _this.svg = d3.select(".image-container svg");
        let svgWidth = _this.svg.attr("width");
        let svgHeight = _this.svg.attr("height");
        let margin = {left: 20, right: 20, top: 20, bottom: 20}
        let scaleNumber = d3.min([(_this.width - margin.left - margin.right) / svgWidth, (_this.height - margin.top - margin.bottom) / svgHeight]);
        _this.svgWidth = svgWidth * scaleNumber;
        _this.svgHeight = svgHeight * scaleNumber;
        _this.svg.attr("width", _this.svgWidth)
        .attr("height", _this.svgHeight)
        .style("position", "absolute")
        .style("left", (_this.width - _this.svgWidth) / 2 + "px")
        .style("top", (_this.height - _this.svgHeight) / 2 + "px");
        _this.initInterval();
      });
    },
    next() {
      clearInterval(this.interval);
      let timeFormat = d3.timeFormat("%Y-%m-%d %H:%M:%S");
      axios.post("/saveDuration/", {
        time: timeFormat(new Date()),
        name: this.imageName,
        consumingtime: this.second,
        qid: '',
        TestType: 3
      }).then(response => {
            
      })
      this.percentage += (100 / this.images.length);
      if (this.percentage > 100) {
        this.percentage = 100;
      }
      if(this.current >= this.images.length-1) {
        setTimeout(() => {
          if( this.msg == 'formal'){
            this.$router.push({ name: 'home', params: { msg: 'expertment' }});
          }else if( this.msg == 'train'){
            this.$router.push({ name: 'home', params: { msg: 'train' }});
          }
        }, 1000)
        return;
      } else {
        this.current += 1;
        d3.select(".image-container").selectAll("svg").remove();
        setTimeout(() => {
          this.loadSvg();
        }, 2000)
      }
    }
  },
  // watch: {
  //   imagePath(n, o) {
  //     d3.select(".graph-container").selectAll("svg").remove();
  //     this.loadSvg();
  //   }
  // },
  computed: {
    imagePath: function() {
      return "/static/images/lab3/" + this.images[this.current].image;
    },
    imageName: function() {
      let arr = this.imagePath.split("/");
      return arr[arr.length-1];
    },
    percent: function() {
      if(this.percentage >= 100) {
        return 100;
      } else {
        return Math.floor(this.percentage);
      }
    },
    consumingtime: function() {
      return 40 - this.second;
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

.content {
  width: 100%;
  padding: 20px;
}
.progress-container {
  text-align: center;
}
.el-main{
      padding: 0 20px;
}
#second {
  position: absolute;
  left: 5%;
  top: 12%;
  font-size: 30px;
  font-weight: bold;
  color: #ccc;
}
.graph-header{
  display: flex;
  justify-content: space-between;
  border-bottom: 2px solid #ccc;
  height: 59px;
  line-height: 59px;
  font-size: 1.5em;
  font-weight: bold;
}

.image-container {
  width: 900px;
  height: 580px;
  margin: 20px auto;
  border: 0.5px solid #ccc;
  position: relative;
}
.image-container >>> .selected {
 fill: red;
}
.button-container {
  width: 500px;
  margin: 0 auto;
  text-align: center;
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

.bt-button{
  display: inline-block;
  width: 90px;
  height:50px;
  line-height: 1;
  white-space: nowrap;
  cursor: pointer;
  background: #FFF;
  border: 1px solid #DCDFE6;
  margin: 0;
  text-align: center;
  border-radius: 4px;
}
.bt-button:focus{
  outline: 0
}
.bt-button:active{
    background-color: #ecf5ff;
    border-color: #3a8ee6;
    outline: 0;
}
</style>
