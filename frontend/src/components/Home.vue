<template>
  <div class="body">
    <div class="header">
      <span><a href="/">Evaluation System</a></span>
      <el-button style="float:right;margin-top:10px;margin-right: 1%;" round @click="signout">Sign out </el-button>
    </div>
    <div class="content">
      <div class="processing_container"><p id="processing">Processing</p></div>
      <div class="mutiple-progress-container">
        <div class="mutiple-progress">
          <div class="circle-container">
            <div class="circle" @click="toIntro();"><label class="number" @click="toIntro();">I</label></div>
            
            <label style="position: absolute;left: -15px;margin-top: 5px;">Introduction </label>
          </div>
          <div class="progress">
            <el-progress :show-text="false" :stroke-width="20" :percentage="intro_percentage" color="#ccc"></el-progress>
          </div>
          <div class="circle-container">
            <div class="circle" @click="toTrain();"><label class="number" @click="toTrain();">1</label></div>
            <label style="position: absolute;left: 7px;margin-top: 5px;">Train </label>
          </div>
          <div class="progress">
            <el-progress :show-text="false" :stroke-width="20" :percentage="train_percentage" color="#ccc"></el-progress>
          </div>
          <div class="circle-container">
            <div class="circle" @click="toExperiment();"><label class="number" @click="toExperiment();">2</label></div>
            <label style="position: absolute;width: 100px;left: -20px;margin-top: 5px;">Experiment </label>
          </div>
          <div class="progress">
            <el-progress :show-text="false" :stroke-width="20" :percentage="expertment_percentage" color="#ccc"></el-progress>
          </div>
          <div class="circle-container">
            <div class="circle" @click="toHeatmap();"><label class="number" @click="toHeatmap();">H</label></div>
            <label style="position: absolute;width: 120px;left: -30px;margin-top: 5px;">Result Review</label>
            <!-- <div>
                <select @change="changeExperiment();">
                    <option value="1">A</option>
                    <option value="2">B</option>
                    <option value="3">C</option>
                </select>
            </div> -->
          </div>
          <!--
          <div class="circle-container-toHeat">
            <div class="circle" @click="toHeatmap();"></div>
            <p class="number" @click="toHeatmap();">H</p>
          </div> -->
        </div>
      </div>
    </div>
    <el-dialog
      title="Sign up"
      :visible.sync="dialogVisible"
      width="60%"
      :show-close="false"
      :close-on-click-modal="false">
      <el-form size="medium" label-position="left" :model="form" :rules="rules" ref="ruleForm" label-width="110px" class="demo-ruleForm">
        <el-form-item label="Name" prop="name">
          <el-input v-model="form.name"></el-input>
        </el-form-item>
        <el-form-item label="Sex" prop="sex">
          <el-radio-group v-model="form.sex">
            <el-radio label="Male"></el-radio>
            <el-radio label="Female"></el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="Age" prop="age">
          <el-input v-model.number="form.age"></el-input>
        </el-form-item>
        <el-form-item label="Education" prop="education">
          <el-select v-model="form.education" placeholder="please select education">
            <el-option label="undergraduate" value="undergraduate"></el-option>
            <el-option label="master" value="master"></el-option>
            <el-option label="doctor" value="doctor"></el-option>
            <el-option label="others" value="others"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="Research" prop="research">
          <el-input v-model="form.research"></el-input>
        </el-form-item>
        <el-form-item label="Background" prop="background">
          <el-radio-group v-model="form.background">
            <el-radio label="1">YES</el-radio>
            <el-radio label="0">NO</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm('ruleForm')">Register</el-button>
          <el-button @click="resetForm('ruleForm')">Reset</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import * as d3 from "d3"
