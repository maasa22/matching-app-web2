<template>
  <div>
    <!-- <p>{{ $store.getters }}</p> -->
    <p>{{ this.authUser }}</p>
    <!-- <p>{{ this.authUser.displayName }}</p> -->
  </div>
</template>

<script>
import firebase from "~/plugins/firebase";

export default {
  data() {
    return {
      authUser: {
        uid: ""
      }
    };
  },
  created() {
    var user = firebase.auth().currentUser;
    console.log(user);
    if (user) {
      // User is signed in.
      console.log(user);
      this.authUser.uid = user.uid;
      console.log(this.authUser);
    } else {
      // No user is signed in.
      this.$router.push("/");
    }
  }
};
</script>
