import axios from 'axios'

axios.defaults.baseURL = 'http://127.0.0.1:8086';
axios.defaults.withCredentials = true;
axios.defaults.headers.post['Content-Type'] = 'application/json' //'application/x-www-form-urlencoded';

export default axios;