
<script setup lang="ts">
import { ref } from 'vue';
import type { Ref } from 'vue';
import { onMounted } from 'vue'

import NavBar from './components/NavBar.vue'
import axios from "axios";



const pageTitleOrUrl = ref("");
let titleSelected = ref(false);
let articleText = ref("");

let articleTheme: Ref<string | undefined> = ref(undefined);
let articleSubtheme: Ref<string | undefined> = ref(undefined);

let themesToSubthemes: { [key: string]: [string] }

let storyThemesSelect = ref([""])
let storySubthemesSelect = ref([""])


function selectTitleInput() {
  titleSelected.value = true
}

async function retrieveArticleText() {
  var titleOrUrl = ""

  titleOrUrl = pageTitleOrUrl.value

  if (titleOrUrl === "")
    return

  axios
    .get("/api/article/?title_or_url=" + titleOrUrl)
    .then((res) => {
      var pageContent = res["data"]['page_content']
      articleText.value = pageContent
    })
    .catch((error) => {
      console.log(error.response);
      alert(error.response.data['detail'])
    })
}

async function generateAudio() {
  console.log(articleTheme.value)
}

function getSubthemes() {
  storySubthemesSelect.value = themesToSubthemes[String(articleTheme.value)]
  articleSubtheme.value = undefined
}

// // Open subtheme select when theme is selected
// function dropdownShouldOpen(VueSelect) {
//   if (articleTheme.value) {
//     console.log("opening drodown")
//     return VueSelect.open
//   }
// }

onMounted(() => {
  axios
    .get("/api/themesandsubthemes",)
    .then((res) => {
      // Unpack themes to subthemes mapping from response
      themesToSubthemes = res["data"]['themes_to_subthemes']
      storyThemesSelect.value = Object.keys(themesToSubthemes);
    })
    .catch((error) => console.log(error));
})

</script>

<template>
  <header>
    <NavBar></NavBar>
  </header>

  <main>
    <div class="container">
      <br />
      <b-form @submit="retrieveArticleText">
        <b-input-group prepend="Title or URL" class="mt-2 mb-1">
          <b-form-input
            v-model="pageTitleOrUrl"
            class="shadow-none"
            :class="{ 'border-primary': titleSelected }"
            type="text"
            placeholder="Enter Wikipedia page title or URL"
            @click="selectTitleInput"
            :required="true"
          ></b-form-input>
        </b-input-group>

        <b-button
          type="submit"
          variant="outline-primary"
          class="mt-3 mb-4 shadow-none"
          :disabled="!titleSelected"
        >Get text</b-button>
      </b-form>

      <div id="fake_textarea" v-if="articleText != ''" v-html="articleText" contenteditable></div>
      <!-- <b-form-textarea v-if="articleText != ''" v-model="articleText" rows="18" max-rows="30"></b-form-textarea> -->

      <div v-if="articleText">
        <div class="row mt-5">
          <v-select
            :options="storyThemesSelect"
            default="Culture"
            v-model="articleTheme"
            placeholder="Enter theme"
            append-to-body
            @close="getSubthemes"
          ></v-select>
          <v-select
            :options="storySubthemesSelect"
            v-model="articleSubtheme"
            :disabled="!articleTheme"
            placeholder="Enter subtheme"
          ></v-select>
        </div>

        <b-button
          variant="primary"
          class="shadow-none"
          style="float: right; margin-top: -40px;"
          :disabled="!(articleSubtheme && articleTheme && articleText)"
          @click="generateAudio"
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

#fake_textarea {
  border: 1px solid rgba(146, 137, 137, 0.555);
  white-space: pre;
  white-space: pre-line;
  height: 425px;
  overflow: auto;
  padding: 10px;
  padding-left: 15px;
  resize: vertical;
  font-size: 15px;
  color: black;
  border-radius: 5px;
}
.shadow-none {
  border-width: 1.5px;
}

.v-select {
  /* max-width: 30em; */
  width: 19em;
}
.row > * {
  /* width: auto; */
  display: inline-block;
  margin-right: 2em;
  height: auto;
}

.row {
  display: flex;
  /* justify-content: space-between; */
}

hl_notfrench {
  color: red;
}
hl_long {
  color: orange;
}
hl_quote {
  color: brown;
}
hl_list {
  color: green;
}
</style>