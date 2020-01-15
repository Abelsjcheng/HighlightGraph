<template>
  <div class="body">
    <div id="tooltip" class="hidden">
        <p><strong>ID: </strong><strong id="value">100 </strong></p>
    </div>
    <el-container >
      <el-aside  width="250px">
        <div class="control-head">Control Panel </div>
        <div class="aside-main">
        <div class="control-container">
          <span class="control-name"> Datasets</span>
          <div class="control-main" v-if="background ==1" >
            <label :id="'graph'+index" v-for="(graphname,index) in images" v-bind:key="index"><input :id="'check'+index" type="checkbox" name="check" style="float:left;visibility:hidden" />{{graphname.image}}</label>
          </div>
          <div class="control-main" v-if="background ==0" >
            <label :id="'graph'+index" v-for="(graphname,index) in images" v-bind:key="index"><input :id="'check'+index" type="checkbox" name="check" style="float:left;visibility:hidden" />Graph_ID: {{graphname.id}}</label>
          </div>
        </div>
        <div class="control-container">
          <span class="control-name"> Interactions</span>
          <div class="control-main">
            <div >
              <span style="padding-left:15px;"> Question Switch </span>
              <div class="freeExplore">
                <input type="button" id="next" class="bt-button" value="Next" @click="nextquestion();">
              </div>
            </div>
            <div style="margin-top:10px">
              <span style="padding-left:15px;"> Dataset Switch </span>
              <div class="freeExplore">
                <input type="button" id="next" class="bt-button" value="Next" @click="next();">
              </div>
            </div>
          </div>
        </div>
        </div>
      </el-aside>
      <el-container>
        <el-main>
          <div class="graph-header">
              <span style="width:142px"></span>
              <span>{{question}} </span>
              <span  :style="{ width: '142px', visibility: queshow }"  >{{quescurrent}}/{{questions.length}}</span>
          </div>
          <div class="graph-main">
            <div class="graph-container">
              <div class="background-container" v-show="drawer">
                <p class="background-title" > {{graphinfo.graphname}}</p>
                <p class="background-content" >{{graphinfo.background}}</p>
                <div style="position: absolute;bottom:0;width:100%" ><input type="button" id="Skip" class="bt-button" value="Skip" @click="Skip();"></div>
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
      testNum: 10,
      questions: [],
      question: '',
      quescurrent: 0,
      drawer: false,
      graphinfo: '',
      drawerclose:{ 'esc':false,'close':false},
      closeback: null,
      msg: '',
      queshow: 'hidden'
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.msg = this.$route.params.msg;
      //this.setContainerSize();
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
      if(this.msg == 'train'){
        this.testNum = 1
      }
      this.images = this.imagelist
    },
    setContainerSize() {
      let screenWidth = document.documentElement.clientWidth ||  document.body.clientWidth;
      let screenHeight = document.documentElement.clientHeight || document.body.clientHeight;
      //document.querySelector(".graph-main").style.height = screenHeight -66 + "px";
      //document.querySelector(".graph-main").style.height = 687 + "px";
      //document.querySelector(".graph-container").style.height = 620 + "px";
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
      return arr;
    },
    getQuestions() {
      axios.post("/getQuestions/", {
        name: this.imageName,
        background: this.background,
        TestType: 2
      }).then(response => {
        let responseData = response.data
        this.questions = responseData.datum
        if(this.background == 0){
          this.question = this.questions[this.quescurrent].content
          this.quescurrent++
          this.queshow="visible"
          this.loadSvg()
        }
      })
    },
    getBcakground() {
      this.question="请先阅读背景信息 (限时10秒)"
      axios.post("/getBackground/", {
        name: this.imageName
      }).then(response => {
        let responseData = response.data
        this.graphinfo = responseData.datum[0]
        this.queshow="hidden"
        this.drawer = true;
        this.closeback= setTimeout(() => {
          this.drawer=false;
          this.question = this.questions[this.quescurrent].content
          this.quescurrent++
          this.queshow="visible"
          this.loadSvg();
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
      });
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
    nextquestion() { //下一题
      if(this.quescurrent >= this.questions.length){
        this.$message({
          message: '你已完成所有任务，请点击next进入下一个数据集',
          type: 'success',
          duration: 1000
        });
      }else{
        this.addTime();
        this.question ='';
        setTimeout(() => {
          this.question = this.questions[this.quescurrent].content
          this.quescurrent++
          this.initInterval();
        }, 2000)
      }
    },
    next() {
      if(this.quescurrent < this.questions.length){
        this.$message({
          message: '同学你还未完成本数据集的所有问题',
          type: 'warning',
          duration: 1000
        });
        return;
      }
      this.addTime();
      document.getElementById("graph"+this.current).style.cssText="color:#000;font-weight: 400"
      document.getElementById("check"+this.current).checked=false
      document.getElementById("check"+this.current).style.visibility="hidden"
      if(this.current >= this.testNum-1) {
        setTimeout(() => {
          if( this.msg == 'formal'){
            this.$router.push({ name: 'experiment', params: { msg: 'test2' }});
          }else if( this.msg == 'train'){
            this.$router.push({ name: 'train', params: { msg: 'test2' }});
          }
        }, 1000)
        return;
      } else {
        this.current += 1
        if(this.background == 1)
        this.getBcakground();
        this.quescurrent = 0
        d3.select("#select").style("border-color","#DCDFE6").style("background-color","#fff")
        d3.select(".graph-container").selectAll("svg").remove();
        document.getElementById("graph"+this.current).style.cssText="color:#000;font-weight: bold;"
        document.getElementById("check"+this.current).checked=true
        document.getElementById("check"+this.current).style.visibility="visible"
        this.getQuestions();
      }
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
    },
    Skip(){
      clearTimeout(this.closeback);
      this.drawer=false;
      this.question = this.questions[this.quescurrent].content
      this.quescurrent++
      this.queshow="visible"
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
    ...mapGetters(["imagelist"]),
    ...mapGetters(["background"])
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
@import '../assets/css/common.css';



.el-main {
  color: #333;
  text-align: center;
  padding: 0px 20px;
}

.graph-header{
  display: flex;
  justify-content: space-between;
  border-bottom: 2px solid #ccc;
  height: 59px;
  line-height: 59px;
  font-size: 1.4em;
  font-weight: bold;
}

.graph-container >>> .selected {
    fill: red;
}
</style>
