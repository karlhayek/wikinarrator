<template>
<body>
  <nav class="navbar navbar-expand-md navbar-dark bg-dark mb-2">
    <div class="container">
      <a class="navbar-brand">{{ appName }}</a>

      <ul class="navbar-nav">
        <li class="nav-item active">
          <img src="@/assets/wikinarrator_logo.jpg" />
        </li>
      </ul>
    </div>
  </nav>
</body>
</template>


<script setup lang="ts">
let appName = import.meta.env.VITE_APP_NAME;

</script>


<style>
.nav-item > img {
  vertical-align: middle;
  height: 45px;
  margin-bottom: -5px;
  margin-top: -5px;
}
</style>