<script setup lang="ts">
import { ref } from 'vue';
import NavBar from './components/NavBar.vue'
import axios from "axios";


let count = ref(0);
const pageLink = ref("");
const pageTitle = ref("");
let urlSelected = ref(false);
let titleSelected = ref(false);

let articleText = ref("");


function increment() {
  count.value++;
}

function selectTitleInput() {
  titleSelected.value = true
  urlSelected.value = false
}
function selectURLInput() {
  urlSelected.value = true
  titleSelected.value = false
}

async function onSubmit() {
  var pageInfo = ""
  if (urlSelected.value) {
    pageInfo = pageLink.value
  }
  else if (titleSelected.value) {
    pageInfo = pageTitle.value
  }

  // console.log("Retrieving article content for page " + pageInfo)

  if (pageInfo === "")
    return

  axios
    .post("/api/getarticlecontent", {
      title: pageInfo
    })
    .then((res) => {
      var pageContent = res["data"]['page_content']
      articleText.value = pageContent
    })
    .catch((error) => console.log(error));
}


</script>

<template>
  <header>
    <NavBar></NavBar>
  </header>

  <main>
    <div class="container">
      <!-- <button :disabled="isButtonDisabled" v-on:click="increment">{{ count }}</button> -->
      <br />Enter the wikipedia article you wish to retrieve:
      <b-form @submit="onSubmit">
        <b-input-group prepend="URL" class="mt-2 mb-1">
          <b-form-input
            class="shadow-none"
            :class="{ 'border-primary': urlSelected }"
            v-model="pageLink"
            type="url"
            placeholder="Enter article url"
            @click="selectURLInput"
            :required="urlSelected"
          ></b-form-input>
        </b-input-group>or
        <b-input-group prepend="Title" class="mt-2 mb-1">
          <b-form-input
            v-model="pageTitle"
            class="shadow-none"
            :class="{ 'border-primary': titleSelected }"
            type="text"
            placeholder="Enter article title"
            @click="selectTitleInput"
            :required="titleSelected"
          ></b-form-input>
        </b-input-group>

        <b-button
          type="submit"
          variant="primary"
          class="mt-3 mb-5"
          :disabled="(urlSelected || titleSelected) == false"
        >Submit</b-button>
      </b-form>

      <b-form-textarea v-if="articleText != ''" v-model="articleText" rows="16" max-rows="30"></b-form-textarea>
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

.shadow-none {
  border-width: 1.5px;
}
</style>