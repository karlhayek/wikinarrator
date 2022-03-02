<script setup lang="ts">
import { ref } from 'vue';
import NavBar from './components/NavBar.vue'
import axios from "axios";


const pageTitleOrUrl = ref("");
let titleSelected = ref(false);
let articleText = ref("");

let articleTheme = ref("");
let articleSubtheme = ref("");


function selectTitleInput() {
  titleSelected.value = true
}

async function retrieveArticleText() {
  var pageInfo = ""

  pageInfo = pageTitleOrUrl.value

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

async function sendText() {
  console.log("Done boy")
  console.log(articleTheme.value)
}

</script>

<template>
  <header>
    <NavBar></NavBar>
  </header>

  <main>
    <div class="container">
      <br />Enter the wikipedia article you wish to retrieve:
      <b-form @submit="retrieveArticleText">
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
          variant="outline-primary"
          class="mt-3 mb-4 shadow-none"
          :disabled="titleSelected == false"
        >Get text</b-button>
      </b-form>

      <b-form-textarea v-if="articleText != ''" v-model="articleText" rows="18" max-rows="30"></b-form-textarea>

      <!-- <b-form @submit="sendText" class="row mt-4" v-if="articleText"> -->
      <div v-if="articleText">
        <div class="row mt-5">
          <b-input-group prepend="Theme">
            <b-form-input v-model="articleTheme" placeholder="Enter theme" :required="true"></b-form-input>
          </b-input-group>

          <b-input-group prepend="Subtheme">
            <b-form-input v-model="articleSubtheme" placeholder="Enter subtheme" :required="true"></b-form-input>
          </b-input-group>
        </div>
        <b-button
          variant="primary"
          class="shadow-none"
          style="float: right; margin-top: -40px;"
          :disabled="!(articleSubtheme && articleTheme && articleText)"
          @click="sendText"
        >Generate audio</b-button>
      </div>
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

.row > * {
  width: auto;
  /* display: inline-block; */
  /* margin-right: 10px; */
}

.row {
  /* display: flex;
  justify-content: space-between; */
}
</style>