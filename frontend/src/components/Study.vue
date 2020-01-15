<template>
  <div class="body">
    <div class="content">
      <div class="progress-container">
        <el-progress :percentage="percent"></el-progress>
      </div>
      <div id="tooltip" class="hidden">
        <p><strong>ID: </strong><strong id="value">100 </strong></p>
      </div>
      <div style="display: flex;justify-content: space-around;">
        <el-card class="box-card">
            <div>
              <label >Dataset Name:</label>
              <div class="graph_name" >  {{graphinfo.graphname}}  
              </div>
            </div>
            <div >
              <label > Background Story:</label> 
              <div class="graph_background" v-if="background == 1" >{{graphinfo.background}}</div> 
              <div class="graph_background" v-else-if="background == 0">No Background Story </div>
            </div>
        </el-card>
        <div class="main-container">
          <div class="Sgraph-container"></div>
          
        </div>
        
      </div>
      <div class="control-container">
            <div class="button-container">
              <input type="button" id="Previous" class="bt-button" value="Previous" @click="previous();">
              <input type="button" id="next" class="bt-button" value="Next" @click="next();">
            </div>
          </div>
    </div>
  </div>
</template>

<script>
import * as d3 from "d3"
import axios from '../assets/js/http'
import { mapGetters } from 'vuex'
export default {
  name: 'Test',
  props: {
  },
  data() {
    return {
      images: [],
      current: 0,
      percentage: 0,
      testNum: 10,
      graphinfo: '',
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
      this.getBcakground();
    })
  },
  methods: {
    initImages() {
      if(this.msg == 'formal'){
        this.images = [
          'got.svg',//权力的游戏网络
          'quakers.svg',  //贵格会网络
          'football.svg', //美国大学生橄榄球网络
          'karate.svg', //空手道俱乐部网络
          'plo.svg', //美国政治书籍网络
          'high.svg', // 德国男校网络
          'TI.svg', //TI棒球队网络
          'strike.svg',   //锯木厂工人网络
          'polactor.svg',  //政治人物网络
          'dol.svg' //海豚网络
        ]
      }else if( this.msg == 'train'){
        this.testNum = 1
        this.images = [
          'kan.svg',//好莱坞电影音乐网络
        ]
      }
      
    },
    setContainerSize() {
      let screenWidth = document.documentElement.clientWidth ||  document.body.clientWidth;
      let screenHeight = document.documentElement.clientHeight || document.body.clientHeight;
      //document.querySelector(".graph-container").style.height = screenHeight * 0.68 + "px";
      //document.querySelector(".box-card").style.height = screenHeight * 0.68 + "px";
    },
    getSize() {
      let parentNode = document.querySelector(".Sgraph-container");
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
      return arr;
    },
    loadSvg() {
      let _this = this;
      this.getSize();
      d3.xml(_this.imagePath).then(function(xml) {
        document.querySelector(".Sgraph-container").appendChild(xml.documentElement);
        _this.svg = d3.select(".Sgraph-container svg");
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
      d3.select(".Sgraph-container").selectAll("svg").remove();
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
          this.$confirm('你已阅读完所有数据集的信息, 是否开始实验三?', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(() => {
            setTimeout(() => {
              if( this.msg == 'formal'){
                this.$router.push({ name: 'Test3', params: { msg: 'formal' }});
              }else if( this.msg == 'train'){
                this.$router.push({ name: 'Test3', params: { msg: 'train' }});
              }
            }, 1000)
          }).catch(() => {
                     
          });
            
            return;
        } else {
            this.current += 1;
            this.graphinfo = "";
            d3.select(".Sgraph-container").selectAll("svg").remove();
            
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
    ...mapGetters(["background"])
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
@import '../assets/css/common.css';
.body {
  width: 100%;
}
.content {
  width: 100%;
}
.progress-container {
  text-align: center;
}

.main-container{
  width: 60%;
  float: right;
}
.Sgraph-container {
  height: 600px;
  margin-top: 30px;
  margin-right: 3%;
  border: 0.5px solid #ccc;
  position: relative;
}
.graphselect{
  width: 100%; 
  height: 100%;
}
.Sgraph-container >>> .selected {
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
  width: 460px;
  height: 600px;
  margin-top: 30px;
  font-size: 20px;
}
.background-container{
  width: 30%;
}
#tooltip {
    position: fixed;
    width: 100px;
      height: auto;
      padding: 10px;
      background-color: #ccc;
      opacity: 0.8;
      -webkit-border-radius: 10px;
      -moz-border-radius: 10px;
      border-radius: 10px;
      border:1px solid #fff;
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
	font-size: 20px;
	line-height: 20px;
}

.graph_name{
 font-family: 'Times New Roman', Times, serif;
 text-indent: 1em;
 margin:10px 0;
}
.graph_background{
  height:480px;
  line-height: 2;
  text-indent: 1em;
  text-align: left;
  font-family: 'Times New Roman', Times, serif;
  font-size: 16px;
  WORD-WRAP: break-word;
  TABLE-LAYOUT: fixed;
  word-break: break-all;
  overflow-y:auto;
} 
.box-card /deep/ .el-card__body{
  height: 100%;
}
</style>
