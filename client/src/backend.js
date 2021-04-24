import axios from 'axios';

let axios = axios.create({
  baseURL: '/api/',
  timeout: 5000,
  headers: { 'Content-Type': 'application/json'},
});

axios.interceptors.request.use(function (config) {
  config.headers['Authorization'] = 'Fake Token';
  return config;
})

axios.interceptors.response.use(function (response) {
  return response;},
  function (error) {
  console.log(error);
  return Promise.reject(error);
});

export default {
  fetchRessource () {
    return axios.get(`reource/xxx`)
      .then(response => response.data)
  }
}
