<template>
  <div>
    <div v-if="isWaiting">
      <p>読み込み中</p>
    </div>
    <div v-else>
      <div v-if="!isLogin">
        <GoogleLoginPage />
      </div>
      <div v-else class="container">
        <div class="top_part">
          <nuxt-link :to="{ path: '../search' }">
            <v-btn>一覧へ</v-btn>
          </nuxt-link>
        </div>
        <!-- {{ partner }} -->
        <v-card class="mx-auto" max-width="344">
          <!-- new mark -->
          <!-- round image -->
          <v-img :src="partner.profile_images" height="250px"></v-img>
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
              {{ partner.age }}歳
              {{ partner.prefecture }}
            </p>
          </v-card-title>
          <!-- 相性 -->
          <v-card-subtitle>{{ partner.status_message }}</v-card-subtitle>
          <v-card-actions>
            <v-spacer></v-spacer>
            <!-- <div v-if="!isWaiting2"> -->
            <div v-if="alreadymatched">
              <v-btn color="blue" text @click="goToChat"
                >メッセージを送る</v-btn
              >
            </div>
            <div v-else-if="alreadyliked">
              <v-btn color="blue" text>いいね済</v-btn>
            </div>
            <div v-else>
              <v-btn
                color="blue"
                text
                @click="sendLike(loginUser.id, partnerId)"
                >いいね</v-btn
              >
            </div>
            <!-- </div> -->
          </v-card-actions>
        </v-card>
        <h3>自己紹介</h3>
        <p>{{ partner.introduction }}</p>
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
                <td>{{ partner.display_name }}</td>
              </tr>
              <tr>
                <td>年齢</td>
                <td>{{ partner.age }}</td>
              </tr>
              <tr>
                <td>都道府県</td>
                <td>{{ partner.prefecture }}</td>
              </tr>
              <!-- <tr>
                  <td>いいね数</td>
                  <td>{{ partner.acquired_favorites }}</td>
                </tr>
                <tr>
                  <td>最終ログイン</td>
                  <td>{{ partner.last_login_batch }}</td>
                </tr>-->
            </tbody>
          </template>
        </v-simple-table>
      </div>
    </div>
  </div>
</template>

<script>
import GoogleLoginPage from "~/components/GoogleLoginPage.vue";
import firebase from "@/plugins/firebase";
import { v4 as uuidv4 } from "uuid";
export default {
  components: {
    GoogleLoginPage
  },
  asyncData() {
    //data() {
    return {
      alreadymatched: false,
      alreadyliked: false,
      isWaiting: true,
      isWaiting2: true,
      isLogin: false,
      loginUserGoogle: [], //ログインしているユーザーの情報 from google
      loginUser: [], //ログインしているユーザーの情報 from firestore
      partner: {}, //ほかのユーザー。
      partnerId: ""
    };
  },
  mounted: function() {
    firebase.auth().onAuthStateChanged(userAuth => {
      this.isWaiting = false;
      if (userAuth) {
        this.isLogin = true;
        this.loginUserGoogle = userAuth;
        console.log("hoge");
        // if first time, go to register page
        this.checkAlreadyRegistered();
      } else {
        this.isLogin = false;
        this.loginUserGoogle = [];
      }
    });
  },
  methods: {
    checkAlreadyRegistered() {
      firebase
        .firestore()
        .collection("users")
        .where("mail", "==", this.loginUserGoogle.email)
        .get()
        .then(snapshot => {
          if (snapshot.empty) {
            //if first time, go to register page
            console.log("No matching documents.");
            this.$router.push("/register");
          }
          snapshot.forEach(doc => {
            this.loginUser.gender = doc.data().gender;
            // 表示する性別
            if (this.loginUser.gender == "male") {
              this.loginUser.partnergender = "female";
            } else {
              this.loginUser.partnergender = "male";
            }
            this.loginUser.id = doc.id;
            this.fetchPartnerInfo();
          });
        })
        .catch(err => {
          console.log("Error getting documents", err);
        });
    },
    fetchPartnerInfo: function() {
      this.partnerId = this.$route.path.split("user/")[1]; //ex. /user/71beb69945ae4
      console.log(this.partnerId);
      firebase
        .firestore()
        .collection("users")
        .doc(this.partnerId)
        .get()
        .then(doc => {
          if (!doc.exists) {
            console.log("No such document!");
          } else {
            // console.log("Document data:", doc.data());
            this.partner = doc.data();
            this.checkAlreadyMatched();
          }
        })
        .catch(err => {
          console.log("Error getting document", err);
        });
    },
    checkAlreadyMatched: function() {
      firebase
        .firestore()
        .collection("likes")
        .where("sender", "==", this.loginUser.id)
        .where("receiver", "==", this.partnerId)
        .get()
        .then(snapshot => {
          if (snapshot.empty) {
            //if first time, go to register page
            console.log("No matching documents.");
          } else {
            firebase
              .firestore()
              .collection("likes")
              .where("sender", "==", this.partnerId)
              .where("receiver", "==", this.loginUser.id)
              // .where("mail", "==", "hoge@gmail.com")
              .get()
              .then(snapshot => {
                if (snapshot.empty) {
                  //if first time, go to register page
                  console.log("No matching documents.");
                  this.alreadyliked = true;
                } else {
                  this.alreadymatched = true;
                  // this.isWaiting2 = false;
                }
              });
          }
        });
    },
    async sendLike(sender, receiver) {
      this.alreadyliked = true;
      let loginUser3 = firebase
        .firestore()
        .collection("likes")
        .where("sender", "==", this.partnerId)
        .where("receiver", "==", this.loginUser.id)
        // .where("mail", "==", "hoge@gmail.com")
        .get()
        .then(snapshot => {
          if (!snapshot.empty) {
            this.alreadymatched = true;
          }
        });
      console.log(sender, "-->", receiver);
      const data = {
        sender: sender,
        receiver: receiver,
        like_id: uuidv4(),
        likedAt: new Date()
      };
      // Add a new document in collection "cities" with ID 'LA'
      const res = await firebase
        .firestore()
        .collection("likes")
        .doc(uuidv4())
        .set(data);
    },
    goToChat() {
      this.$router.push(
        "/messagedetail/" + this.loginUser.id + "___" + this.partnerId
      );
    }
  }
};
</script>
<style scoped>
/* 最終ログインによって色を変える。 */
.container {
  margin: 0 auto;
}

.top_part {
  margin: 0px 0px 5px 0px;
}
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

a {
  text-decoration: none;
}
</style>
