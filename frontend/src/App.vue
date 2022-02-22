<script setup lang="ts">
import { ref } from 'vue';
// import HelloWorld from './components/HelloWorld.vue'
import NavBar from './components/NavBar.vue'

let count = ref(0);
const isButtonDisabled = false;


function increment() {
  count.value++;
}
</script>

<template>
  <header>
    <NavBar></NavBar>

    <!-- <div class="wrapper"> -->
    <!-- <HelloWorld msg="You did it!" />
    </div>-->
  </header>

  <main>
    <div class="container">
      <button :disabled="isButtonDisabled" v-on:click="increment">{{ count }}</button>
      Enter the name of the page you want to retrieve:
    </div>
  </main>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>