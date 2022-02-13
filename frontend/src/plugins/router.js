/** @file router configuration */

import {createRouter, createWebHistory} from 'vue-router';
import Register from '../views/Register.vue';
import Login from '../views/Login.vue';
import NotFound from '../views/NotFound.vue';
import CreateColor from '../views/CreateColor.vue';
import CreateGym from '../views/CreateGym.vue';
import ConfirmEmail from '../views/ConfirmEmail.vue';
import GymMapView from '../views/GymMap.vue';
import store from '../plugins/store';
import HomeView from '../views/HomeView.vue';
import ResetPassword from '../views/ResetPassword.vue';
import ChangePassword from '../views/ChangePassword.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: HomeView,
      meta: {requiresAuth: true},
    },
    {
      path: '/register',
      component: Register,
    },
    {
      path: '/login',
      component: Login,
    },
    {
      path: '/reset-password',
      component: ResetPassword,
    },
    {
      path: '/create-color',
      component: CreateColor,
      meta: {requiresAuth: true},
    },
    {
      path: '/create-gym',
      component: CreateGym,
      meta: {requiresAuth: true},
    },
    {
      path: '/gym-map/:gymName',
      component: GymMapView,
      meta: {requiresAuth: true},
      name: 'gymMap',
    },
    {
      path: '/registration/account-confirm-email/:key',
      component: ConfirmEmail,
    },
    {
      path: '/registration/password/reset/change/:uid/:token',
      component: ChangePassword,
    },
    {
      path: '/:pathMatch(.*)',
      component: NotFound,
    },
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
