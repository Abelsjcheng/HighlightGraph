<template>
  <div class="body">
    <el-container style="height:100%">
      <el-aside width="250px">
        <div class="control-head">Control Plane </div>
        <div class="control-container">
          <span class="control-name"> Datasets</span>
          <div class="control-main">
              <p :id="'graph'+index" v-for="(imagename,index) in images" v-bind:key="index">{{imagename}} </p>
          </div>
        </div>
        <div class="control-container">
          <span class="control-name"> Question {{quescurrent}}/{{questions.length}}</span>
          <div class="control-main">
            <div style="margin-top:10px;text-align:center">
              <span > {{question}}</span>
              <div class="freeExplore">
                <input type="button" id="next" class="bt-button" value="Next" @click="nextquestion();">
              </div>
            </div>
          </div>
        </div>
        <div class="control-container">
          <span class="control-name"> Interactions</span>
          <div class="control-main">
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
                <button id="TimeStop" class="bt-button" @click="TimeStop();">Stop</button >
                <p>{{second}} </p>
              </div>
            </div>
          </div>
        </div>
      </el-aside>
      <el-container>
        <el-main>
          <div class="graph-container">
            <div class="questionType1" v-show="questionType == 1">
              <div class="graph-block"  v-for="(n,index) in 6" v-bind:key="index">
                <div :id="'graph-block'+index" style="height:100%"> </div>
                <span class="selectradio" >图片{{n}}</span>
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
      testNum: 2,
      SelectedData:[],
      Timerflag:0,
      imageschiose: '',
      graphs:[],
      question: '',
      questions: [],
      questionType: 0, //问题类型
      quescurrent: 1
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.setContainerSize();
      this.initImages();
      this.getQuestions();
      this.$nextTick(() => {
        document.getElementById("graph"+this.current).style.cssText="color:#409EFF;font-weight: 700"
      }) 
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
      document.querySelector(".body").style.height = screenHeight + "px";
      document.querySelector(".graph-container").style.height = screenHeight * 0.8 + "px";
      document.querySelector(".graph-block").style.height = document.querySelector(".graph-container").style.height/3;
      
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
    loadSvg(imagepath,index) {
      let _this = this;
      let graphblock = document.querySelector(".graph-block");
      let width = graphblock.clientWidth;
      let height = graphblock.clientHeight;
      d3.xml(imagepath).then(function(xml) {
        document.querySelector("#graph-block"+index).appendChild(xml.documentElement);
        _this.svg = d3.select("#graph-block"+index+" svg");
        let svgWidth = _this.svg.attr("width");
        let svgHeight = _this.svg.attr("height");
        let scaleNumber = d3.min([(width) / svgWidth, (height) / svgHeight]);
        _this.svgWidth = svgWidth * scaleNumber;
        _this.svgHeight = svgHeight * scaleNumber;
        _this.svg.attr("width", _this.svgWidth)
        .attr("height", _this.svgHeight)
        .style("position", "absolute")
        .style("left", (width - _this.svgWidth) / 2 + "px")
        .style("top", (height - _this.svgHeight) / 2 + "px");
      });
    },
    loadBigSvg(imagepath) {
      let _this = this;
      this.getSize();
      d3.xml(imagepath).then(function(xml) {
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
      });
    },
    next() {
      if(this.Timerflag == 0){
        this.$message({
          message: '同学你还未开始计时做答',
          type: 'warning'
        });
        return;
      }else if(this.Timerflag == 1){
        this.$message({
          message: '同学你还未停止计时做答',
          type: 'warning'
        });
        return;
      }else if(this.quescurrent < this.questions.length){
        this.$message({
          message: '同学你还未完成本数据集的所有问题',
          type: 'warning'
        });
        return;
      }
      if(this.current >= this.testNum-1) {
        setTimeout(() => {
          this.$router.push({ name: 'home', params: { msg: 'expertment' }});
        }, 1000)
        return;
      } 
      document.getElementById("graph"+this.current).style.cssText="color:#000;font-weight: 400"
      this.current += 1
      this.Timerflag = 0;
      this.quescurrent = 1;
      this.question = "";
      d3.select("#select").style("border-color","#DCDFE6").style("background-color","#fff")
      d3.select(".graph-container").selectAll("svg").remove();
      document.getElementById("graph"+this.current).style.cssText="color:#409EFF;font-weight: 700"
      setTimeout(() => {
        this.getQuestions();
      }, 2000)
      
    },
    TimeStart() {
      if(this.Timerflag == 1){
        this.$message({
          message: '同学你已开始计时做答',
          type: 'warning'
        });
        return;
      }
      if(this.Timerflag == 2){
        this.$message({
          message: '同学你已完成本次做答',
          type: 'warning'
        });
        return;
      }
      this.questionType=this.questions[this.quescurrent-1].type
      this.$nextTick(() => {
        this.loadQuestion();
      }) 
      this.$message({
          message: '计时开始',
          type: 'success'
        });
      document.getElementById("TimeStart").style.cssText="background-color:#ecf5ff";
      this.Timerflag=1
    },
    TimeStop() {
      if(this.Timerflag != 1){
        this.$message({
          message: '同学你还未开始计时做答',
          type: 'warning'
        });
        return;
      }
      clearInterval(this.interval);
      this.$message({
          message: '停止计时',
          type: 'success'
        });
      let timeFormat = d3.timeFormat("%Y-%m-%d %H:%M:%S");
      axios.post("/saveDuration/", {
        time: timeFormat(new Date()),
        name: this.imageName,
        consumingtime: this.second,
        qid: this.questions[this.quescurrent-1].qid,
        TestType: 1
      }).then(response => {
            
      })
      this.Timerflag = 2;
      this.questionType = 0;
      document.getElementById("TimeStart").style.cssText="background-color:#fff";
    },
    getQuestions() {
      axios.post("/getQuestions/", {
        name: this.imageName,
        background: 1,
        TestType: 3
      }).then(response => {
        let responseData = response.data
        this.questions = responseData.datum
        this.question = this.questions[this.quescurrent-1].content
      })
    },
    loadQuestion() {  
      if(this.questionType == 1 ){
        this.imageschiose=this.questions[this.quescurrent-1].choices;
        for(let i=0;i<this.imagesmhs.length;i++){
          this.loadSvg("/static/images/lab3/"+this.imagesmhs[i],i)
        }
      }else{
        this.loadBigSvg("static/images/lab3/"+this.questions[this.quescurrent-1].questionImg)
      }
      this.initInterval();
      
    },
    nextquestion() { //下一题
      if(this.Timerflag == 0){
        this.$message({
          message: '同学你还未开始计时做答',
          type: 'warning'
        });
        return;
      }else if(this.Timerflag == 1){
        this.$message({
          message: '同学你还未停止计时做答',
          type: 'warning'
        });
        return;
      }else if(this.quescurrent >= this.questions.length){
        this.$message({
          message: '你已完成所有任务，请点击Submit进入下一个实验',
          type: 'success'
        });
      }else{
        this.questionType = 0;
        this.question ='';
        this.Timerflag = 0;
        d3.select(".graph-container").selectAll("svg").remove();
        setTimeout(() => {
          this.question = this.questions[this.quescurrent].content
          this.quescurrent++
        }, 2000)
      }
    },
  },
  computed: {
    imagePath: function() {
      return "/static/images/lab3/" + this.images[this.current];
    },
    imageName: function() {
      let arr = this.imagePath.split("/");
      return arr[arr.length-1];
    },
    imagesmhs:function() {
        let img=this.imageschiose.split(";");
        return img;
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
.control-head{
  background-color: #ccc;
  color:#FFF;
  height: 60px;
  font-size: 24px;
  line-height: 60px;
  text-align: center;
}
.el-aside {
    overflow-x: hidden;
  }
.control-container{
  margin: 3% 0;
}
.control-name{
  display: block;
  padding: 10px 15px;
  border-bottom: 1.5px solid #EBEEF5;
  -webkit-box-sizing: border-box;
  box-sizing: border-box;
  font-size:20px;
  font-weight: 500;
}  
.control-main p{
  margin:3px 40px;
  font-size: 14px;
  font-weight: 400;
}
.selected-data{
  padding: 2px 15px;
  word-wrap: break-word;
  word-break: break-all;
  overflow: hidden;
}
  .el-main {
    background-color: #E9EEF3;
    color: #333;
    text-align: center;
  }
.progress-container {
  text-align: center;
}

.graph-container {
  width: 90%;
  height: 720px;
  margin: 3% auto;
  border: 1px solid black;
  position: relative;
}

.questionType1{
  display: -webkit-flex;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-around;
  width:100%;
  height:100%;
}
.graph-block{
  position: relative;
  border: 1px solid black;
  height: 40%;
  width: 30%;
}
.selectradio{
  display: block;
  margin-top:5px;
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
    border-color: #3a8ee6;
    outline: 0;
}
</style>
