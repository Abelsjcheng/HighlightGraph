<template>
    <div class="body">
    <div class="content">
      <div class="progress-container">
        <el-progress :percentage="percent"></el-progress>
      </div>
      <div class="main-container">
        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <span>{{questionTypeText}} {{current}}/{{questions.length}}</span>
            <el-button style="float: right;" size="medium" type="primary" @click="nextquestion()">提交</el-button>
          </div>
          <div v-show="questionType == 1">
            <div class="question-title">
              {{question}}  
            </div>
            <el-radio-group v-model="radio">
            <div class="block" v-for="(image,index) in images" :key="index">
               <el-image
                      class="graphselect"
                      :src="image.url[0]"
                      fit="contain"
                      :preview-src-list="image.url"></el-image> 
              <el-radio class="selectradio" :label="image.name">{{image.cname}}</el-radio>
            </div>
            </el-radio-group>
          </div>
          <div v-show="questionType == 2 || questionType == 3">
            <div class="question-title">
              {{question}}  
            </div>
            <div style="text-align: center;margin: 4% 0;">
            <el-image
                      class="graphselect"
                      :src="imageMHPath"
                      fit="contain"
            ></el-image> 
            </div>
            <el-radio-group v-model="radio">
            <el-radio style="display:block;margin-top: 10px;" v-for="(chiose,index) in questionchiose" :key="index" :label="chiose">{{chiose}}</el-radio>
            </el-radio-group>
          </div>
        </el-card>
        <div class="button-container">
            <input type="button" id="next" class="button" value="Next" @click="next();">
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import * as d3 from "d3"
import axios from '../assets/js/http'
export default {
    data () {
      return {
        current: 0,
        imagecurrent:0,
        percentage: 0,
        testNum: 6,
        radio: '',
        imageschiose: "",
        question: '',
        questions: [],
        questionType: 1, //问题类型
        images:[],
        inputClasstype:"",
        inputGraphname:"",
        imageMHPath:"",
        second:0,
        questionchiose:[]
      };
    },
    methods:{
      initImages() {
        this.graphs = [
          'kapmine.svg',
          'sawmill.svg',
          'kan.svg',
          'Mexican.svg',
          'studentgov.svg',
          'PloActor.svg',
          ]
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
      push(){
        let timeFormat = d3.timeFormat("%Y-%m-%d %H:%M:%S");
            axios.post("/saveanswer/", {
                time: timeFormat(new Date()),
                name: this.imageName,
                x1: 0,
                y1: 0,
                x2: 0,
                y2: 0,
                answer: this.radio,
                qid: this.questions[this.current-1].qid,
                consumingtime: this.second.toFixed(1),
                TestType: this.questions[this.current-1].TestType
            }).then(response => {
                let responseData = response.data;
                        if(responseData.state == 'fail') {
                            this.$message.error('提交失败');
                        } else {
                          this.radio = '';
                          this.question=""
                          this.images=[];
                            clearInterval(this.interval);
                            this.$message({
                                message: '提交成功',
                                type: 'success'
                            });
                        }
        })
      },
      next() {
        this.percentage += (100 / this.testNum);
        if (this.percentage > 100) {
          this.percentage = 100;
        }
        if(this.imagecurrent >= this.graphs.length-1) {
          setTimeout(() => {
            this.$router.push({ name: 'home', params: { msg: 'expertment' }});
          }, 1000)
          return;
        }
        this.imagecurrent += 1;
        this.current =0;
        this.images=[];
        this.inputClasstype = ""
        this.inputGraphname = ""
        setTimeout(() => {
          this.getQuestions();
        }, 2000)
        
      },
      initInterval() { // 倒计时
            this.second = 0;
            this.interval = setInterval(() => {
                this.second +=0.1
            }, 100)
        },
      nextquestion() { //下一题
            this.$confirm("是否提交本题进入下一题？", '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
              if(this.radio == ''){
                this.$message.error('您还未做答');
                return;
              }
              this.push();
                if(this.current >= this.questions.length){
                    this.$message({
                        message: '你已完成所有任务，请点击Submit进入下一个实验',
                        type: 'success'
                    });
                }else{
                    setTimeout(() => {
                        this.loadQuestion();
                    }, 2000)
                }
                
            }).catch(() => {     
            });
        },
      getQuestions() {
            axios.post("/getQuestions/", {
                name: this.imageName,
                background: 1,
                TestType: 3
            }).then(response => {
                let responseData = response.data
                this.questions = responseData.datum
                console.log(this.questions)
                this.loadQuestion()
            })
        },
        loadQuestion() {
            this.question = this.questions[this.current].content
            this.questionType=this.questions[this.current].type
            if(this.questionType == 1 ){
              this.imageschiose=this.questions[this.current].choices;
              for(let i=0;i<this.imagesmhs.length;i++){
                this.images.push({
                  name:this.imagesmhs[i],
                  url:["static/images/"+this.imagesmhs[i]],
                  cname:"图片"+(i+1)
                })
              }
            }else{
              this.questionchiose=[]
              this.imageMHPath = "static/images/"+this.questions[this.current].questionImg
              this.imageschiose=this.questions[this.current].choices;
              for(let i=0;i<this.imagesmhs.length;i++){
                this.questionchiose.push(this.imagesmhs[i])
              }
            }
            this.initInterval();
            this.current++
        },
    },
    computed:{
      imagePath: function() {
        return "static/images/" + this.graphs[this.imagecurrent];
      },
      imageName: function() {
        let arr = this.imagePath.split("/");
        return arr[arr.length-1];
      },
      imagesmhs:function() {
        let img=this.imageschiose.split(";");
        img = this.shuffle(img);
        return img;
      },
      percent: function() {
        if(this.percentage >= 100) {
          return 100;
        } else {
          return Math.floor(this.percentage);
        }
      },
      questionTypeText: function() {
            switch(this.questionType)
            {
                case 1://填空
                return '熟悉任务';
                break;
                case 2://判断
                return '语义任务';
                break;
                case 3://判断
                return '语义任务';
                break;
                default:
                return '';
            }
        },
    },
    mounted() {
      this.$nextTick(() => {
        this.initImages();
        this.shuffle(this.graphs);
        this.getQuestions();
      })
    },
}
</script>
<style scoped>
.block{
  text-align: center;
  display: inline-block;
  margin: 1%;
}
.graphselect{
  width: 200px; 
  height: 200px;
  border: 1px solid #c0c0c0;

}
.selectradio{
  display: block;
  margin-top:5px;
}
.text {
    font-size: 14px;
  }

  .item {
    margin-bottom: 18px;
  }

  .clearfix:before,
  .clearfix:after {
    display: table;
    content: "";
  }
  .clearfix:after {
    clear: both
  }

  .box-card {
    width: 480px;
    margin: 0 auto;
  }
  .button-container {
  text-align: center;
  margin: 20px 0;
}
.button {
  width: 100px;
  height: 50px;
  font-size: 18px;
  margin-bottom: 20px;
}
</style>