import {createRouter, createWebHistory} from 'vue-router';
import Register from '@/views/Register';
import Home from '@/views/Home';
import Login from '@/views/Login';
import NotFound from '@/views/NotFound';
import CreateColor from '@/views/CreateColor';
import CreateGym from '@/views/CreateGym';
import GymMapRest from '@/views/GymMapRest';

export default createRouter({
  history: createWebHistory(),
  routes: [
    {path: '/', component: Home},
    {path: '/register', component: Register},
    {path: '/login', component: Login},
    {path: '/create-color', component: CreateColor},
    {path: '/create-gym', component: CreateGym},
    {path: '/gym-map/:gymName', component: GymMapRest},
    {path: '/:pathMatch(.*)', component: NotFound},
  ],
});
