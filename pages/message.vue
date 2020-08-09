<template>
  <div class="container">
    <div v-if="isWaiting">
      <p>読み込み中</p>
    </div>
    <div v-else>
      <div v-if="!isLogin">
        <button @click="googleLogin">Googleでログイン</button>
      </div>
      <div v-else>
        <p>{{ user.email }}でログイン中</p>
        <button @click="logOut">ログアウト</button>
        <p class="title is-1 is-spaced">
          user: {{ $store.getters.getUserName }}
        </p>
        <table class="table is-narrow">
          <tbody>
            <tr>
              <th>message</th>
            </tr>
          </tbody>
          <tbody>
            <tr
              v-for="message in $store.getters.getmessages"
              :key="message.message"
            >
              <td>{{ message }}</td>
              <!-- <td>{{ message.email }}</td> -->
            </tr>
          </tbody>
        </table>

        <div class="field is-grouped">
          <p class="control is-expanded">
            <input
              v-model="newmessage"
              class="input"
              type="text"
              placeholder="message"
            />
          </p>

          <!-- <p class="control is-expanded">
            <input
              v-model="newemail"
              class="input"
              type="text"
              placeholder="email"
            />
          </p> -->

          <p class="control">
            <a class="button is-primary" @click="addmessage"> add </a>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import firebase from "@/plugins/firebase";

export default {
  asyncData() {
    return {
      isWaiting: true,
      isLogin: false,
      user: [],
      newmessage: "",
      newreceiver: "hoge@gmail.com",
      newsender: "hoge@gmail.com"
      // newemail: ""
    };
  },
  // mounted: function() {
  created() {
    // this.$store.state.messages = [];
    firebase.auth().onAuthStateChanged(user => {
      this.isWaiting = false;
      if (user) {
        this.isLogin = true;
        this.user = user;
        this.$store.dispatch("fetchmessages");
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
    },
    addmessage() {
      // const doc = firebase.firestore().collection("messages").doc;
      // const observer = doc.onSnapshot(
      //   docSnapshot => {
      //     console.log(`Received doc snapshot: ${docSnapshot}`);
      //     // ...
      //   },
      //   err => {
      //     console.log(`Encountered error: ${err}`);
      //   }
      // );

      const message = this.newmessage;
      // const sender = this.newsender;
      const sender = this.user.email;
      const receiver = this.newreceiver;
      const today = new Date();
      // const date =
      //   today.getFullYear() +
      //   "-" +
      //   (today.getMonth() + 1) +
      //   "-" +
      //   today.getDate();
      // const time =
      //   today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
      // const createdAt = date + " " + time;
      const createdAt = today;
      // const email = this.newemail;
      console.log(message, sender, receiver, createdAt);
      this.$store.dispatch("addmessage", {
        message,
        sender,
        receiver,
        createdAt
      });
      this.newmessage = "";
      // this.newemail = "";
    }
  }
};
</script>
<style>
.container {
  margin: 0 auto;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  flex-direction: column;
  /* background-color: #888888; */
  /* color: var(--v-primary-base);
  background-color: var(--v-accent-lighten2); */
}
</style>
