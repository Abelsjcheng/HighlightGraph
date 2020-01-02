<template>
  <div class="body">
    <div id="tooltip" class="hidden">
        <p><strong>ID:</strong><strong id="value">100 </strong></p>
    </div>
    <el-drawer :visible.sync="drawer" direction="btt" :close-on-press-escape="drawerclose.esc" :show-close="drawerclose.close"  size="100%">
      <div class="background-container">
      <p class="background-title" > {{graphinfo.graphname}}</p>
      <p class="background-content" >{{graphinfo.background}}</p>
      </div>
    </el-drawer>
    <el-container style="height:100%">
      <el-aside  width="250px">
        <div class="control-head">Control Plane </div>
        <div class="aside-main">
        <div class="control-container">
          <span class="control-name"> Datasets</span>
          <div class="control-main">
            <label :id="'graph'+index" v-for="(graphname,index) in images" v-bind:key="index"><input :id="'check'+index" type="checkbox" name="check" style="float:left;visibility:hidden" />{{graphname.image}}</label>
          </div>
        </div>
        <div class="control-container">
          <span class="control-name"> Interactions</span>
          <div class="control-main">
            <div style="margin-top:10px">
              <span style="padding-left:15px;"> Question </span>
              <div class="freeExplore">
                <input type="button" id="next" class="bt-button" value="Next" @click="nextquestion();">
              </div>
            </div>
            <div style="margin-top:10px">
              <span style="padding-left:15px;"> Switch </span>
              <div class="freeExplore">
                <input type="button" id="next" class="bt-button" value="Next" @click="next();">
              </div>
            </div>
          </div>
        </div>
        <div class="control-container">
          <span class="control-name"> Timer</span>
          <div class="control-main">
            <div style="margin-top:10px">
              <div class="freeExplore">
                <button id="TimeStart" class="bt-button" @click="TimeStart();">Start</button>
              </div>
            </div>
          </div>
        </div>
        </div>
      </el-aside>
      <el-container>
        <el-main>
          <div class="graph-header">
              <span style="width:142px">graph_id:{{image_id}}</span>
              <span>{{question}} </span>
              <span style="width:142px">{{quescurrent}}/{{questions.length}}</span>
          </div>
          <div class="graph-container"></div>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import * as d3 from "d3"
