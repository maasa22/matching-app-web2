<template>
  <div>
    <div v-if="isWaiting">
      <p>読み込み中</p>
    </div>
    <div v-if="!isLogin">
      <GoogleLoginPage />
    </div>
    <div v-else class="container">
      <div class="buttonRegister">
        <div>
          <v-btn class="mr-4" @click="registerUser">登録</v-btn>
        </div>
      </div>
      <v-text-field v-model="display_name" label="名前" required></v-text-field>
      <v-select v-model="gender" :items="gender_option" label="性別"></v-select>
      <v-select
        v-model="prefecture"
        :items="prefecture_option"
        label="居住地"
      ></v-select>
      <v-select v-model="age" :items="age_option" label="年齢"></v-select>
      <p>プロフィール画像</p>
      <v-img :src="profile_images" class="profile_images" />
      <label class="postImage-appendBtn">
        <input @change="upload" type="file" data-label="画像の添付" />
      </label>
      <div v-if="isValidationError">
        <v-alert type="error">全て選択して下さい。</v-alert>
      </div>
      <div class="buttonLogin">
        <div class="buttonLogin">
          <v-btn @click="googleLogin"
            >(すでに登録済の方)<br />Googleでログイン</v-btn
          >
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import firebase from "@/plugins/firebase";
import { v4 as uuidv4 } from "uuid";
import GoogleLoginPage from "~/components/GoogleLoginPage.vue";

export default {
  components: {
    GoogleLoginPage
  },
  data: () => ({
    isWaiting: true,
    isLogin: false,
    userAuth: [], //ユーザー。
    show: true,
    users: [], //ほかのユーザー。
    display_name: "",
    gender: null,
    age: null,
    prefecture: null,
    profile_images: "",
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
    async registerUser() {
      if (
        !this.display_name ||
        !this.gender ||
        !this.age ||
        !this.prefecture ||
        !this.profile_images
      ) {
        this.isValidationError = true;
      } else {
        this.isValidationError = false;
        const data = {
          display_name: this.display_name,
          gender: this.gender,
          age: this.age,
          prefecture: this.prefecture,
          mail: this.userAuth.email,
          profile_images: this.profile_images
        };
        // Add a new document in collection "cities" with ID 'LA'
        const res = await firebase
          .firestore()
          .collection("users")
          .doc(uuidv4())
          .set(data);
        this.$router.push("/search");
      }
    },
    googleLogin() {
      const provider = new firebase.auth.GoogleAuthProvider();
      firebase.auth().signInWithRedirect(provider);
      this.$router.push("/search");
    },
    upload(p) {
      const file = p.target.files[0];
      console.log(file);
      const storageRef = firebase
        .storage()
        .ref("imgs/" + uuidv4() + "___" + file.name);
      console.log(storageRef);
      // 画像をStorageにアップロード
      storageRef.put(file).then(() => {
        // アップロードした画像のURLを取得
        storageRef
          .getDownloadURL()
          .then(url => {
            this.profile_images = url;
          })
          .catch(error => {
            console.log(error);
          });
      });
    }
  }
};
</script>

<style scoped>
.container {
  margin: 0 auto;
  height: 70vh;
  max-width: 400px;
}

.buttonRegister {
  margin: 0px 0px 5px 0px;
  text-align: center;
}

.buttonLogin {
  margin: 80px 0px 0px 0px;
  text-align: center;
}

.box {
  display: inline-block;
  width: 100px;
}

.profile_images {
  height: 250px;
}
</style>
