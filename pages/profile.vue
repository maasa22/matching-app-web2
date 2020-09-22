<template>
  <div>
    <section class="container">
      <div v-if="isWaiting">
        <p>読み込み中</p>
      </div>
      <div v-else>
        <div v-if="!isLogin">
          <!-- <button @click="googleLogin">Googleでログイン</button> -->
          <GoogleLoginPage />
        </div>
        <div v-else>
          <v-card class="mx-auto" max-width="344">
            <v-img :src="user.profile_images" height="250px"></v-img>
            <v-card-title>
              <p>
                <span class="last_login_icon">●</span>
                {{ user.age }}歳
                {{ user.prefecture }}
              </p>
            </v-card-title>
            <v-card-subtitle>
              <div v-if="status_message_editing">
                <v-text-field
                  v-model="status_message"
                  label="ひとこと"
                ></v-text-field>
                <v-btn @click="update_status_message">更新</v-btn>
                <v-btn @click="cancel_editing_status_message">キャンセル</v-btn>
              </div>
              <div v-else>
                {{ user.status_message }}
                <br />
                <v-btn @click="start_editing_status_message"
                  >ひとこと編集</v-btn
                >
              </div>
            </v-card-subtitle>
            <v-card-actions>
              <v-spacer></v-spacer>
            </v-card-actions>
          </v-card>
          <h3>自己紹介</h3>
          <div v-if="introduction_editing">
            <v-textarea v-model="introduction" label="自己紹介"></v-textarea>
            <v-btn @click="update_introduction">更新</v-btn>
            <v-btn @click="cancel_editing_introduction">キャンセル</v-btn>
          </div>
          <div v-else>
            {{ user.introduction }}
            <br />
            <v-btn @click="start_editing_introduction">自己紹介編集</v-btn>
          </div>
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
                  <div v-if="display_name_editing">
                    <td>
                      <v-text-field
                        v-model="display_name"
                        label="名前"
                      ></v-text-field>
                    </td>
                    <td>
                      <v-btn @click="update_display_name">更新</v-btn>
                      <v-btn @click="cancel_editing_display_name"
                        >キャンセル</v-btn
                      >
                    </td>
                  </div>
                  <div v-else>
                    <td>{{ user.display_name }}</td>
                    <td>
                      <v-btn @click="start_editing_display_name"
                        >名前編集</v-btn
                      >
                    </td>
                  </div>
                </tr>
                <tr>
                  <td>年齢</td>
                  <td>{{ user.age }}</td>
                  <td></td>
                </tr>
                <tr>
                  <td>都道府県</td>
                  <td>{{ user.prefecture }}</td>
                </tr>
                <!-- <tr>
                  <td>いいね数</td>
                  <td>{{ user.acquired_favorites }}</td>
                </tr>
                <tr>
                  <td>最終ログイン</td>
                  <td>{{ user.last_login_batch }}</td>
                </tr>-->
              </tbody>
            </template>
          </v-simple-table>

          <!-- <p>{{ userAuth.email }}でログイン中</p>
          <button @click="logOut">ログアウト</button>-->
          <h3>設定</h3>
          <v-btn>課金する（未実装）</v-btn>
          <v-btn @click="logOut">ログアウト</v-btn>
          <v-btn>退会する（未実装）</v-btn>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import GoogleLoginPage from "~/components/GoogleLoginPage.vue";
// いいね済かどうかを判定する。
// いいねされていたら、いいね済に表示を変える。from DB data
// いいねボタンがクリックされたら、いいね済に表示を変える。
import firebase from "@/plugins/firebase";
import { v4 as uuidv4 } from "uuid";
export default {
  components: {
    GoogleLoginPage
  },
  asyncData() {
    return {
      status_message: "",
      status_message_editing: false,
      introduction: "",
      introduction_editing: false,
      display_name: "",
      display_name_editing: false,
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
      console.log("fuga");
      firebase.auth().signOut();
      console.log("hoge");
    },
    checkFirstTime() {
      console.log(this.loginUserGoogle.email);
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
    },
    start_editing_status_message() {
      this.status_message = this.user.status_message;
      this.status_message_editing = true;
    },
    async update_status_message() {
      console.log(this.status_message);
      const data = {
        status_message: this.status_message
      };
      // Add a new document in collection "cities" with ID 'LA'
      const res = await firebase
        .firestore()
        .collection("users")
        .doc(this.loginUser.id)
        .set(data, { merge: true });
      this.user.status_message = this.status_message;
      this.status_message = "";
      this.status_message_editing = false;
    },
    cancel_editing_status_message() {
      this.status_message = "";
      this.status_message_editing = false;
    },
    start_editing_introduction() {
      this.introduction = this.user.introduction;
      this.introduction_editing = true;
    },
    async update_introduction() {
      console.log(this.introduction);
      const data = {
        introduction: this.introduction
      };
      // Add a new document in collection "cities" with ID 'LA'
      const res = await firebase
        .firestore()
        .collection("users")
        .doc(this.loginUser.id)
        .set(data, { merge: true });
      this.user.introduction = this.introduction;
      this.introduction = "";
      this.introduction_editing = false;
    },
    cancel_editing_introduction() {
      this.introduction = "";
      this.introduction_editing = false;
    },
    start_editing_display_name() {
      this.display_name = this.user.display_name;
      this.display_name_editing = true;
    },
    async update_display_name() {
      console.log(this.display_name);
      const data = {
        display_name: this.display_name
      };
      // Add a new document in collection "cities" with ID 'LA'
      const res = await firebase
        .firestore()
        .collection("users")
        .doc(this.loginUser.id)
        .set(data, { merge: true });
      this.user.display_name = this.display_name;
      this.display_name = "";
      this.display_name_editing = false;
    },
    cancel_editing_display_name() {
      this.display_name = "";
      this.display_name_editing = false;
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
