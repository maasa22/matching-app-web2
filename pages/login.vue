<template>
  <div class="container">
    <h3 style="text-align:center;">Googleアカウントでログインする</h3>
    <v-row justify="center">
      <v-btn
        depressed
        small
        color="primary"
        align-content="center"
        @click="login"
        >Sign in</v-btn
      >
    </v-row>
  </div>
</template>
<script>
import firebase from "~/plugins/firebase";

export default {
  methods: {
    login() {
      const provider = new firebase.auth.GoogleAuthProvider();
      firebase
        .auth()
        .signInWithPopup(provider)
        .then(function(result) {
          const user = result.user;
          // console.log("success : " + user.uid + " : " + user.displayName);
        })
        .catch(function(error) {
          let errorCode = error.code;
          console.log("error : " + errorCode);
        });
    }
  }
};
</script>
<style scoped>
.container {
  margin: 0 auto;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.v-btn {
  margin: 20px 0px;
}
</style>