import axios from '../assets/js/http'
import { mapGetters } from 'vuex'
export default {
  name: 'Test2',
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
      rectangleInfo: [],
      testNum: 7,
      frameflag: false,
      SelectedData: [],
      Timerflag: 0,
      questions: [],
      question: '',
      quescurrent: 0,
      drawer: false,
      graphinfo: '',
      drawerclose:{ 'esc':false,'close':false},
      image_id: 0
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.setContainerSize();
      this.initImages();
      this.getQuestions();
      if(this.background == 1){
        this.getBcakground();
      }
      this.$nextTick(() => {
        document.getElementById("graph"+this.current).style.cssText="color:#000;font-weight: bold;"
        document.getElementById("check"+this.current).checked=true
        document.getElementById("check"+this.current).style.visibility="visible"
      })
    })
  },
  methods: {
    initImages() {
      this.images = this.imagelist
      this.image_id = this.images[this.current].id
    },
    setContainerSize() {
      let screenWidth = document.documentElement.clientWidth ||  document.body.clientWidth;
      let screenHeight = document.documentElement.clientHeight || document.body.clientHeight;
      document.querySelector(".graph-container").style.height = screenHeight * 0.8 + "px";
      document.querySelector(".body").style.height = screenHeight + "px";
      document.querySelector(".aside-main").style.height = screenHeight-64 + "px";
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
    getQuestions() {
      axios.post("/getQuestions/", {
        name: this.imageName,
        background: 1,
        TestType: 2
      }).then(response => {
        let responseData = response.data
        this.questions = responseData.datum
        this.question = this.questions[this.quescurrent].content
        this.quescurrent++
      })
    },
    getBcakground() {
      axios.post("/getBackground/", {
        name: this.imageName
      }).then(response => {
        let responseData = response.data
        this.graphinfo = responseData.datum[0]
        this.drawer = true;
        setTimeout(() => {
          this.drawer=false;
        }, 10000);
      })
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
        d3.select("#select").style("border-color","#c6e2ff").style("background-color","#ccc")
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
              circle.classed("selected", true);
              d3.select("#tooltip")
              .style("left", (d3.event.pageX)+"px")
              .style("top", (d3.event.pageY+20)+"px")
              .select("#value")
              .text(index);
              d3.select("#tooltip").classed("hidden", false);
            }).on('mouseout',function(d){
              circle.classed("selected", false);
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
          let selectcircles =0
          d3.selectAll("circle").nodes().forEach(function(d,index) {
            let circle = d3.select(d);
            let x = parseFloat(circle.attr("cx"));
            let y = parseFloat(circle.attr("cy"));
            
            if(x > s[0][0] && x < s[1][0] && y > s[0][1] && y < s[1][1]) {
              selectcircles ++;
              circle.classed("selected", true);
            }
          })
          _this.SelectedData.push(selectcircles)
        }
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
      this.SelectedData.pop();
      if(this.frameflag == true)
      this.drawRectangle();
    },
    submit() {
      if(this.rectangleInfo.length > 0){
        this.rectangleInfo.forEach(d => {
          axios.post("/saveRect/", {
            time: d.time,
            name: d.name,
            x1: d.x1,
            y1: d.y1,
            x2: d.x2,
            y2: d.y2
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
      }else{
        this.$message({
          message: '请框选出你对图中感兴趣的部分',
          type: 'warning'
        });
      }
    },
    nextquestion() { //下一题
      if(this.Timerflag == 0){
        this.$message({
          message: '同学你还未开始计时做答',
          type: 'warning',
          duration: 1000
        });
        return;
      }else if(this.quescurrent >= this.questions.length){
        this.$message({
          message: '你已完成所有任务，请点击Submit进入下一个实验',
          type: 'success',
          duration: 1000
        });
      }else{
        this.addTime();
        this.question ='';
        this.Timerflag = 0;
        setTimeout(() => {
          this.question = this.questions[this.quescurrent].content
          this.quescurrent++
        }, 2000)
      }
    },
    next() {
      if(this.Timerflag == 0){
        this.$message({
          message: '同学你还未开始计时做答',
          type: 'warning',
          duration: 1000
        });
        return;
      }else if(this.quescurrent < this.questions.length){
        this.$message({
          message: '同学你还未完成本数据集的所有问题',
          type: 'warning',
          duration: 1000
        });
        return;
      }
      this.addTime();
      this.rectangleInfo = [];
      document.getElementById("graph"+this.current).style.cssText="color:#000;font-weight: 400"
      document.getElementById("check"+this.current).checked=false
      document.getElementById("check"+this.current).style.visibility="hidden"
      if(this.current >= this.testNum-1) {
        setTimeout(() => {
          this.$router.push({ name: 'home', params: { msg: 'study' }});
        }, 1000)
        return;
      } else {
        this.current += 1
        if(this.background == 1)
        this.getBcakground();
        this.frameflag = false
        this.Timerflag = 0
        this.quescurrent = 0
        d3.select("#select").style("border-color","#DCDFE6").style("background-color","#fff")
        d3.select(".graph-container").selectAll("svg").remove();
        document.getElementById("graph"+this.current).style.cssText="color:#000;font-weight: bold;"
        document.getElementById("check"+this.current).checked=true
        document.getElementById("check"+this.current).style.visibility="visible"
        this.image_id = this.images[this.current].id
        this.getQuestions();
      }
    },
    TimeStart() {
      if(this.Timerflag == 1){
        this.$message({
          message: '同学你已开始计时做答',
          type: 'warning',
          duration: 1000
        });
        return;
      }
      if(this.quescurrent == 1)
      this.loadSvg();
      this.$message({
          message: '计时开始',
          type: 'success',
          duration: 1000
        });
      document.getElementById("TimeStart").style.cssText="background-color:#ccc";
      this.Timerflag=1
    },
    addTime() {
      clearInterval(this.interval);
      let timeFormat = d3.timeFormat("%Y-%m-%d %H:%M:%S");
      axios.post("/saveDuration/", {
        time: timeFormat(new Date()),
        name: this.imageName,
        consumingtime: this.second,
        qid: this.questions[this.quescurrent-1].qid,
        TestType: 2
      }).then(response => {
            
      })
      this.Timerflag=2
      document.getElementById("TimeStart").style.cssText="background-color:#fff";
    }
    
  },
  computed: {
    imagePath: function() {
      return "/static/images/lab12/" + this.images[this.current].image+".svg";
    },
    imageName: function() {
      let arr = this.imagePath.split("/");
      return arr[arr.length-1];
    },
    ...mapGetters(["imagelist"]),
    ...mapGetters(["background"])
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
}
.control-head{
  background-color: #b4b4b4;
  color:#FFF;
  height: 60px;
  font-size: 24px;
  line-height: 60px;
  text-align: center;
}
.el-aside {
  overflow-x: hidden;
  border-right: 2px solid #ccc;
}
.aside-main{
  justify-content: space-around;
  display: flex;
  flex-direction: column;
}


.control-name{
  display: block;
  margin: 0px 10px;
  border-bottom: 1.5px solid #ccc;;
  -webkit-box-sizing: border-box;
  box-sizing: border-box;
  font-size:20px;
  font-weight: 500;
  
}

.control-main label{
  display: block;
  margin:3px 25px;
  font-size: 15px;
}

.selected-data{
  padding: 2px 15px;
  word-wrap: break-word;
  word-break: break-all;
  overflow: hidden;
}

.el-main {
  color: #333;
  text-align: center;
}

.progress-container {
  text-align: center;
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
  width: 90%;
  height: 720px;
  margin: 1% auto;
  border: 0.5px solid #ccc;
  position: relative;
}


#tooltip {
    position: absolute;
  width: 100px;
	height: auto;
	padding: 10px;
	background-color: #b4b4b4;
    color: #fff;
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

#tooltip p  {
	margin: 0;
	font-family: sans-serif;
	font-size: 16px;
	line-height: 20px;
}
.freeExplore{
  margin-top: 10px;
  display: flex;
  justify-content: space-around;
}


.bt-button{
  display: inline-block;
  width: 65px;
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
    border-color: #b4b4b4;
    outline: 0;
}

.background-container{
  width: 700px;
  margin: 0 auto;
}
.background-title{
  font-size:30px;
  font-weight:bold;
  text-align:center;
}
.background-content{
  margin-top: 2%;
  font-size: 20px;
  line-height: 2;
  text-indent: 2em;WORD-WRAP: break-word;
  TABLE-LAYOUT: fixed;
  word-break: break-all;
}
</style>
