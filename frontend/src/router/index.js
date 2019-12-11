import Vue from 'vue'
import VueRouter from 'vue-router'

import Home from '../components/Home'
import Introduction from '../components/Introduction'
import NodeLinkGraph from '../components/NodeLinkGraph'
import Test from '../components/Test'
import HeatmapGraph from '../components/HeatmapGraph'
import SelectGraph from '../components/SelectGraph'
import Study from '../components/Study'
Vue.use(VueRouter)

const router = new VueRouter({
  routes: [
    { path: '/intro', name: 'intro', component: Introduction},
    { path: '/nodelink', name: 'nodelink', component: NodeLinkGraph },
    { path: '/test', name: 'test', component: Test },
    { path: '/heatmap', name: 'heatmap', component: HeatmapGraph },
    { path: '/home', name: 'home', component: Home },
    { path: '/SelectGraph', name: 'SelectGraph', component: SelectGraph },
    { path: '/Study', name: 'Study', component: Study },
    { path:'/', redirect:'/home' }
  ]
});

export default router;
