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
        <div class="chat_title">
          <div class="btn_talk_list">
            <nuxt-link :to="{ path: '../message' }">
              <v-btn>トーク一覧へ</v-btn>
            </nuxt-link>
          </div>
          <div class="partner_name">
            <p class="partner_name_p">{{ partnerinfo.display_name }}</p>
          </div>
          <div class="partner_image">
            <img :src="partnerinfo.profile_images" height="30px;" alt="" />
          </div>
        </div>
        <div class="msg_history">
          <div v-for="message in messages" :key="message.index">
            <div
              :class="[
                message.sender == loginUser.id ? 'sent_msg' : 'received_msg'
              ]"
            >
              <!-- <p classs="msg_msg">{{ message.message }}</p> -->
              {{ message.message }}
            </div>
            <div
              :class="[
                message.sender == loginUser.id ? 'sent_msg2' : 'received_msg2'
              ]"
            >
              <p class="msg_time">{{ message.createdAt | formatDate }}</p>
            </div>
          </div>
        </div>
        <input
          v-model="newmessage"
          class="input"
          type="text"
          placeholder="Type a message"
        />
        <a class="button is-primary" @click="addmessage">送信</a>
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
      partnerId: "",
      partnerinfo: []
    };
  },
  mounted: function() {
    firebase.auth().onAuthStateChanged(userAuth => {
      this.isWaiting = false;
      if (userAuth) {
        this.isLogin = true;
        this.loginUserGoogle = userAuth;
        this.checkFirstTime();
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
      this.fetchmessage();
      this.fetchpartnerinfo();
    },
    scrollToBottom() {
      let box = document.querySelector(".msg_history");
      box.scrollTop = box.scrollHeight;
    },
    fetchpartnerinfo() {
      console.log(this.partnerId);
      let loginUser = firebase
        .firestore()
        .collection("users")
        .doc(this.partnerId)
        .get()
        .then(doc => {
          if (!doc.exists) {
            console.log("No such document!");
          } else {
            // console.log("Document data:", doc.data());
            this.partnerinfo = doc.data();
          }
        })
        .catch(err => {
          console.log("Error getting document", err);
        });
    },
    checkFirstTime() {
      let loginUser = firebase
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
          snapshot.forEach(doc => {
            // ログインユーザーのID
            this.loginUser.id = doc.id;
            this.getPartnerId();
          });
        })
        .catch(err => {
          console.log("Error getting documents", err);
        });
    },
    fetchmessage() {
      let sender_receiver = "";
      if (this.loginUser.id <= this.partnerId) {
        sender_receiver = this.loginUser.id + "___" + this.partnerId;
      } else {
        sender_receiver = this.partnerId + "___" + this.loginUser.id;
      }
      firebase
        .firestore()
        .collection("messages")
        // .where("sender", "==", this.loginUser.id)
        // .where("receiver", "==", this.partnerId)
        .where("sender_receiver", "==", sender_receiver)
        .orderBy("createdAt")
        .onSnapshot(snapshot => {
          let changes = snapshot.docChanges();
          changes.forEach(change => {
            if (change.type == "added") {
              //console.log("added", change.doc.id, change.doc.data());
              let newmessage = change.doc.data();
              newmessage.message_id = change.doc.id;
              this.messages.push(newmessage);
            } else if (change.type == "removed") {
              //console.log("removed", change.doc.id, change.doc.data());
              for (let i = 0; i < this.messages.length; i++) {
                //console.log(i, this.messages[i].message_id, change.doc.id);
                if (this.messages[i].message_id == change.doc.id) {
                  this.messages.splice(i, 1);
                  break;
                }
              }
            }
            setTimeout(() => {
              console.log("World!");
              this.scrollToBottom();
            }, 200);
          });
        });
      setTimeout(() => {
        console.log("World!");
        this.scrollToBottom();
      }, 1000); //sleepするとうまく行きそう。
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
      setTimeout(() => {
        console.log("World!");
        this.scrollToBottom();
      }, 300); //sleepするとうまく行きそう。
    }
  },
  filters: {
    formatDate: function(value) {
      // if (value) {
      //   return moment(String(value)).format("MM/DD/YYYY hh:mm");
      // }
      let a = new Date(value.seconds * 1000);
      let year = ("0000" + a.getFullYear()).slice(-4);
      let month = ("00" + a.getMonth()).slice(-2);
      let date = ("00" + a.getDate()).slice(-2);
      let hour = ("00" + a.getHours()).slice(-2);
      let min = ("00" + a.getMinutes()).slice(-2);
      let sec = ("00" + a.getSeconds()).slice(-2);
      // let time = year + "/" + month + "/" + date + " " + hour + ":" + min;
      let time = month + "/" + date + " " + hour + ":" + min;
      return time;
    }
  }
};
</script>
<style scoped>
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

.sent_msg {
  margin: 2px 10px 2px 0px;
  padding: 10px;
  text-align: left;
  width: 80%;
  height: 100px;
  background-color: #66bfbf;
  border-radius: 10px;
  float: right;
  clear: both;
  word-wrap: break-word;
}

.received_msg {
  margin: 2px 0px 2px 10px;
  /* padding: 10px 10px 10px 10px; */
  padding: 10px;
  text-align: left;
  width: 80%;
  height: 100px;
  background-color: #e0ece4;
  border-radius: 10px;
  float: left;
  clear: both;
  word-wrap: break-word;
}

.msg_history {
  /* height: 500px; */
  height: 500px;
  overflow-y: auto;
  border-radius: 10px;
  border: 1px dotted #66bfbf;
}

.sent_msg2 {
  margin: 2px 10px 10px 0px;
  padding: 0px 0px 0px 5px;
  text-align: left;
  width: 80%;
  height: 30px;
  float: right;
  clear: both;
  text-align: right;
  word-wrap: break-word;
}

.received_msg2 {
  margin: 2px 0px 10px 10px;
  padding: 0px 0px 0px 5px;
  text-align: left;
  width: 80%;
  height: 30px;
  float: left;
  clear: both;
  text-align: right;
  word-wrap: break-word;
}

.chat_title {
  margin: 0px 0px 50px 0px;
  overflow: hidden;
}

.btn_talk_list {
  float: left;
  width: 30%;
}

.partner_name {
  float: left;
  width: 30%;
}

.partner_name_p {
  width: 50px;
  /* padding: 0px 100px 0px 0px; */
}

.partner_image {
  float: right;
  width: 40%;
  text-align: right;
}
/* .partner_name {
  float: right;
  clear: both;
  text-align: left;
} */

.input {
  margin: 30px 0px 0px 0px;
}
/* .msg_msg {
  width: 80%;
  float: left;
  clear: both;
}

.msg_time {
  width: 20%;
  float: right;
  clear: both;
} */
</style>
