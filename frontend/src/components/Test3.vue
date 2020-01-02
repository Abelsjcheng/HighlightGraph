<template>
  <div class="body">
    <el-container>
        <el-main>
            <div class="graph-header">
                <span style="visibility:hidden;">{{current+1}}/{{images.length}} </span>
                <span>请判断是不是熟悉的? </span>
                <span>{{current+1}}/{{images.length}}</span>
            </div>
            <div class="graph-container"></div>
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
      images: [],
      current: 0,
      width: null,
      height: null,
      svg: null,
      svgWidth: null,
      svgHeight: null,
      second: 40,
      interval: null,
      percentage: 0,
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.setContainerSize();
      this.initImages();
      this.shuffle(this.images);
      this.loadSvg();
    })
  },
  methods: {
    initImages() {
      this.images = [
        // 好莱坞电影音乐网络
          // 美国离婚网络
          'sawmillM.svg', // 锯木厂网络
          'MexicanM.svg', // 墨西哥政治精英网络
          'kapmineM.svg', // 采矿工人网络
          'studentM.svg', // 学生会网络
          'polbooksM.svg', // 美国政治书籍网络
          // 火车爆炸事件网络
          // 网络高科技公司网络
          // 现代数学方法网络
        ]
    },
    setContainerSize() {
      let screenWidth = document.documentElement.clientWidth ||  document.body.clientWidth;
      let screenHeight = document.documentElement.clientHeight || document.body.clientHeight;
      document.querySelector(".graph-container").style.height = screenHeight * 0.7 + "px";
      document.querySelector(".body").style.height = screenHeight + "px";
    },
    initInterval() {
      this.second = 0;
      this.interval = setInterval(() => {
        this.second += 1;
      }, 1000)
    },
    getSize() {
      let parentNode = document.querySelector(".graph-container");
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
      console.log(arr)
      var arr2 = arr;
      for(let j = 0;j<iLength;j++){
        iRandom = (Math.floor(Math.random() * 3) + 2)+j;
        arr.splice(iRandom,0,arr2[j])
      }
      console.log(arr)
      return arr;
    },
    loadSvg() {
      let _this = this;
      this.getSize();
      d3.xml(_this.imagePath).then(function(xml) {
        document.querySelector(".graph-container").appendChild(xml.documentElement);
        _this.svg = d3.select(".graph-container svg");
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
          this.$router.push({ name: 'home', params: { msg: 'expertment' }});
        }, 1000)
        return;
      } else {
        this.current += 1;
        d3.select(".graph-container").selectAll("svg").remove();
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
      return "/static/images/lab3/" + this.images[this.current];
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
.body {
  width: 100%;
  border: 2px solid #b4b4b4;
  box-sizing: border-box;
}
.content {
  width: 100%;
  padding: 20px;
}
.progress-container {
  text-align: center;
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
  font-size: 1.5em;
  font-weight: bold;
}
.graph-header span{
  margin-bottom: 0.5rem;  
}
.graph-container {
  width: 70%;
  height: 720px;
  margin: 3% auto;
  border: 0.5px solid #ccc;
  position: relative;
}
.graph-container >>> .selected {
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
  width: 70px;
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
