<template>
  <div class="container">
    <div v-if="isWaiting">
      <p>読み込み中</p>
    </div>
    <div v-else>
      <div v-if="!isLogin">
        <button @click="googleLogin">Googleでログイン</button>
      </div>
      <div v-else>
        <v-row>
          <nuxt-link :to="{ path: 'search' }">
            <v-btn class="mr-4" @click="registerUser">登録</v-btn>
          </nuxt-link>
        </v-row>
        <v-text-field v-model="name" label="名前" required></v-text-field>
        <v-select
          v-model="gender"
          :items="gender_option"
          label="性別"
        ></v-select>
        <v-select
          v-model="prefecture"
          :items="prefecture_option"
          label="居住地"
        ></v-select>
        <v-select v-model="age" :items="age_option" label="年齢"></v-select>
        <p>プロフィール画像</p>
        <label class="postImage-appendBtn">
          <input @change="upload" type="file" data-label="画像の添付" />
        </label>
        <div v-if="isValidationError">
          <v-alert type="error">全て選択して下さい。</v-alert>
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped>
.box {
  display: inline-block;
  width: 100px;
}
</style>

<script>
import firebase from "@/plugins/firebase";
import { v4 as uuidv4 } from "uuid";

export default {
  data: () => ({
    isWaiting: true,
    isLogin: false,
    userAuth: [], //ユーザー。
    show: true,
    users: [], //ほかのユーザー。
    name: "",
    gender: null,
    age: null,
    prefecture: null,
    isValidationError: false,
    gender_option: ["male", "female"],
    prefecture_option: ["東京都", "埼玉県", "神奈川県"],
    age_option: [18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
  }),
  mounted: function() {
    firebase.auth().onAuthStateChanged(userAuth => {
      this.isWaiting = false;
      if (userAuth) {
        this.isLogin = true;
        this.userAuth = userAuth;
        console.log(this.userAuth.email);
      } else {
        this.isLogin = false;
        this.userAuth = [];
      }
    });
  },
  methods: {
    googleLogin() {
      const provider = new firebase.auth.GoogleAuthProvider();
      firebase.auth().signInWithRedirect(provider);
    },
    logOut() {
      firebase.auth().signOut();
    },
    async registerUser() {
      if (!this.name || !this.gender || !this.age || !this.prefecture) {
        this.isValidationError = true;
      } else {
        this.isValidationError = false;
        const data = {
          name: this.name,
          gender: this.gender,
          age: this.age,
          prefecture: this.prefecture,
          mail: this.userAuth.email
        };
        // Add a new document in collection "cities" with ID 'LA'
        const res = await firebase
          .firestore()
          .collection("users")
          .doc(uuidv4())
          .set(data);
      }
    }
  }
};
</script>
