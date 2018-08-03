<template>
  <div id="inspire">
      <navi></navi>
      <slot />
    <footer id="footer" class="section" color="indigo" app>
			
    </footer>
    <div id='preloader'><div class='preloader'></div></div>
  </div>
</template>

<script>
  import Navigation from '../components/Navigation';
  import '../assets/css/bootstrap.min.css';
  import '../assets/css/font-awesome.min.css';
  import '../assets/css/style.css';
  import * as jquery from '../assets/js/jquery.min.js';
  // import * as bootstrap from '../assets/js/bootstrap.min.js';
  import * as main from '../assets/js/main.js';
  export default { 
    data: () => ({
      drawer: null
    }),
    props: {
      source: String,
    },
    components: {
    'navi': Navigation,
    },
  };
</script>
