import Vue from 'vue';
import Router from 'vue-router';
import HelloWorld from '@/components/HelloWorld';
import Blog from '@/components/Blog';
import Home from '@/components/Home';
import About from '@/components/About';
import Contact from '@/components/Contact';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      meta: {layout: 'default'},
      component: Home,
    },
    {
      path: '/blog',
      name: 'Blog',
      meta: {layout: 'default'},
      component: Blog,
    },
    {
      path: '/about',
      name: 'About',
      meta: {layout: 'default'},
      component: About,
    },
    {
      path: '/contact',
      name: 'Contact',
      meta: {layout: 'default'},
      component: Contact,
    },
  ],
  mode: 'history',
});
