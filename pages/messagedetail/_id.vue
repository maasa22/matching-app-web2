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

        <h3>{{ partnerId }}</h3>
        <!-- <p>{{ messages_filtered }}</p> -->
        <div v-for="message in messages_filtered" :key="message.index">
          <div
            :class="[
              message.sender == loginUser.id ? 'sent_msg' : 'received_msg'
            ]"
          ></div>
          <!-- computedが何か処理しないと動かねぇ... 1回mountedのタイミングで実行して初期値入れると良いのかも!?-->
          <!-- | で後に関数挟むとかもありかも。-->
          <p>{{ message.sender }}</p>
          <p>{{ message.message }} {{ message.createdAt | formatDate }}</p>
        </div>
        <!-- 
        <p class="title is-1 is-spaced">user: {{ $store.getters.getUserName }}</p>
        <table class="table is-narrow">
          <tbody>
            <tr>
              <th>receiver</th>
              <th>sender</th>
              <th>createdAt</th>
              <th>message</th>
              <th>message_id</th>
            </tr>
          </tbody>
          <tbody>
            <tr v-for="message in $store.getters.getmessages" :key="message.message">
              <td>{{ message.receiver }}</td>
              <td>{{ message.sender }}</td>
              <td>{{ message.createdAt }}</td>
              <td>{{ message.message}}</td>
              <td>{{ message.message_id }}</td>
            </tr>
          </tbody>
        </table>-->
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
              this.checkAlreadyMessaged();
              console.log(this.loginUserMatched);
            });
        });
      // this.getMatchedPartners2();

      //     .where("sender", "==", this.loginUserGoogle.email);
    },
    compare(a, b) {
      const genreA = a.createdAt;
      const genreB = b.createdAt;

      let comparison = 0;
      if (genreA > genreB) {
        comparison = 1;
      } else if (genreA < genreB) {
        comparison = -1;
      }
      return comparison;
    },
    checkAlreadyMessaged() {},
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
      // const sender = this.loginUserGoogle.email;
      const sender = this.loginUser.id;
      const receiver = this.partnerId;
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
    },
    // 自分が送って相手が受け取ったメッセージのみ獲得する。
    findBy: function(list, loginUser, partner) {
      return list.filter(function(item) {
        // 入力がない場合は全件表示
        return item["receiver"] == partner || item["sender"] == loginUser;
        // return item[column1] == value;
      });
    },
    findBy2: function(list, loginUser, partner) {
      return list.filter(function(item) {
        // 入力がない場合は全件表示
        return item["sender"] == partner || item["receiver"] == loginUser;
        // return item[column1] == value;
      });
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
  },
  computed: {
    //これ絶対遅いな。これ専用のreal time database作ってsnapshotで最新の更新持ってくる方が良い気がする。
    messages_filtered() {
      let messages_from_partners =
        // return this.$store.state.messages;
        this.findBy(
          this.$store.state.messages,
          this.loginUser.id,
          this.partnerId
        );
      let messages_from_loginUser = this.findBy2(
        this.$store.state.messages,
        this.loginUser.id,
        this.partnerId
      );
      let messages = messages_from_partners.concat(messages_from_loginUser);
      messages.sort(this.compare);
      // this.isWaiting2 = false;
      return messages;
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
