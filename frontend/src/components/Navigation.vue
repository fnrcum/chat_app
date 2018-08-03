<template>
		<div id="header" class="sticktop">
			<!-- <div class="container">
				<div class="navbar-header">
					<div class="navbar-brand">
						<router-link class="logo" to="/">
              <img src="../assets/img/svlogo.svg" alt="logo">
						</router-link>
					</div>
					<button class="navbar-toggle">
						<span></span>
					</button>
				</div>
				<nav id="nav">
					<ul class="main-menu nav navbar-nav navbar-right">
						<li><router-link to="/">Home</router-link></li>
						<li><router-link to="/blog">Blog</router-link></li>
						<li><router-link to="/login">Login</router-link></li>
            <li><router-link to="/register">Register</router-link></li>
					</ul>
				</nav>
			</div> -->
		</div>
</template>

<script>
export default {
  name: 'Navigation',
  data() {
    return {
      links: [
        {
          id: 0,
          text: 'About',
          page: '/about',
        },
        {
          id: 0,
          text: 'Contact',
          page: '/contact',
        },
        {
          id: 0,
          text: 'Hello World',
          page: '/HelloWorld',
        },
        {
          id: 0,
          text: 'Home',
          page: '/home',
        },
        {
          id: 0,
          text: 'Ping',
          page: '/ping',
        },
      ],
    };
  },
};
</script>
