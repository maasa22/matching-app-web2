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
        <nuxt-link :to="{ path: '../message' }">
          <button>戻る</button>
        </nuxt-link>

        <p></p>
        <input
          v-model="newmessage"
          class="input"
          type="text"
          placeholder="message"
        />
        <a class="button is-primary" @click="addmessage">add</a>
      </div>
    </div>
  </div>
</template>

<script>
import firebase from "@/plugins/firebase";
import moment from "moment";

export default {
  asyncData() {
    return {
      isWaiting: true,
      isWaiting2: true,
      isLogin: false,
      loginUserGoogle: [], //ログインしているユーザーの情報 from google
      loginUser: [], //ログインしているユーザーの情報 from firestore
      newmessage: "",
      newreceiver: "hoge@gmail.com",
      newsender: "hoge@gmail.com",
      messages: [],
      loginUserSendLike: [],
      loginUserReceiveLike: [],
      loginUserMatched: [],
      partnerId: ""
      // newemail: ""
    };
  },
  // mounted: function() {
  mounted: function() {
    // this.$store.state.messages = [];
    firebase.auth().onAuthStateChanged(userAuth => {
      this.isWaiting = false;
      if (userAuth) {
        this.isLogin = true;
        this.loginUserGoogle = userAuth;
        this.$store.dispatch("fetchmessages");
        this.checkFirstTime();
        this.getPartnerId();
        this.fetchmessage();
      } else {
        this.isLogin = false;
        this.loginUserGoogle = [];
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
    getPartnerId: function() {
      this.partnerId = this.$route.path
        .split("messagedetail/")[1]
        .split("___")[1]; //ex. /user/71beb69945ae4
      console.log(this.partnerId);
    },
    checkFirstTime() {
      let loginUser = firebase
        .firestore()
        .collection("users")
        .where("mail", "==", this.loginUserGoogle.email)
        // .where("mail", "==", "hoge@gmail.com")
        .get()
        .then(snapshot => {
          if (snapshot.empty) {
            //if first time, go to register page
            console.log("No matching documents.");
            this.$router.push("/register");
          }
          snapshot.forEach(doc => {
            // ログインユーザーのID
            this.loginUser.id = doc.id;
            this.getMatchedPartners();
          });
        })
        .catch(err => {
          console.log("Error getting documents", err);
        });
    },
    getMatchedPartners() {
      console.log(this.loginUserGoogle.email);
      let loginUserSendLike = firebase
        .firestore()
        .collection("likes")
        .where("sender", "==", this.loginUser.id)
        .get()
        .then(snapshot => {
          if (snapshot.empty) {
            console.log("still no matches");
          } else {
            snapshot.forEach(doc => {
              this.loginUserSendLike.push(doc.data().receiver);
            });
          }
          let loginUserReceiveLike = firebase
            .firestore()
            .collection("likes")
            .where("receiver", "==", this.loginUser.id)
            .get()
            .then(snapshot => {
              if (snapshot.empty) {
                console.log("still no matches");
              } else {
                snapshot.forEach(doc => {
                  this.loginUserReceiveLike.push(doc.data().sender);
                });
              }
              // console.log("send", this.loginUserSendLike);
              // console.log("receive", this.loginUserReceiveLike);

              for (let i = 0; i < this.loginUserSendLike.length; i++) {
                if (
                  this.loginUserReceiveLike.includes(this.loginUserSendLike[i])
                ) {
                  this.loginUserMatched.push(this.loginUserSendLike[i]);
                }
              }
              console.log(this.loginUserMatched);
            });
        });
      // this.getMatchedPartners2();

      //     .where("sender", "==", this.loginUserGoogle.email);
    },
    fetchmessage() {
      const db = firebase.firestore();
      const messageRef = db.collection("messages");
      messageRef.orderBy("message").onSnapshot(snapshot => {
        let changes = snapshot.docChanges();
        //console.log(changes);
        changes.forEach(change => {
          //console.log(change);
          if (change.type == "added") {
            //console.log("added", change.doc.id, change.doc.data());
            // commit("addmessage", [change.doc.id, change.doc.data()]);
            messageRef
              .add({
                message: change.doc.data().message,
                sender: change.doc.data().sender,
                receiver: change.doc.data().receiver,
                createdAt: change.doc.data().createdAt,
                sender_receiver: change.doc.data().sender_receiver
              })
              .then(function(docRef) {
                // console.log("Document written with ID: ", docRef.id);
                // commit("addmessage", id_message);
              })
              .catch(function(error) {
                // console.error("Error adding document: ", error);
              });
            //   state.messages.push(change.doc.data());
          } else if (change.type == "removed") {
            //console.log("removed", change.doc.id, change.doc.data());
            //commit("deletemessage", change.doc.id);
            console.log("deletemessage作る！");
          }
        });
        //   console.log(changes);
      });
    },

    addmessage() {
      const message = this.newmessage;
      const sender = this.loginUser.id;
      const receiver = this.partnerId;
      let sender_receiver = "";
      if (this.loginUser.id <= this.partnerId) {
        sender_receiver = this.loginUser.id + "___" + this.partnerId;
      } else {
        sender_receiver = this.partnerId + "___" + this.loginUser.id;
      }
      const today = new Date();
      const createdAt = today;
      console.log(message, sender, receiver, sender_receiver, createdAt);
      this.$store.dispatch("addmessage", {
        message,
        sender,
        receiver,
        sender_receiver,
        createdAt
      });
      this.newmessage = "";
    }
  },
  filters: {
    formatDate: function(value) {
      // if (value) {
      //   return moment(String(value)).format("MM/DD/YYYY hh:mm");
      // }
      let a = new Date(value.seconds * 1000);
      let year = a.getFullYear();
      let month = a.getMonth();
      let date = a.getDate();
      let hour = a.getHours();
      let min = a.getMinutes();
      let sec = a.getSeconds();
      // let time = year + "/" + month + "/" + date + " " + hour + ":" + min;
      let time = month + "/" + date + " " + hour + ":" + min;
      return time;
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

.sendmsg_class {
  margin-top: 50px;
}

.logout_btn_class {
  margin-bottom: 50px;
}

.chat_element {
  width: 300px;
  height: 200px;
  margin: 10px;
  background-color: cadetblue;
}

.sent_msg {
  width: 200px;
  height: 200px;
  background-color: #888822;
}

.received_msg {
  width: 200px;
  height: 200px;
  background-color: #228822;
}
</style>
