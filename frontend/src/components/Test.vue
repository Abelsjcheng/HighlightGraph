<template>
  <div class="body">
    <div id="tooltip" class="hidden">
        <p><strong>ID: </strong><strong id="value">100 </strong></p>
    </div>
    <el-container >
      <el-aside width="250px">
        <div class="control-head">Control Panel </div>
        <div class="aside-main">
        <div class="control-container">
          <span class="control-name"> Datasets</span>
          <div class="control-main" v-if="background ==1" >
            <label :id="'graph'+index" v-for="(graphname,index) in images" v-bind:key="index"><input :id="'check'+index" type="checkbox" name="check" style="float:left;visibility:hidden" />{{graphname.image}}</label>
          </div>
          <div class="control-main" v-if="background ==0" >
            <label :id="'graph'+index" v-for="(graphname,index) in images" v-bind:key="index"><input :id="'check'+index" type="checkbox" name="check" style="float:left;visibility:hidden" />Graph_Id: {{graphname.id}}</label>
          </div>
        </div>
        <div class="control-container">
          <span class="control-name"> Interactions</span>
          <div class="control-main">
            <div style="margin-top:10px">
              <span style="padding-left:15px;">Graph Exploration </span>
              <div class="freeExplore">
                <button id="select" class="bt-button" @click="Frame();"> Select</button>
                <button  id="redo" class="bt-button" @click="redo();">Redo</button >
              </div>
            </div>
            <div style="margin-top:10px">
              <span style="padding-left:15px;">Dataset Switch </span>
              <div class="freeExplore">
                <input type="button" id="next" class="bt-button" value="Next" @click="next();">
              </div>
            </div>
          </div>
        </div>
        <div class="control-container">
          <span class="control-name">Selected Data Items</span>
          <div class="control-main">
            <div style="margin-top:10px">
                <div v-if="SelectedData.length > 0">
                  <div class="selected-data"  v-for="(data,index) in SelectedData" v-bind:key="index" > Selected Data_sum: {{data}} </div>
                </div>
                <div style="text-align:center" v-else> No selected data</div>
            </div>
          </div>
        </div>
        </div>
      </el-aside>
      <el-container>
        <el-main>
          <div class="graph-header">
              <span>{{questionname}} </span>
          </div>
          <div class="graph-main">
            <div class="graph-container">
              <div class="background-container" v-show="drawer">
                <p class="background-title" > {{graphinfo.graphname}}</p>
                <p class="background-content" >{{graphinfo.background}}</p>
                <div style="position: absolute;bottom:0;width:100%;text-align: center;" ><input type="button" id="Skip" class="bt-button" value="Skip" @click="Skip();"></div>
              </div>
            </div>
          </div>
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
      rectangleInfo: [],
      testNum: 10,
      frameflag: false,
      SelectedData:[],
      drawer: false,
      graphinfo: '',
      drawerclose:{ 'esc':false,'close':false},
      questionname: '请找出你对图中感兴趣的部分', //
      closeback: null,
      msg: ''
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.msg = this.$route.params.msg;
      //this.setContainerSize();
      this.initImages();
      this.shuffle(this.images);
      if(this.background == 1){
        this.getBcakground();
      }else{
        this.loadSvg();
      }
      this.$nextTick(() => {
        document.getElementById("graph"+this.current).style.cssText="color:#000;font-weight: 700"
        document.getElementById("check"+this.current).checked=true
        document.getElementById("check"+this.current).style.visibility="visible"
      })
    })
  },
  methods: {
    initImages() {
      if( this.msg == 'formal'){
        this.images = [
          { 'id':1,'image':'got'}, //权力的游戏网络
          { 'id':2,'image':'quakers'}, //贵格会网络
          { 'id':3,'image':'football'}, //美国大学生橄榄球网络
          { 'id':4,'image':'karate'}, //空手道俱乐部网络
          { 'id':5,'image':'plo'}, //美国政治书籍网络
          { 'id':6,'image':'high'}, // 德国男校网络
          { 'id':7,'image':'TI'}, //TI棒球队网络
          { 'id':8,'image':'strike'}, //锯木厂工人网络
          { 'id':9,'image':'polactor'}, //政治人物网络
          { 'id':10,'image':'dol'} //海豚网络
        ]
      }else if( this.msg == 'train'){
        this.testNum = 1
        this.images = [
          { 'id':1,'image':'kan'}, //权力的游戏网络
        ]
      }
      
    },
    setContainerSize() {
      let screenWidth = document.documentElement.clientWidth ||  document.body.clientWidth;
      let screenHeight = document.documentElement.clientHeight || document.body.clientHeight;
      //document.querySelector(".graph-main").style.height = screenHeight -66 + "px";
      //document.querySelector(".graph-main").style.height = 687 + "px";
      //document.querySelector(".graph-container").style.height = (screenHeight -66) *0.9 + "px";
      //document.querySelector(".body").style.height = screenHeight + "px";
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
      this.$store.commit("setImagelist",arr);
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
        //let scaleNumber = 2
        console.log(scaleNumber)
        _this.svgWidth = svgWidth * scaleNumber;
        _this.svgHeight = svgHeight * scaleNumber;
        _this.svg.attr("width", _this.svgWidth)
        .attr("height", _this.svgHeight)
        .style("position", "absolute")
        .style("left", (_this.width - _this.svgWidth) / 2 + "px")
        .style("top", (_this.height - _this.svgHeight) / 2 + "px");
        _this.initInterval();
        _this.tooltip();
        _this.Frame();
        //_this.drawRectangle();
      });
    },
    getBcakground() {
      this.questionname="请先阅读背景信息 (限时10秒)"
      axios.post("/getBackground/", {
        name: this.imageName
      }).then(response => {
        let responseData = response.data
        this.graphinfo = responseData.datum[0]
        this.drawer = true;
        this.closeback = setTimeout(() => {
          this.drawer=false;
          this.questionname="请找出你对图中感兴趣的部分"
          this.loadSvg()
        }, 4000);
      })
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
        .style("stroke-opacity", "0")
        .call(d3.brush().on("end", brushended));

      this.svg.append("g")
        .attr("class", "rectangles");

      let _this = this;
      function brushended() {
        var s = d3.event.selection;
        let timeFormat = d3.timeFormat("%Y-%m-%d %H:%M:%S");
        if(s) {
          d3.select("g.rectangles").append("rect")
          .attr("x", s[0][0])
          .attr("y", s[0][1])
          .attr("width", s[1][0] - s[0][0])
          .attr("height", s[1][1] - s[0][1])
          .style("fill", "#777")
          .style("fill-opacity", 0.3)
          .style("stroke-opacity", "0");

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
            } 
            // else {
            //   this.$message({
            //     message: '提交成功',
            //     type: 'success',
            //     duration: 2000
            //   });
            // }
          })
        })
      }
      
    },
    next() {
      if(this.rectangleInfo.length == 0 ){
        this.$message({
          message: '请框选出你对图中感兴趣的部分',
          type: 'warning',
          duration: 1000
        });
        return;
      }
      clearInterval(this.interval);
      this.submit();
      this.addTime();
      if(this.current >= this.testNum-1) {
        setTimeout(() => {
          if( this.msg == 'formal'){
            this.$router.push({ name: 'experiment', params: { msg: 'test' }});
          }else if( this.msg == 'train'){
            this.$router.push({ name: 'train', params: { msg: 'test' }});
          }
        }, 1000)
        return;
      } else {
        this.rectangleInfo = [];
        this.SelectedData = [];
        document.getElementById("graph"+this.current).style.cssText="color:#000;font-weight: 400"
        document.getElementById("check"+this.current).checked=false
        document.getElementById("check"+this.current).style.visibility="hidden"
        this.current += 1
        this.frameflag = false
        d3.select("#select").style("border-color","#DCDFE6").style("background-color","#fff")
        d3.select(".graph-container").selectAll("svg").remove();
        document.getElementById("graph"+this.current).style.cssText="color:#000;font-weight: 700"
        document.getElementById("check"+this.current).checked=true
        document.getElementById("check"+this.current).style.visibility="visible"
        if(this.background == 1)
        this.getBcakground();
        else{
          this.loadSvg();
        }
      }
    },
    addTime() {
      let timeFormat = d3.timeFormat("%Y-%m-%d %H:%M:%S");
      axios.post("/saveDuration/", {
        time: timeFormat(new Date()),
        name: this.imageName,
        consumingtime: this.second,
        qid: '',
        TestType: 1
      }).then(response => {
            
      })
    },
    Skip(){
      clearTimeout(this.closeback);
      this.drawer=false;
      this.questionname="请找出你对图中感兴趣的部分"
      this.loadSvg();
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
    ...mapGetters(["background"])
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
@import '../assets/css/common.css';


.el-main {
  padding: 0px 20px;
}
.graph-header{
  text-align: center;
  border-bottom: 2px solid #ccc;
  height: 59px;
  line-height: 59px;
  font-size: 1.5em;
  font-weight: bold;
}

.graph-container >>> .selected {
    fill: red;
}


</style>
