<template>
  <div class="googleLogin">
    <div class="buttonLogin">
      <v-btn @click="googleLogin">Googleでログイン <br />または新規登録</v-btn>
    </div>
    <!-- <div>
      <nuxt-link :to="{ path: 'register' }">
        <v-btn>新規登録ページへ</v-btn>
      </nuxt-link>
    </div> -->
    <!-- <div class="buttonRegister">
      <nuxt-link to="/register">
        <v-btn>新規登録</v-btn>
      </nuxt-link>
    </div> -->
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
<style scoped>
.googleLogin {
  margin: 30% auto;
  text-align: center;
}

a {
  text-decoration: none;
}

.buttonLogin {
  margin: 20px;
}

.buttonRegisrer {
  margin: 20px;
}
</style>
