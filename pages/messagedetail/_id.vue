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
        <div class="chat_title">
          <div class="btn_talk_list">
            <ul>
              <li>
                <nuxt-link :to="{ path: '../message' }">
                  <!-- <v-btn>トーク一覧へ</v-btn> -->
                  <!-- <v-btn> < </v-btn> -->
                  <v-icon :size="30"> mdi-less-than </v-icon>
                </nuxt-link>
              </li>
            </ul>
          </div>
          <div class="partner_image">
            <img :src="partnerinfo.profile_images" height="30px;" alt="" />
          </div>
          <div class="partner_name">
            <p class="partner_name_p">{{ partnerinfo.display_name }}</p>
          </div>
        </div>
        <div class="msg_history">
          <div v-for="message in messages" :key="message.index">
            <div
              :class="[
                message.sender == loginUser.id ? 'sent_msg' : 'received_msg'
              ]"
            >
              <p class="msg_msg">{{ message.message }}</p>
              <!-- {{ message.message }} -->
            </div>
            <div
              :class="[
                message.sender == loginUser.id
                  ? 'sent_msg_time'
                  : 'received_msg_time'
              ]"
            >
              <p class="msg_time">{{ message.createdAt | formatDate }}</p>
            </div>
          </div>
        </div>
        <div class="input_area">
          <input
            v-model="newmessage"
            class="input"
            type="text"
            placeholder="Type a message"
          />
          <v-btn class="submit_button is-primary" @click="addmessage"
            >送信</v-btn
          >
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import firebase from "@/plugins/firebase";
import GoogleLoginPage from "~/components/GoogleLoginPage.vue";
export default {
  components: {
    GoogleLoginPage
  },
  asyncData() {
    return {
      isWaiting: true,
      isLogin: false,
      loginUserGoogle: [], //ログインしているユーザーの情報 from google
      loginUser: [], //ログインしているユーザーの情報 from firestore
      newmessage: "",
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
          snapshot.forEach(doc => {
            this.loginUser.id = doc.id;
            this.getPartnerId();
          });
        })
        .catch(err => {
          console.log("Error getting documents", err);
        });
    },
    getPartnerId: function() {
      this.partnerId = this.$route.path
        .split("messagedetail/")[1]
        .split("___")[1];
      this.fetchMessage();
      this.fetchPartnerInfo();
    },
    fetchMessage() {
      // let senderReceiver = "";
      // if (this.loginUser.id <= this.partnerId) {
      //   senderReceiver = this.loginUser.id + "___" + this.partnerId;
      // } else {
      //   senderReceiver = this.partnerId + "___" + this.loginUser.id;
      // }
      const senderReceiver =
        this.loginUser.id <= this.partnerId
          ? this.loginUser.id + "___" + this.partnerId
          : this.partnerId + "___" + this.loginUser.id;
      firebase
        .firestore()
        .collection("messages")
        .where("senderReceiver", "==", senderReceiver)
        .orderBy("createdAt")
        .onSnapshot(snapshot => {
          let changes = snapshot.docChanges();
          changes.forEach(change => {
            if (change.type == "added") {
              let newmessage = change.doc.data();
              newmessage.message_id = change.doc.id;
              this.messages.push(newmessage);
            } else if (change.type == "removed") {
              for (let i = 0; i < this.messages.length; i++) {
                if (this.messages[i].message_id == change.doc.id) {
                  this.messages.splice(i, 1);
                  break;
                }
              }
            }
            setTimeout(() => {
              this.scrollToBottom();
            }, 300); // 更新があったら、rendering用の時間を若干待ってから下にスクロール。
          });
        });
      setTimeout(() => {
        this.scrollToBottom();
      }, 1000); // 初回に全部読み込んだら、rendering用の時間を若干待ってから下にスクロール。
    },
    // エラーがでとるな。。
    scrollToBottom() {
      let box = document.querySelector(".msg_history");
      if (box) {
        box.scrollTop = box.scrollHeight;
      }
    },
    fetchPartnerInfo() {
      firebase
        .firestore()
        .collection("users")
        .doc(this.partnerId)
        .get()
        .then(doc => {
          if (!doc.exists) {
            console.log("No such document!");
          } else {
            this.partnerinfo = doc.data();
          }
        })
        .catch(err => {
          console.log("Error getting document", err);
        });
    },
    addmessage() {
      const message = this.newmessage;
      const sender = this.loginUser.id;
      const receiver = this.partnerId;
      // let senderReceiver = "";
      // if (this.loginUser.id <= this.partnerId) {
      //   senderReceiver = this.loginUser.id + "___" + this.partnerId;
      // } else {
      //   senderReceiver = this.partnerId + "___" + this.loginUser.id;
      // }
      const senderReceiver =
        this.loginUser.id <= this.partnerId
          ? this.loginUser.id + "___" + this.partnerId
          : this.partnerId + "___" + this.loginUser.id;
      const createdAt = new Date();
      // **index.jsを使わない版**
      firebase
        .firestore()
        .collection("messages")
        .add({
          message: message,
          sender: sender,
          receiver: receiver,
          createdAt: createdAt,
          senderReceiver: senderReceiver
        });
      // **vuex使う版**
      // this.$store.dispatch("addmessage", {
      //   message,
      //   sender,
      //   receiver,
      //   senderReceiver,
      //   createdAt
      // });
      this.newmessage = "";
      setTimeout(() => {
        this.scrollToBottom();
      }, 300); //rendering用の時間を若干待ってから下にスクロール。
    }
  },
  filters: {
    formatDate: function(value) {
      let a = new Date(value.seconds * 1000);
      let year = ("0000" + a.getFullYear()).slice(-4);
      let month = ("00" + String(Number(a.getMonth()) + 1)).slice(-2);
      let date = ("00" + a.getDate()).slice(-2);
      let hour = ("00" + a.getHours()).slice(-2);
      let min = ("00" + a.getMinutes()).slice(-2);
      let sec = ("00" + a.getSeconds()).slice(-2);
      let time = month + "/" + date + " " + hour + ":" + min;
      return time;
    }
  }
};
</script>
<style scoped>
.container {
  /* margin: 0 auto; */
  height: 70vh;
  max-width: 400px;
  /* min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  flex-direction: column; */
  /* background-color: #888888; */
  /* color: var(--v-primary-base);
  background-color: var(--v-accent-lighten2); */
}

