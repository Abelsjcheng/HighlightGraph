<template>
  <div class="body">
    <div class="content">
      <div class="image-container"></div>
        <div class="button-container">
          <input type="button" id="previous" class="bt-button" value="Previous" @click="previous();">
          <input type="button" id="next" class="bt-button" value="Next" @click="next();">
        </div>
    </div>
  </div>
</template>

<script>
import * as d3 from "d3"
import * as h337 from "heatmap.js"
import axios from '../assets/js/http'
export default {
  name: 'NodeLinkGraph',
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
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.setContainerSize();
      this.initImages();
      this.loadSvg();
    })
  },
  methods: {
    initImages() {
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
    },
    getSize() {
      let parentNode = document.querySelector(".image-container");
      this.width = parentNode.clientWidth;
      this.height = parentNode.clientHeight;
    },
    setContainerSize() {
      let screenWidth = document.documentElement.clientWidth ||  document.body.clientWidth;
      let screenHeight = document.documentElement.clientHeight || document.body.clientHeight;
      //document.querySelector(".image-container").style.height = screenHeight * 0.7 + "px";
    },
    loadSvg() {
      let _this = this;
      this.getSize();
      d3.xml(_this.imagePath).then(function(xml) {
        document.querySelector(".image-container").appendChild(xml.documentElement);
        _this.svg = d3.select(".image-container svg");
        let svgWidth = _this.svg.attr("width");
        let svgHeight = _this.svg.attr("height");
        let margin = {left: 20, right: 20, top: 20, bottom: 20}
        let scaleNumber = d3.min([(_this.width - margin.left - margin.right) / svgWidth, (_this.height - margin.top - margin.bottom) / svgHeight]);
        _this.svgWidth = svgWidth * scaleNumber;
        _this.svgHeight = svgHeight * scaleNumber;
        // _this.svg.attr("transform", `
        //   translate(${(_this.width - svgWidth) / 2}, ${(_this.height - svgHeight) / 2})
        //   scale(${scaleNumber}, ${scaleNumber})
        // `);
        // _this.svg.style("position", "absolute")
        //   .style("left", 0)
        //   .style("top", 0);
        _this.svg.attr("width", _this.svgWidth)
        .attr("height", _this.svgHeight)
        .style("position", "absolute")
        .style("left", (_this.width - _this.svgWidth) / 2 + "px")
        .style("top", (_this.height - _this.svgHeight) / 2 + "px");
        _this.createHeatmap();
        document.querySelector("#previous").removeAttribute("disabled");
        document.querySelector("#next").removeAttribute("disabled");
      });
    },
    createHeatmap() {
      let heatmapDiv = document.createElement("div");
      heatmapDiv.id = "heatmap";
      document.querySelector(".image-container").appendChild(heatmapDiv);
      let heatmap = d3.select("#heatmap")
        .style("width", this.svgWidth + "px")
        .style("height", this.svgHeight + "px")
        .style("position", "absolute")
        .style("top", (this.height - this.svgHeight) / 2 + "px")
        .style("left", (this.width - this.svgWidth) / 2 + "px")
        .style("fill", 'red')

      axios.post("/readRect/", {name: this.imageName})
        .then(response => {
          let responseData = response.data;
          console.log(responseData)
          let map = new Map();
          let points = [];
          let viewBox = this.svg.attr("viewBox");
          let viewBoxArr = viewBox.split(" ");
          let radius = 10;
          let xScale = d3.scaleLinear()
            .domain([parseFloat(viewBoxArr[0]), parseFloat(viewBoxArr[0])+parseFloat(viewBoxArr[2])])
            .range([0, this.svgWidth]);
          let yScale = d3.scaleLinear()
            .domain([parseFloat(viewBoxArr[1]), parseFloat(viewBoxArr[1])+parseFloat(viewBoxArr[3])])
            .range([0, this.svgHeight]);
          responseData.datum.forEach(d => {
            d3.selectAll("circle").nodes().forEach(c => {
              let circle = d3.select(c);
              let x = parseFloat(circle.attr("cx"));
              let y = parseFloat(circle.attr("cy")); 
              radius = parseInt(circle.attr("r")) * 1.5;
              if(x > d.x1 && x < d.x2 && y > d.y1 && y < d.y2) {
                let position = map.get(x+','+y);
                if(position == undefined) {
                  map.set(x+','+y, 1);
                } else {
                  map.set(x+','+y, position + 1)
                }
              }
            })
          })
          for (let [key, value] of map.entries()) {
            let arr = key.split(",");
            points.push({x: parseInt(xScale(parseFloat(arr[0]))), y: parseInt(yScale(parseFloat(arr[1]))), value: value});
          }

          let heatmapInstance = h337.create({
            // only container is required, the rest will be defaults
            container: document.querySelector('#heatmap'),
            maxOpacity: .5,
            minOpacity: 0,
            // radius: radius
            // gradient: {
              // enter n keys between 0 and 1 here
              // for gradient color customization
              // 0.25: "rgb(0,0,255)", 
              // 0.55: "rgb(0,255,0)", 
              // 0.95: "yellow", 
              // 1.0: "rgb(255,0,0)"
            // }
          });

          let max = d3.max(points.map(d => d.value));

          heatmapInstance.setData({
            max: max,
            data: points
          });
        })
    },
    previous() {
      console.log(this.current)
      if(this.current <= 0) {
        alert("第一张...");
        return;
      }
      this.current -= 1;
      d3.select(".image-container").selectAll("svg").remove();
      d3.select(".image-container").selectAll("#heatmap").remove();
      this.loadSvg();
    },
    next() {
      if(this.current >= this.images.length-1) {
        setTimeout(() => {
          this.$router.push({ name: 'home', params: { msg: 'expertment' }});
        }, 1000)
        return;
      }
      this.current += 1;
      d3.select(".image-container").selectAll("svg").remove();
      d3.select(".image-container").selectAll("#heatmap").remove();
      document.querySelector("#previous").disabled = "disabled"
      document.querySelector("#next").disabled = "disabled"
      this.loadSvg();
    },
  },
  watch: {
    
  },
  computed: {
    imagePath: function() {
      return "/static/images/lab12/" + this.images[this.current];
    },
    imageName: function() {
      let arr = this.imagePath.split("/");
      return arr[arr.length-1];
    }
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
.image-container {
  width: 65%;
  height: 600px;
  margin: 2% auto;
  border: 0.5px solid #ccc;
  position: relative;
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
#previous {
  float: left;
}
#next {
  float: right;
}
</style>
