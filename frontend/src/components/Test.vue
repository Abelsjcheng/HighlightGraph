<template>
  <div class="body">
    <div class="content">
      <div class="progress-container">
        <el-progress :percentage="percent"></el-progress>
      </div>
      <p id="second">计时器:{{second}} S</p>
      <div id="tooltip" class="hidden">
        <p><strong>编号</strong></p>
        <p><span id="value">100 </span></p>
      </div>
      <div style="display: flex;justify-content: center;">
        <div class="freeExplore">
          <p style="text-align: center;font-size:24px">自由探索 </p>
          <button id="select" class="bt-button" @click="Frame();"> <img src="/static/font/Select.svg"/></button>
          <button  id="redo" class="bt-button" @click="redo();">Redo</button >
          <p style="text-align: center;"> <button style="height:60px" class="bt-button" @click="submit();">submit</button></p>
        </div>
        <div style="width: 80%;">
          <div class="graph-container"></div>
          <div class="control-container">
            <div class="button-container">
              
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
      width: null,
      height: null,
      svg: null,
      svgWidth: null,
      svgHeight: null,
      second: 0,
      interval: null,
      percentage: 0,
      rectangleInfo: [],
      testNum: 7,
      frameflag: false
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.setContainerSize();
      this.initImages();
      //this.shuffle(this.images);
      this.loadSvg();
    })
  },
  methods: {
    initImages() {
      this.images = [
        'got.svg', // 权力的游戏网络
        'quakers.svg', // 贵格会网络
        'football.svg', // 美国大学生橄榄球网络
        'karate.svg', // 空手道俱乐部网络
        'les.svg', // 悲惨世界网络
        // 德国男校网络
        // TI棒球队网络
        // SA棒球队络 
        'strike.svg', // 锯木厂工人网络
        'PolActor.svg' // 政治人物网络
        ]
    },
    setContainerSize() {
      let screenWidth = document.documentElement.clientWidth ||  document.body.clientWidth;
      let screenHeight = document.documentElement.clientHeight || document.body.clientHeight;
      document.querySelector(".graph-container").style.height = screenHeight * 0.68 + "px";
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
        document.querySelector("#second").style.visibility="visible";
        document.querySelector("#redo").removeAttribute("disabled");
        document.querySelector("#next").removeAttribute("disabled");
        _this.tooltip();
        //_this.drawRectangle();
        
      });
    },
    Frame() {
      this.frameflag = !this.frameflag
      if(this.frameflag == false){
        d3.select("#select").style("border-color","#DCDFE6").style("background-color","#fff")
        d3.select(".graph-container .brush").remove();
      }else{
        d3.select("#select").style("border-color","#c6e2ff").style("background-color","#ecf5ff")
        this.drawRectangle();
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
    drawRectangle() {
      /**
       * 框选数据
       */
      this.svg.append("g")
        .attr("class", "brush")
        .call(d3.brush().on("end", brushended));

      this.svg.append("g")
        .attr("class", "rectangles");

      let _this = this;
      function brushended() {
        var s = d3.event.selection;
        let timeFormat = d3.timeFormat("%Y-%m-%d %H:%M:%S");
        console.log(s)
        if(s) {
          d3.select("g.rectangles").append("rect")
          .attr("x", s[0][0])
          .attr("y", s[0][1])
          .attr("width", s[1][0] - s[0][0])
          .attr("height", s[1][1] - s[0][1])
          .style("fill", "#777")
          .style("fill-opacity", 0.3)
          .style("stroke", "#fff");

          _this.rectangleInfo.push({
            name: _this.imageName,
            time: timeFormat(new Date()),
            x1: s[0][0],
            y1: s[0][1],
            x2: s[1][0],
            y2: s[1][1]
          })

          d3.selectAll("circle").nodes().forEach(d => {
            let circle = d3.select(d);
            let x = parseFloat(circle.attr("cx"));
            let y = parseFloat(circle.attr("cy"));
            
            if(x > s[0][0] && x < s[1][0] && y > s[0][1] && y < s[1][1]) {
              circle.classed("selected", true);
            }
          })
        }
      }
    },
    submit() {
      this.rectangleInfo.forEach(d => {
        axios.post("/saveanswer/", {
          time: d.time,
          name: d.name,
          x1: d.x1,
          y1: d.y1,
          x2: d.x2,
          y2: d.y2,
          qid: '1.5.1',
          answer: '',
          consumingtime: this.second.toFixed(1),
          TestType: 1
        }).then(response => {
          let responseData = response.data;
          if(responseData.state == 'fail') {
            this.$message.error('提交失败');
          } else {
            this.$message({
              message: '提交成功',
               type: 'success'
            });
          }
        })
      })
    },
    next() {
      this.rectangleInfo = [];
      clearInterval(this.interval);
      this.percentage += (100 / this.testNum);
      if (this.percentage > 100) {
        this.percentage = 100;
      }
      if(this.current >= this.testNum-1) {
        setTimeout(() => {
          this.$router.push({ name: 'home', params: { msg: 'test' }});
        }, 1000)
        return;
      } else {
        this.current += 1;
        this.frameflag = false
        d3.select("#select").style("border-color","#DCDFE6").style("background-color","#fff")
        d3.select(".graph-container").selectAll("svg").remove();
        document.querySelector("#second").style.visibility = "hidden";
        document.querySelector("#redo").disabled = "disabled"
        document.querySelector("#next").disabled = "disabled"
        setTimeout(() => {
          this.loadSvg();
        }, 2000)
      }
    },
    redo() {
      let rects = d3.select(".graph-container .rectangles").selectAll("rect").nodes();
      d3.select(rects[rects.length - 1]).remove();
      d3.select(".graph-container .brush").remove();
      if(this.rectangleInfo.length > 0) {
        let rectangle = this.rectangleInfo[this.rectangleInfo.length-1];
        this.rectangleInfo.splice(this.rectangleInfo.length-1, 1);
        d3.selectAll("circle").nodes().forEach(d => {
          let circle = d3.select(d);
          let x = parseFloat(circle.attr("cx"));
          let y = parseFloat(circle.attr("cy"));
          if(x > rectangle.x1 && x < rectangle.x2 && y > rectangle.y1 && y < rectangle.y2) {
            circle.classed("selected", false);
          }
        })
      }
      if(this.frameflag == true)
      this.drawRectangle();
    }
  },
  computed: {
    imagePath: function() {
      return "/static/images/" + this.images[this.current];
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
  left: 4%;
  top: 12%;
  font-size: 30px;
  font-weight: bold;
  color: #ccc;
}
.graph-container {
  width: 90%;
  height: 720px;
  margin: 3% auto;
  border: 1px solid black;
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
.freeExplore{
  width: 200px;
  height: 250px;
  margin-top:10%;
  padding: 20px;
  border: 1px solid #DCDFE6;
  
}
#redo{
  height: 60px;
  float: right;
}

.bt-button{
  display: inline-block;
  line-height: 1;
  white-space: nowrap;
  cursor: pointer;
  background: #FFF;
  border: 1px solid #DCDFE6;
  margin: 0;
  text-align: center;
  padding: 12px 20px;
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
