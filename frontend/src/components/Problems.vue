<template>
    <div class="problem-container">
        <el-card class="box-card">
            <div slot="header" class="clearfix">
                <p>
                    背景信息: <br>
                    {{backgroundinfo}}
                </p>
                <span>{{questionTypeText}} {{current}}/{{questions.length}}</span>
                <el-button style="float: right;" type="primary" @click="nextquestion()">提交</el-button>
            </div>
            <!--单选题-->
            <div v-show="questionType == 3">
                <div class="question-title">
                    {{question}}
                </div>
                <div class="answer">
                    <div class="answer-item" v-for="(item,index) in questions.choice" :key="index">
                        <el-radio v-model="radio" :label="index">{{item}}</el-radio>
                    </div>
                </div>
            </div>
            <!--简答题-->
            <div v-show="questionType == 1">
                <div class="question-title">
                    {{question}}
                </div>
                <div class="answer">
                    <div class="answer-item">
                    <el-input
                        type="textarea"
                        :rows="5"
                        placeholder="请输入答案"
                        v-model="textarea">
                    </el-input>
                    </div>
                </div>
            </div>
            <!--框图-->
            <div v-show="questionType == 2">
                <div class="question-title">
                    {{question}}
                </div>
            </div>
        </el-card>
    </div>
</template>
<script>
import * as d3 from "d3"
import axios from '../assets/js/http'
import { mapGetters } from 'vuex'

export default {
    name: 'Problems',
    props: [ 'graphname' , 'rectInfos'],
    data() {
        return {
            radio1:'',
            textarea: '',
            radio: '',
            current: 0,
            second: 0,
            interval: null,
            questionType: 1, //问题类型
            question: '',
            questions:[],
            backgroundinfo: '',
        }
    },
    methods: {
        nextquestion() { //下一题
            this.$confirm("是否提交本题进入下一题？", '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                if(this.questionType == 1)
                {
                    this.postanswer();
                }else{
                    this.saveRect()
                }
                this.question=""
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
        getQuestions(graphname) {
            axios.post("/getQuestions/", {
                name: graphname,
                background: this.background,
                TestType: 1
            }).then(response => {
                let responseData = response.data
                this.questions = responseData.datum
                this.backgroundinfo = responseData.graphbackground[0].background
                this.loadQuestion()
            })
        },
        postanswer() {
            let timeFormat = d3.timeFormat("%Y-%m-%d %H:%M:%S");
            axios.post("/saveanswer/", {
                time: timeFormat(new Date()),
                name: this.graphname,
                x1: 0,
                y1: 0,
                x2: 0,
                y2: 0,
                answer: this.textarea,
                qid: this.questions[this.current-1].qid,
                consumingtime: this.second.toFixed(1),
                TestType: this.questions[this.current-1].TestType
            }).then(response => {
                let responseData = response.data;
                if(responseData.state == 'fail') {
                    this.$message.error('提交失败');
                } else {
                    clearInterval(this.interval);
                    this.textarea = ""
                    this.$message({
                        message: '提交成功',
                        type: 'success'
                    });
                }
            })
        },
        loadQuestion() {
            this.question = this.questions[this.current].content
            this.questionType=this.questions[this.current].type
            this.initInterval();
            this.current++
        },
        initInterval() { // 倒计时
            this.second = 0;
            this.interval = setInterval(() => {
                this.second +=0.1
            }, 100)
        },
        saveRect() {
            if( this.rectInfos.length == 0 ){
                alert("请框选感兴趣的区域")
            }else{
                let timeFormat = d3.timeFormat("%Y-%m-%d %H:%M:%S");
                this.rectInfos.forEach(d => {
                    axios.post("/saveanswer/", {
                        time: timeFormat(new Date()),
                        name: d.name,
                        x1: d.x1,
                        y1: d.y1,
                        x2: d.x2,
                        y2: d.y2,
                        answer: this.textarea,
                        qid: this.questions[this.current-1].qid,
                        consumingtime: this.second.toFixed(1),
                        TestType: this.questions[this.current-1].TestType
                    }).then(response => {
                        let responseData = response.data;
                        if(responseData.state == 'fail') {
                            this.$message.error('提交失败');
                        } else {
                            clearInterval(this.interval);
                            this.textarea = ""
                            this.$message({
                                message: '提交成功',
                                type: 'success'
                            });
                        }
                    })
                })
            }
            
        }
    },
    computed : {
        questionTypeText: function() {
            switch(this.questionType)
            {
                case 1://填空
                return '填空';
                break;
                case 2://判断
                return '自由探索';
                break;
                default:
                return '';
            }
        },
        ...mapGetters(["background"])
    },
    watch:{
        graphname(name) {
            if(name != ''||name !=null){
                this.current = 0
                this.getQuestions(name)
            }
        }
    },
    mounted() {
    }
}
</script>
<style scoped>
.problem-container{
  height: 300px;
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
    margin:6% auto;
  }
  .answer-item {
  padding: 10px;
}
#second {
  position: absolute;
  left: 33%;
  top: 7%;
  font-size: 30px;
  font-weight: bold;
  color: #ccc;
}
</style>