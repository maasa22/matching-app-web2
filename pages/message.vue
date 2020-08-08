<template>
  <div>
    <!-- <p>{{ $store.getters }}</p> -->
    <p>hello</p>
    <p>{{ authUser }}</p>
    <!-- <p>{{ this.authUser.displayName }}</p> -->
  </div>
</template>

<script>
import firebase from "~/plugins/firebase";

export default {
  data() {
    return {
      //   authUser: {
      //     uid: ""
      // };
      authUser: ""
    };
  },
  created() {
    //mounted() {
    firebase.auth().onAuthStateChanged(function(user) {
      if (user) {
        // this.authUser.uid = use.uid;
        this.authUser = user.uid;
        console.log(user);
        console.log(user.uid);
        console.log("ok");
      } else {
        console.log("nook");
        // $nuxt.$router.push("/login");
      }
    });
  }
};
</script>
