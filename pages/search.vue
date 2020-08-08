<template>
  <section class="container">
    <div v-if="isWaiting">
      <p>読み込み中</p>
    </div>
    <div v-else>
      <div v-if="!isLogin">
        <button @click="googleLogin">Googleでログイン</button>
      </div>
      <div v-else>
        <v-row>
          <v-col v-for="user in users" :key="user.mail">
            <!-- {{ user }} -->
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
                  <span class="last_login_icon">●</span> {{ user.age }}歳
                  {{ user.prefecture }}
                </p>
              </v-card-title>
              <!-- 相性 -->
              <v-card-subtitle>
                {{ user.status_message }}
              </v-card-subtitle>
              <!-- 
              <v-card-actions>
                <v-spacer></v-spacer>

                <v-btn icon @click="show = !show">
                  <v-icon>{{
                    show ? "mdi-chevron-up" : "mdi-chevron-down"
                  }}</v-icon>
                </v-btn> 
              </v-card-actions>-->
            </v-card>
          </v-col>
        </v-row>
        <p>{{ user.email }}でログイン中</p>
        <button @click="logOut">ログアウト</button>
      </div>
    </div>
  </section>
</template>

<script>
import firebase from "@/plugins/firebase";
export default {
  asyncData() {
    return {
      isWaiting: true,
      isLogin: false,
      user: [], //ユーザー。
      show: true,
      users: [] //ほかのユーザー。
    };
  },
  mounted: function() {
    firebase.auth().onAuthStateChanged(user => {
      this.isWaiting = false;
      if (user) {
        this.isLogin = true;
        this.user = user;
      } else {
        this.isLogin = false;
        this.user = [];
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
    }
  },
  async created() {
    const citiesRef = firebase.firestore().collection("users");
    const snapshot = await citiesRef
      .where("gender", "==", "female")
      // .orderby("age", "asc")
      .get();
    if (snapshot.empty) {
      // console.log("No matching documents.");
      return;
    }
    snapshot.forEach(doc => {
      // console.log(doc.id, "=>", doc.data());
      this.users.push(doc.data());
    });
  }
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
  height: 300px;
}
</style>
