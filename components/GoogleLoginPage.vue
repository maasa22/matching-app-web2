<template>
  <div>
    <v-btn @click="googleLogin">Googleでログイン</v-btn>
  </div>
</template>
<script>
import firebase from "@/plugins/firebase";
export default {
  methods: {
    googleLogin() {
      const provider = new firebase.auth.GoogleAuthProvider();
      firebase.auth().signInWithRedirect(provider);
    }
  }
};
</script>
