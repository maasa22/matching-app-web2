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
        <h1>いちらん</h1>
        <nuxt-link :to="{ path: 'search_by_profiles' }">
          <button class="box">条件をつけて検索</button>
        </nuxt-link>
        <h4>{{ partners.length }} 人</h4>
        <v-row>
          <v-col v-for="user in partners" :key="user.mail">
            <nuxt-link :to="{ path: 'user/' + user.id }">
              <v-card class="mx-auto" max-width="344">
                <!-- new mark -->
                <!-- round image -->
                <v-img :src="user.profile_images" height="200px"></v-img>

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
              </v-card>
            </nuxt-link>
          </v-col>
        </v-row>
      </div>
    </div>
  </div>
</template>

<script>
import GoogleLoginPage from "~/components/GoogleLoginPage.vue";
import firebase from "@/plugins/firebase";
export default {
  components: {
    GoogleLoginPage
  },
  data() {
    //asyncData()?
    return {
      isWaiting: true,
      isLogin: false,
      loginUserGoogle: [], //ログインしているユーザーの情報 from google
      loginUser: [], //ログインしているユーザーの情報 from firestore
      partners: [] //ほかのユーザー。
    };
  },
  mounted: function() {
    firebase.auth().onAuthStateChanged(userAuth => {
      this.isWaiting = false;
      if (userAuth) {
        this.isLogin = true;
        this.loginUserGoogle = userAuth;
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
            this.fetchUserData();
          });
        })
        .catch(err => {
          console.log("Error getting documents", err);
        });
    },
    fetchUserData() {
      let age_max = 30;
      let age_min = 18;
      let prefectures = ["東京都", "埼玉県", "神奈川県"];
      if (this.$route.query.age_max != undefined) {
        age_max = parseInt(this.$route.query.age_max);
      }
      if (this.$route.query.age_min != undefined) {
        age_min = parseInt(this.$route.query.age_min);
      }
      // if (this.$route.query.prefectures != undefined) {
      //   prefectures = this.$route.query.prefectures;
      // }
      // console.log(age_min, age_max, prefectures);
      firebase
        .firestore()
        .collection("users")
        .where("gender", "==", this.loginUser.partnergender)
        .where("age", "<=", age_max)
        .where("age", ">=", age_min)
        // .where("prefecture", "in", prefectures) //1回しか使えないらしい。
        // .orderby("age", "asc")
        .get()
        .then(snapshot => {
          if (snapshot.empty) {
            console.log("No matching documents.");
            return;
          }
          snapshot.forEach(doc => {
            let partner = doc.data();
            partner["id"] = doc.id;
            this.partners.push(partner);
          });
        })
        .catch(err => {
          console.log("Error getting documents", err);
        });
    }
  }
};
</script>
<style scoped>
/* 最終ログインによって色を変える。 */
.container {
  margin: 0 auto;
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
  height: 300px;
}
a {
  text-decoration: none;
}
</style>
