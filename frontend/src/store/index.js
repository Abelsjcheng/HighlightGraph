import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

const store = new Vuex.Store({
	state: {
		username: null,
		background: null,
	},
	getters: {
		background:state => state.background
	},
	mutations: {
		setUsername(state, username) {
			state.username = username;
		},
		setBackground(state, background) {
			state.background = background;
		}
	},
	actions: {
		register(context, username) {
			context.commit("setUsername", username);
		},
		getBackground(context, background) {
			context.commit("setBackground", background);
		}
	}
})	

export default store;