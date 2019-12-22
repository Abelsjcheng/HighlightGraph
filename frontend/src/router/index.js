import Vue from 'vue'
import VueRouter from 'vue-router'

import Home from '../components/Home'
import Introduction from '../components/Introduction'
import NodeLinkGraph from '../components/NodeLinkGraph'
import Test from '../components/Test'
import HeatmapGraph from '../components/HeatmapGraph'
import Study from '../components/Study'
import SelectGraph from '../components/SelectGraph'
Vue.use(VueRouter)

const router = new VueRouter({
  routes: [
    { path: '/intro', name: 'intro', component: Introduction},
    { path: '/nodelink', name: 'nodelink', component: NodeLinkGraph },
    { path: '/test', name: 'test', component: Test },
    { path: '/Study', name: 'Study', component: Study },
    { path: '/SelectGraph', name: 'SelectGraph', component: SelectGraph },
    { path: '/heatmap', name: 'heatmap', component: HeatmapGraph },
    { path: '/home', name: 'home', component: Home },
    { path:'/', redirect:'/home' }
  ]
});

export default router;
