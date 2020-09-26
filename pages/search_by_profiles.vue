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
        <nuxt-link :to="{ path: 'search' }">
          <button class="buttonToReturn">一覧へ</button>
        </nuxt-link>
        <v-row class="buttonToSearch">
          <nuxt-link
            :to="{
              path: 'search',
              query: {
                age_min: age_min,
                age_max: age_max
                //prefectures: prefectures
              }
            }"
          >
            <v-btn class="mr-4">検索</v-btn>
          </nuxt-link>
          <v-btn class="mr-4" @click="onReset">リセット</v-btn>
        </v-row>
        <!-- <v-select
      v-model="prefectures"
      :items="prefectures_option"
      label="都道府県"
      multiple
      chips
    ></v-select>-->

        <v-select
          v-model="age_min"
          :items="age_min_option"
          label="何歳以上"
        ></v-select>

        <v-select
          v-model="age_max"
          :items="age_max_option"
          label="何歳以下"
        ></v-select>
      </div>
    </div>
  </div>
</template>
<script>
//   methods: {
//     async onSubmit(evt) {},
//     onReset(evt) {
//       evt.preventDefault();
//       // Reset our form values
//       this.form.age_min = 17;
//       this.form.age_max = 31;
//       this.form.prefectures = null;
//       // Trick to reset/clear native browser form validation state
//       this.show = false;
//       this.$nextTick(() => {
//         this.show = true;
//       });
//     }
//   }
// };
import GoogleLoginPage from "~/components/GoogleLoginPage.vue";
import firebase from "@/plugins/firebase";

export default {
  components: {
    GoogleLoginPage
  },
  // data: () => ({
  //   isWaiting: true,
  //   isLogin: false,
  //   prefectures: null,
  //   age_min: null, //17
  //   age_max: null, //31
  //   prefectures_option: ["東京都", "埼玉県", "神奈川県"],
  //   age_min_option: [18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
  //   age_max_option: [18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
  // }),
  data() {
    return {
      isWaiting: true,
      isLogin: false,
      prefectures: null,
      age_min: null, //17
      age_max: null, //31
      prefectures_option: ["東京都", "埼玉県", "神奈川県"],
      age_min_option: [18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
      age_max_option: [18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
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
        })
        .catch(err => {
          console.log("Error getting documents", err);
        });
    },
    onReset() {
      this.prefectures = null;
      this.age_min = null;
      this.age_max = null;
    }
  }
};
</script>

<style scoped>
a {
  text-decoration: none;
}
.buttonToReturn {
  margin: 0px 0px 8px 0px;
}
.buttonToSearch {
  margin: 0px 0px 8px 0px;
}
</style>