import axios from '../assets/js/http'
import { mapGetters } from 'vuex'
export default {
  name: 'Home',
  props: {
  },
  data() {
    return {
			intro_percentage: 0,
      train_percentage: 0,
      expertment_percentage: 0,
      dialogVisible: false,
      form: {
        name: '',
        education: '',
        age: '',
        sex: '',
        research: '',
        background: ''
      },
      rules: {
        name: [
          { required: true, message: 'please input user name', trigger: 'blur' },
          // { min: 3, max: 5, message: '长度在 3 到 5 个字符', trigger: 'blur' }
        ],
        sex: [
          { required: true, message: 'please select sex', trigger: 'change' }
        ],
        education: [
          { required: true, message: 'please select education', trigger: 'change' }
        ],
        age: [
          // { required: true, message: 'please input age', trigger: 'blur' },
          // { type: 'number', message: 'age must be number', trigger: 'blur'}
          { required: true, message: 'please input age'},
          { type: 'number', message: 'age must be number'}
        ],
        research: [
          { required: true, message: 'please input research derection', trigger: 'blur' }
        ],
        background: [
          { required: true, message: 'please select background', trigger: 'change' }
        ]
      }
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.isLogged();
      let msg = this.$route.params.msg;
      switch (msg) {
        case 'intro':
          this.intro_percentage = 100;
          break;
        case 'train':
          this.intro_percentage = 100;
          this.train_percentage = 100;
          break;
        case 'expertment':
          this.intro_percentage = 100;
          this.train_percentage = 100;
          this.expertment_percentage = 100;
          break;
        default:
          break;
      }
    })
  },
  methods: {
    toIntro() {
      this.isLogged();
			this.$router.push('/intro');
		},
		toTrain() {
			if(this.intro_percentage == 0) {
				alert("请按序操作...")
				return;
			}
			this.$router.push('/train');
    },
    toExperiment() {
      if(this.train_percentage == 0) {
				alert("请按序操作...")
				return;
			}
			this.$router.push('/experiment');
    },
    toHeatmap() {
      this.$router.push('/heatmap');
    },
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          axios.post("/register/", this.form)
            .then(response => {
              if(response.data == 'OK') {
                this.dialogVisible = false;
                this.$store.commit("setBackground",this.form.background);
                alert('success');
              } else if(response.data == 'fail') {
                alert('The user already exists');
              } else {
                alert('The user already sign in');
              }
            }) 
        } else {
          // alert('error');
          return false;
        }
      });
    },
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },
    signout() {
      axios.get('/signout/')
        .then(response => {
          if(response.data == 'OK') {
            alert("sign out")
            window.location.href="/";
          }
        })
    },
    isLogged() {
      axios.get('/isLogged/')
      .then(response => {
        if(response.data == 'log_in') { // 已经登录
          this.dialogVisible = false;
        } else { // 未登录
          this.dialogVisible = true;
        }
      })
    },
    
  },
  computed: {
    ...mapGetters(["background"])
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
.processing_container {
  text-align: center;
  margin-top: 15%;
}
#processing {
  font-size: 40px;
  font-weight: bold;
  color: #ccc;
}
.mutiple-progress-container {
  text-align: center;
  margin-top: 100px;
}
.mutiple-progress {
  margin: 0 auto;
  vertical-align: middle;
  display: inline;
}
.progress {
  text-align: center;
  display: inline-block;
  width: 15%;
  margin-left: 15px;
  vertical-align: middle;
}
.circle-container {
  text-align: center;
  display: inline-block;
  width: 50px;
  height: 50px;
  margin-left: 15px;
  position: relative;
  vertical-align: middle;
}
.circle-container-toHeat{
  text-align: center;
  width: 50px;
  height: 50px;
  margin: 1% auto;
  left: 8px;
  position: relative;
  vertical-align: middle;
}
.circle {
  width: 100%;
  height: 100%;
  background-color: #ccc;
  border-radius: 50%;
  cursor: pointer;
}
.number {
  font-size: 25px;
  color: #fff;
  line-height: 50px;
  margin-top: -50px;
  cursor: pointer;
}

.header {
  width: 100%;
  height: 20%;
  background-color: #ccc;
}
.header a {
  font-size: 25px;
  font-weight: bold;
  line-height: 60px;
  color: white;
  margin-left: 1%;
  text-decoration: none;
}
.signout{
  float: right;
}
</style>
