<template>
  <div id="app">
    <component :is="layout">
      <div class="bg-image bg-parallax overlay pgbg"></div>
      <!-- <navi></navi> -->
      <router-view/>
    </component>
    <!-- <img src="./assets/logo.png"> -->
  </div>
</template>

<script>
import Navigation from './components/Navigation';
import Default from './layouts/Default';
const default_layout = 'default';

export default {
  name: 'App',
  components: {
    'navi': Navigation,
    'app-layout': Default,
  },
  computed: {
    layout() {
      return (this.$route.meta.layout || default_layout) + '-layout';
    },
  },
  // created: function() {
  //       window.document.title = "SV QA Courses"
  //   },
};
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
