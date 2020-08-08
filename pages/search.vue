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
          <v-col>
            <v-card class="mx-auto" max-width="344">
              <!-- new mark -->
              <!-- round image -->
              <v-img
                src="https://cdn.vuetifyjs.com/images/cards/sunshine.jpg"
                height="200px"
              ></v-img>
              <!-- 最終ログイン -->
              <!-- 年齢 -->
              <!-- 居住地 -->
              <!-- 相性 -->
              <!-- 一言 -->
              <!-- かげ -->
              <!-- 1列に5人 -->
              <!-- 読み込みは20人ずつ、スクロールで読み込み -->
              <v-card-title>
                Top western road trips
              </v-card-title>

              <v-card-subtitle>
                1,000 miles of wonder
              </v-card-subtitle>

              <v-card-actions>
                <v-btn text>Share</v-btn>

                <v-btn color="purple" text>
                  Explore
                </v-btn>

                <v-spacer></v-spacer>

                <v-btn icon @click="show = !show">
                  <v-icon>{{
                    show ? "mdi-chevron-up" : "mdi-chevron-down"
                  }}</v-icon>
                </v-btn>
              </v-card-actions>
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
      user: [],
      show: true
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
  }
};
</script>
