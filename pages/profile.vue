<template>
  <div>
    <section class="container">
      <div v-if="isWaiting">
        <p>読み込み中</p>
      </div>
      <div v-else>
        <div v-if="!isLogin">
          <button @click="googleLogin">Googleでログイン</button>
        </div>
        <div v-else>
          <v-card class="mx-auto" max-width="344">
            <v-img :src="user.profile_images" height="250px"></v-img>
            <v-card-title>
              <p>
                <span class="last_login_icon">●</span> {{ user.age }}歳
                {{ user.prefecture }}
              </p>
            </v-card-title>
            <v-card-subtitle>
              {{ user.status_message }}<v-btn>ひとこと編集</v-btn>
            </v-card-subtitle>
            <v-card-actions>
              <v-spacer></v-spacer>
            </v-card-actions>
          </v-card>
          <h3>自己紹介</h3>
          <p>{{ user.introduction }}</p>
          <v-btn>自己紹介編集</v-btn>
          <v-simple-table height="300px">
            <template v-slot:default>
              <thead>
                <tr>
                  <th class="text-left"></th>
                  <th class="text-left"></th>
                  <th class="text-left"></th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>名前</td>
                  <td>{{ user.display_name }}</td>
                  <td><v-btn>編集</v-btn></td>
                </tr>
                <tr>
                  <td>年齢</td>
                  <td>{{ user.age }}</td>
                  <td><v-btn>編集</v-btn></td>
                </tr>
                <tr>
                  <td>都道府県</td>
                  <td>{{ user.prefecture }}</td>
                  <td><v-btn>編集</v-btn></td>
                </tr>
                <!-- <tr>
                  <td>いいね数</td>
                  <td>{{ user.acquired_favorites }}</td>
                </tr>
                <tr>
                  <td>最終ログイン</td>
                  <td>{{ user.last_login_batch }}</td>
                </tr> -->
              </tbody>
            </template>
          </v-simple-table>

          <!-- <p>{{ userAuth.email }}でログイン中</p>
          <button @click="logOut">ログアウト</button> -->
        </div>
      </div>
    </section>
  </div>
</template>

<script>
// いいね済かどうかを判定する。
// いいねされていたら、いいね済に表示を変える。from DB data
// いいねボタンがクリックされたら、いいね済に表示を変える。
import firebase from "@/plugins/firebase";
import { v4 as uuidv4 } from "uuid";
export default {
  asyncData() {
    return {
      isWaiting: true,
      isLogin: false,
      loginUserGoogle: [], //ログインしているユーザーの情報 from google
      loginUser: [], //ログインしているユーザーの情報 from firestore
      user: {}, //ほかのユーザー。
      user_id: ""
    };
  },
  mounted: function() {
    firebase.auth().onAuthStateChanged(userAuth => {
      this.isWaiting = false;
      if (userAuth) {
        this.isLogin = true;
        this.loginUserGoogle = userAuth;
        // if first time, go to register page
        this.checkFirstTime();
      } else {
        this.isLogin = false;
        this.loginUserGoogle = [];
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
    checkFirstTime() {
      let loginUser = firebase
        .firestore()
        .collection("users")
        .where("mail", "==", this.loginUserGoogle.email)
        // .where("mail", "==", "hoge@gmail.com")
        .get()
        .then(snapshot => {
          if (snapshot.empty) {
            //if first time, go to register page
            console.log("No matching documents.");
            this.$router.push("/register");
          }
          snapshot.forEach(doc => {
            // 表示する性別
            if (doc.data().gender == "male") {
              this.loginUser.partnergender = "female";
            } else {
              this.loginUser.partnergender = "male";
            }
            // ログインユーザーのID
            this.loginUser.id = doc.id;
            this.user_id = doc.id;
            this.user = doc.data();
          });
        })
        .catch(err => {
          console.log("Error getting documents", err);
        });
    }
  }
  //   async created() {
  //     let cityRef = firebase
  //       .firestore()
  //       .collection("users")
  //       .doc(this.user_id);
  //     let getDoc = cityRef
  //       .get()
  //       .then(doc => {
  //         if (!doc.exists) {
  //           console.log("No such document!");
  //         } else {
  //           console.log("Document data:", doc.data());
  //           this.user = doc.data();
  //         }
  //       })
  //       .catch(err => {
  //         console.log("Error getting document", err);
  //       });
  //   }
};
</script>
<style scoped>
/* 最終ログインによって色を変える。 */
.last_login_icon {
  width: 20px;
  height: 20px;
  color: #005555;
  font-weight: 2000;
  border-radius: 50%;
  /* background-color: blueviolet; */
}
.mx-auto {
  /* height: 350px; */
  margin-bottom: 40px;
}
</style>
