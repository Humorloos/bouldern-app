import {createRouter, createWebHistory} from 'vue-router';
import Register from '@/views/Register';
import Home from '@/views/Home';
import Login from '@/views/Login';
import NotFound from '@/views/NotFound';

export default createRouter({
  history: createWebHistory(),
  routes: [
    {path: '/', component: Home},
    {path: '/register', component: Register},
    {path: '/login', component: Login},
    {path: '/:pathMatch(.*)', component: NotFound},
  ],
});
