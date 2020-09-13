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
          <nuxt-link :to="{ path: '../search' }">
            <v-btn>一覧へ</v-btn>
          </nuxt-link>
          <!-- {{ user }} -->
          <v-card class="mx-auto" max-width="344">
            <!-- new mark -->
            <!-- round image -->
            <v-img :src="user.profile_images" height="250px"></v-img>
            <!-- <v-img
                  src="../../static/images/woman1.jpg"
                  height="200px"
            ></v-img>-->

            <!-- かげ -->
            <!-- 1列に5人 -->
            <!-- 読み込みは20人ずつ、スクロールで読み込み -->
            <!-- create db -->
            <!-- v-icon -->
            <v-card-title>
              <p>
                <span class="last_login_icon">●</span>
                {{ user.age }}歳
                {{ user.prefecture }}
              </p>
            </v-card-title>
            <!-- 相性 -->
            <v-card-subtitle>{{ user.status_message }}</v-card-subtitle>
            <v-card-actions>
              <v-spacer></v-spacer>
              <div v-if="alreadymatched">
                <v-btn color="blue" text>メッセージを送る</v-btn>
              </div>
              <div v-else-if="alreadyliked">
                <v-btn color="blue" text>いいね済</v-btn>
              </div>
              <div v-else>
                <v-btn color="blue" text @click="sendLike(loginUser.id, user_id)">いいね</v-btn>
              </div>
            </v-card-actions>
          </v-card>
          <h3>自己紹介</h3>
          <p>{{ user.introduction }}</p>
          <v-simple-table height="300px">
            <template v-slot:default>
              <thead>
                <tr>
                  <th class="text-left"></th>
                  <th class="text-left"></th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>名前</td>
                  <td>{{ user.display_name }}</td>
                </tr>
                <tr>
                  <td>年齢</td>
                  <td>{{ user.age }}</td>
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
      alreadymatched: false,
      alreadyliked: false,
      isWaiting: true,
      isLogin: false,
      loginUserGoogle: [], //ログインしているユーザーの情報 from google
      loginUser: [], //ログインしているユーザーの情報 from firestore
      user: {}, //ほかのユーザー。
      user_id: "",
    };
  },
  mounted: function () {
    firebase.auth().onAuthStateChanged((userAuth) => {
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
        .then((snapshot) => {
          if (snapshot.empty) {
            //if first time, go to register page
            console.log("No matching documents.");
            this.$router.push("/register");
          }
          snapshot.forEach((doc) => {
            // 表示する性別
            if (doc.data().gender == "male") {
              this.loginUser.partnergender = "female";
            } else {
              this.loginUser.partnergender = "male";
            }
            // ログインユーザーのID
            this.loginUser.id = doc.id;
            this.getUserId();
            let cityRef = firebase
              .firestore()
              .collection("users")
              .doc(this.user_id);
            let getDoc = cityRef
              .get()
              .then((doc) => {
                if (!doc.exists) {
                  console.log("No such document!");
                } else {
                  console.log("Document data:", doc.data());
                  this.user = doc.data();
                }
              })
              .catch((err) => {
                console.log("Error getting document", err);
              });
            let loginUser = firebase
              .firestore()
              .collection("likes")
              .where("sender", "==", this.loginUser.id)
              .where("reciever", "==", this.user_id)
              // .where("mail", "==", "hoge@gmail.com")
              .get()
              .then((snapshot) => {
                if (!snapshot.empty) {
                  this.alreadyliked = true;
                  let loginUser2 = firebase
                    .firestore()
                    .collection("likes")
                    .where("sender", "==", this.user_id)
                    .where("reciever", "==", this.loginUser.id)
                    // .where("mail", "==", "hoge@gmail.com")
                    .get()
                    .then((snapshot) => {
                      if (!snapshot.empty) {
                        this.alreadymatched = true;
                      }
                    });
                }
              });
          });
        })
        .catch((err) => {
          console.log("Error getting documents", err);
        });
    },
    getUserId: function () {
      this.user_id = this.$route.path.split("user/")[1]; //ex. /user/71beb69945ae4
    },
    async sendLike(sender, reciever) {
      this.alreadyliked = true;
      let loginUser3 = firebase
        .firestore()
        .collection("likes")
        .where("sender", "==", this.user_id)
        .where("reciever", "==", this.loginUser.id)
        // .where("mail", "==", "hoge@gmail.com")
        .get()
        .then((snapshot) => {
          if (!snapshot.empty) {
            this.alreadymatched = true;
          }
        });
      console.log(sender, "-->", reciever);
      const data = {
        sender: sender,
        reciever: reciever,
        like_id: uuidv4(),
        likedAt: new Date(),
      };
      // Add a new document in collection "cities" with ID 'LA'
      const res = await firebase
        .firestore()
        .collection("likes")
        .doc(uuidv4())
        .set(data);
    },
  },
  async created() {
    // this.getUserId();
    // let cityRef = firebase.firestore().collection("users").doc(this.user_id);
    // let getDoc = cityRef
    //   .get()
    //   .then((doc) => {
    //     if (!doc.exists) {
    //       console.log("No such document!");
    //     } else {
    //       console.log("Document data:", doc.data());
    //       this.user = doc.data();
    //     }
    //   })
    //   .catch((err) => {
    //     console.log("Error getting document", err);
    //   });
    // let loginUser = firebase
    //   .firestore()
    //   .collection("users")
    //   .where("sender", "==", this.loginUser.id)
    //   .where("reciever", "==", this.user_id)
    //   // .where("mail", "==", "hoge@gmail.com")
    //   .get()
    //   .then((snapshot) => {
    //     if (snapshot.empty) {
    //       //if first time, go to register page
    //       console.log("No matching documents.");
    //       this.$router.push("/register");
    //     } else {
    //       thiis.alreadymatched = true;
    //     }
    //   });
  },
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
