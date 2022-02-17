<template>
  <body>
    <nav class="navbar navbar-expand-md navbar-dark bg-dark mb-4">
      <div class="container">
        <a class="navbar-brand" href>{{ appName }}</a>

        <ul class="navbar-nav">
          <li class="nav-item active">
            <!-- <a href="https://www.groupeonepoint.com/" target="_blank">
            <img src="@/assets/logo_onepoint.jpg" />
          </a>-->
            <!-- <img src="@/assets/logo_onepointbdf.png" /> -->
            <!-- <img src="@/assets/logo_onepoint.jpg" /> -->
          </li>
        </ul>
      </div>
    </nav>
  </body>
</template>


<script>
export default {
  name: "NavBar",
  data() {
    return {
      appName: process.env.VUE_APP_NAME,
    };
  },
};
</script>

<style>
.nav-item > img {
  vertical-align: middle;
  height: 40px;
}
</style>