.chat_title {
  margin: 0px 0px 4px 0px;
  overflow: hidden;
  height: 10%;
}

.btn_talk_list {
  float: left;
  /* width: 30%; */
}

ul {
  list-style: none;
  padding-left: 0;
}

li a {
  text-decoration: none;
}

.partner_image {
  float: left;
  margin: 0px 0px 0px 30px;
  /* width: 30%; */
  text-align: left;
}

.partner_name {
  float: left;
  margin: 0px 0px 0px 10px;
  /* width: 40%; */
}

.partner_name_p {
  text-align: left;
  /* padding: 0px 100px 0px 0px; */
}

.msg_history {
  /* height: 500px; */
  height: 82%;
  margin: 0px 0px 4px 0px;
  overflow-y: auto;
  border-radius: 10px;
  border: 1px dotted #66bfbf;
}

.sent_msg {
  margin: 2px 10px 2px 0px;
  padding: 10px;
  text-align: left;
  width: 80%;
  /* height: 100px; */
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
  /* height: 100px; */
  background-color: #e0ece4;
  border-radius: 10px;
  float: left;
  clear: both;
  word-wrap: break-word;
}

.sent_msg_time {
  margin: 0px 10px 4px 0px;
  padding: 0px 0px 0px 5px;
  text-align: left;
  width: 80%;
  height: 20px;
  float: right;
  clear: both;
  text-align: right;
  word-wrap: break-word;
}

.received_msg_time {
  margin: 0px 0px 4px 10px;
  padding: 0px 0px 0px 5px;
  text-align: left;
  width: 80%;
  height: 20px;
  float: left;
  clear: both;
  text-align: right;
  word-wrap: break-word;
}

.input_area {
  height: 8%;
  /* position: absolute;
  bottom: 15px; */
  /* max-width: 100vw; */
}
.input {
  margin: 0px 0px 0px 0px;
  /* height: 10%; */
}

.submit_button {
  margin: 0px 10px 0px 0px;
}
</style>
