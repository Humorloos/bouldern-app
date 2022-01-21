/** @file router configuration */

import {createRouter, createWebHistory} from 'vue-router';
import Register from '../views/Register.vue';
import Home from '../views/Home.vue';
import Login from '../views/Login.vue';
import NotFound from '../views/NotFound.vue';
import CreateColor from '../views/CreateColor.vue';
import CreateGym from '../views/CreateGym.vue';
import GymMapView from '../views/GymMap.vue';

export default createRouter({
  history: createWebHistory(),
  routes: [
    {path: '/', component: Home},
    {path: '/register', component: Register},
    {path: '/login', component: Login},
    {path: '/create-color', component: CreateColor},
    {path: '/create-gym', component: CreateGym},
    {path: '/gym-map/:gymName', component: GymMapView},
    {path: '/:pathMatch(.*)', component: NotFound},
  ],
});
