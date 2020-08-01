<template>
  <div class="container">
    <h3 style="text-align:center;">sign in with google account</h3>
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
      console.log("login");
      console.log("login action");
      const provider = new firebase.auth.GoogleAuthProvider();
      firebase
        .auth()
        .signInWithPopup(provider)
        .then(function(result) {
          const user = result.user;
          console.log("success : " + user.uid + " : " + user.displayName);
        })
        .catch(function(error) {
          var errorCode = error.code;
          console.log("error : " + errorCode);
        });
    }
  }
};
</script>
<style scoped>
.v-btn {
  margin-top: 20px;
}
</style>
