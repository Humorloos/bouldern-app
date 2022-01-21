/** @file router configuration */

import {createRouter, createWebHistory} from 'vue-router';
import Register from '../views/Register.vue';
import Login from '../views/Login.vue';
import NotFound from '../views/NotFound.vue';
import CreateColor from '../views/CreateColor.vue';
import CreateGym from '../views/CreateGym.vue';
import GymMapView from '../views/GymMap.vue';
import store from '../plugins/store';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: GymMapView,
      meta: {requiresAuth: true}},
    {
      path: '/register',
      component: Register},
    {
      path: '/login',
      component: Login},
    {
      path: '/create-color',
      component: CreateColor,
      meta: {requiresAuth: true}},
    {
      path: '/create-gym',
      component: CreateGym,
      meta: {requiresAuth: true}},
    {
      path: '/gym-map/:gymName',
      component: GymMapView,
      meta: {requiresAuth: true},
    },
    {
      path: '/:pathMatch(.*)',
      component: NotFound},
  ],
});

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !store.getters.isAuthenticated) {
    next('/login');
  } else {
    next();
  }
});

export default router;
