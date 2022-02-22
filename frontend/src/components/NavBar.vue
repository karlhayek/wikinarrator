<template>
<body>
  <nav class="navbar navbar-expand-md navbar-dark bg-dark mb-4">
    <div class="container">
      <a class="navbar-brand">{{ appName }}</a>

      <ul class="navbar-nav">
        <li class="nav-item active"></li>
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
  height: 40px;
}
</style>