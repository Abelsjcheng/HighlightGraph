import Vue from 'vue'
import VueRouter from 'vue-router'

import Home from '../components/Home'
import Introduction from '../components/Introduction'
import NodeLinkGraph from '../components/NodeLinkGraph'
import Test from '../components/Test'
import HeatmapGraph from '../components/HeatmapGraph'
import Study from '../components/Study'
import SelectGraph from '../components/SelectGraph'
import Test3 from '../components/Test3'
import Test2 from '../components/Test2'
import Train from '../components/train'
import Experiment from '../components/experiment'
Vue.use(VueRouter)



const router = new VueRouter({
  routes: [
    { path: '/intro', name: 'intro', component: Introduction},
    { path: '/nodelink', name: 'nodelink', component: NodeLinkGraph },
    { path: '/test', name: 'test', component: Test },
    { path: '/Study', name: 'Study', component: Study },
    { path: '/SelectGraph', name: 'SelectGraph', component: SelectGraph },
    { path: '/Test3', name: 'Test3', component: Test3 },
    { path: '/Test2', name: 'Test2', component: Test2 },
    { path: '/heatmap', name: 'heatmap', component: HeatmapGraph },
    { path: '/home', name: 'home', component: Home },
    { path: '/train', name: 'train', component: Train },
    { path: '/experiment', name: 'experiment', component: Experiment },
    { path:'/', redirect:'/home' }
  ]
});

const routerPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
  return routerPush.call(this, location).catch(error=> error)
}

export default router;
