<template>
  <div class="body">
    <div class="content">
      <div class="processing_container"><p id="processing">Processing</p></div>
      <div class="mutiple-progress-container">
        <div class="mutiple-progress">
          <div class="circle-container">
            <div class="circle" @click="toTest1();"><label class="number" @click="toTest1();">1</label></div>
            
            <label style="position: absolute;width: 100px;left: -20px;margin-top: 5px;">experiment 1 </label>
          </div>
          <div class="progress">
            <el-progress :show-text="false" :stroke-width="20" :percentage="test1_percentage" color="#ccc"></el-progress>
          </div>
          <div class="circle-container">
            <div class="circle" @click="toTest2();"><label class="number" @click="toTest2();">2</label></div>
            <label style="position: absolute;width: 100px;left: -20px;margin-top: 5px;">experiment 2 </label>
          </div>
          <div class="progress">
            <el-progress :show-text="false" :stroke-width="20" :percentage="test2_percentage" color="#ccc"></el-progress>
          </div>
          <div class="circle-container">
            <div class="circle" @click="totest3();"><label class="number" @click="totest3();">3</label></div>
            <label style="position: absolute;width: 100px;left: -20px;margin-top: 5px;">experiment 3 </label>
            <!-- <div>
                <select @change="changeExperiment();">
                    <option value="1">A</option>
                    <option value="2">B</option>
                    <option value="3">C</option>
                </select>
            </div> -->
          </div>
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
  name: 'Home',
  props: {
  },
  data() {
    return {
      test1_percentage: 0,
      test2_percentage: 0,
    }
  },
  mounted() {
    this.$nextTick(() => {
      let msg = this.$route.params.msg;
      switch (msg) {
        case 'test':
          this.test1_percentage = 100;
          break;
        case 'test2':
          this.test1_percentage = 100;
          this.test2_percentage = 100;
          break;
        default:
          break;
      }
    })
  },
  methods: {
	toTest1() {
        this.$router.push({ name: 'test', params: { msg: 'formal' }});
    },
    toTest2() {
		if( this.test1_percentage == 0 ) {
			alert("请按序操作...")
			return;
        }
        this.$router.push({ name: 'Test2', params: { msg: 'formal' }});
    },
    toStudy() {
      if(this.background == 0) {
				alert("请直接进行实验三...")
				return;
            }
        this.$router.push({ name: 'Study', params: { msg: 'formal' }});
    },
    totest3() {
      if( this.test2_percentage ==0 ) {
        alert("请按序操作...")
        return;
      }
      this.$router.push({ name: 'Study', params: { msg: 'formal' }});
    }
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
</style>
