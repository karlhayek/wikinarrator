<script setup lang="ts">
import { ref } from 'vue';
import NavBar from './components/NavBar.vue'
import axios from "axios";


let count = ref(0);
const pageTitleOrUrl = ref("");
let titleSelected = ref(false);

let articleText = ref("");


function increment() {
  count.value++;
}

function selectTitleInput() {
  titleSelected.value = true
}

async function onSubmit() {
  var pageInfo = ""

  pageInfo = pageTitleOrUrl.value

  // console.log("Retrieving article content for page " + pageInfo)

  if (pageInfo === "")
    return

  axios
    .post("/api/getarticlecontent", {
      article_title_or_url: pageInfo
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
        <b-input-group prepend="Title or URL" class="mt-2 mb-1">
          <b-form-input
            v-model="pageTitleOrUrl"
            class="shadow-none"
            :class="{ 'border-primary': titleSelected }"
            type="text"
            placeholder="Enter article title or URL"
            @click="selectTitleInput"
            :required="true"
          ></b-form-input>
        </b-input-group>

        <b-button
          type="submit"
          variant="primary"
          class="mt-3 mb-4"
          :disabled="titleSelected == false"
        >Get text</b-button>
      </b-form>

      <b-form-textarea v-if="articleText != ''" v-model="articleText" rows="18" max-rows="30"></b-form-textarea>
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