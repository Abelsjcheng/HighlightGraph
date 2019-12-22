<template>
  <div class="body">
    <div class="content">
      <div class="progress-container">
        <el-progress :percentage="percent"></el-progress>
      </div>
      <div id="tooltip" class="hidden">
        <p><strong>编号</strong></p>
        <p><span id="value">100 </span></p>
      </div>
      <div style="display: flex;justify-content: center;">
        <el-card class="box-card">
            <P>图的名称：{{graphinfo.graphname}} </P>
            <P>图的类别标签：{{graphinfo.label}} </P>
            <div style="height:70%;overflow-y:auto;">背景信息：{{graphinfo.background}} </div>
        </el-card>
        <div class="main-container">
          <div class="graph-container"></div>
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
      images: [],
      current: 0,
      percentage: 0,
      testNum: 5,
      graphinfo: ''
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.setContainerSize();
      this.initImages();
      this.loadSvg();
      this.getBcakground();
    })
  },
  methods: {
    initImages() {
      this.images = [
        // 好莱坞电影音乐网络
          // 美国离婚网络
          'sawmill.svg', // 锯木厂网络
          'Mexican.svg', // 墨西哥政治精英网络
          'kapmine.svg', // 采矿工人网络
          'student.svg', // 学生会网络
          'polbooks.svg', // 美国政治书籍网络
          // 火车爆炸事件网络
          // 网络高科技公司网络
          // 现代数学方法网络
        ]
    },
    setContainerSize() {
      let screenWidth = document.documentElement.clientWidth ||  document.body.clientWidth;
      let screenHeight = document.documentElement.clientHeight || document.body.clientHeight;
      document.querySelector(".graph-container").style.height = screenHeight * 0.68 + "px";
      document.querySelector(".box-card").style.height = screenHeight * 0.68 + "px";
    },
    getSize() {
      let parentNode = document.querySelector(".graph-container");
      this.width = parentNode.clientWidth;
      this.height = parentNode.clientHeight;
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
        document.querySelector("#previous").removeAttribute("disabled");
        document.querySelector("#next").removeAttribute("disabled");
        _this.tooltip();
        
      });
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
      d3.select(".graph-container").selectAll("svg").remove();
      setTimeout(() => {
        this.loadSvg();
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
            d3.select(".graph-container").selectAll("svg").remove();
            document.querySelector("#previous").disabled = "disabled"
            document.querySelector("#next").disabled = "disabled"
            setTimeout(() => {
              this.loadSvg();
              this.getBcakground();
            }, 1000)
        }
        
      },
    tooltip(){
      d3.selectAll("circle").nodes().forEach(function(d,index) {
            let circle = d3.select(d);
            let x = parseFloat(circle.attr("cx"));
            let y = parseFloat(circle.attr("cy"));
            d3.select("#nodes").append('rect') //创建一个小矩形感应鼠标的moveover
            .attr('x',x-3) .attr('y',y-3) .attr('width',"6px")
		        .attr('height',"6px").attr('fill-opacity','0.0').on("mouseover",function(){
              d3.select("#tooltip")
              .style("left", (d3.event.pageX)+"px")
              .style("top", (d3.event.pageY+20)+"px")
              .select("#value")
              .text(index);
              d3.select("#tooltip").classed("hidden", false);
            }).on('mouseout',function(d){
              d3.select("#tooltip").classed("hidden", true);
            })
          })
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
  width: 70%;
}
.graph-container {
  width: 90%;
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
  width: 25%;
  margin: 3% auto;
  font-size: 20px;
}
.background-container{
  float: left;
  width: 30%;
}
#tooltip {
	position: absolute;
  width: 100px;
	height: auto;
	padding: 10px;
	background-color: white;
	-webkit-border-radius: 10px;
	-moz-border-radius: 10px;
	border-radius: 10px;
	-webkit-box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.4);
	-moz-box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.4);
	box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.4);
	pointer-events: none;
  z-index: 10000;
}
#tooltip.hidden {
	display: none;
}

#tooltip p {
	margin: 0;
	font-family: sans-serif;
	font-size: 16px;
	line-height: 20px;
}
.box-card /deep/ .el-card__body{
  height: 100%;
}
</style>
