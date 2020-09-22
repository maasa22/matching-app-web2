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
        <!-- <p>{{ loginUserGoogle.email }}でログイン中</p>
        <button @click="logOut" class="logout_btn_class">ログアウト</button>-->
        <h5>マッチングしているユーザー</h5>
        <!-- <div v-for="partner in loginUserMatched" :key="partner.index"> -->
        <div v-for="partner in matchedPartnersInfo" :key="partner.index">
          <div class="chat_element">
            <!-- <nuxt-link :to="{ path: 'message/' + loginUser.id + '___' + partner}">
              <button>{{ partner }} とチャットする。</button>
            </nuxt-link>-->
            <div class="partner_image">
              <img :src="partner.profile_images" height="60px" alt="" />
            </div>
            <div class="partner_name">
              <nuxt-link
                :to="{
                  path:
                    'messagedetail/' + loginUser.id + '___' + partner.user_id
                }"
              >
                <!-- なぜかたまに、リンクが失敗する問題調査する -->
                <button>{{ partner.display_name }}</button>
              </nuxt-link>
            </div>
          </div>
        </div>
        <!-- <p>{{ messages_filtered }}</p>
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

        <!-- <h6 class="sendmsg_class">メッセージを送る。</h6>
        <div class="field is-grouped">
          <p class="control is-expanded">
            <input v-model="newmessage" class="input" type="text" placeholder="message" />
          </p> 
          <p class="control">
            <a class="button is-primary" @click="addmessage">add</a>
        </p>-->
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
      loginUserGoogle: [], //ログインしているユーザーの情報 from google
      loginUser: [], //ログインしているユーザーの情報 from firestore
      newmessage: "",
      newreceiver: "hoge@gmail.com",
      newsender: "hoge@gmail.com",
      messages: [],
      loginUserSendLike: [],
      loginUserReceiveLike: [],
      loginUserMatched: [],
      matchedPartnersInfo: []
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
              this.fetchMatchedPartnersInfo();
              this.checkAlreadyMessaged();
              console.log(this.loginUserMatched);
            });
        });
      // this.getMatchedPartners2();

      //     .where("sender", "==", this.loginUserGoogle.email);
    },
    checkAlreadyMessaged() {},
    fetchMatchedPartnersInfo() {
      for (let i = 0; i < this.loginUserMatched.length; i++) {
        console.log(i);
        console.log(this.loginUserMatched[i]);
        console.log(this.matchedPartnersInfo.length);
        firebase
          .firestore()
          .collection("users")
          .doc(this.loginUserMatched[i])
          .get()
          .then(doc => {
            if (!doc.exists) {
              console.log("No such document!");
            } else {
              let matchedPartnerInfo = doc.data();
              matchedPartnerInfo.user_id = doc.id;
              // console.log(matchedPartnerInfo);
              this.matchedPartnersInfo.push(matchedPartnerInfo);
            }
          })
          .catch(err => {
            console.log("Error getting document", err);
          });
      }
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
      // const sender = this.loginUserGoogle.email;
      const sender = this.loginUser.id;
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
    },
    findBy: function(list, value, column1, column2) {
      return list.filter(function(item) {
        // 入力がない場合は全件表示
        // return item[column] == value || value === "";
        return item[column1] == value || item[column2] == value;
        // return item[column1] == value;
      });
    }
  },
  // filters: {
  //   capitalize: function (value) {
  //     if (!value) return "";
  //     value = value.toString();
  //     return value.charAt(0).toUpperCase() + value.slice(1);
  //   },
  // },
  computed: {
    messages_filtered() {
      // return this.$store.state.messages;
      return this.findBy(
        this.$store.state.messages,
        this.loginUserGoogle.email,
        // "masaki.hrak@gmail.com",
        "sender",
        "receiver"
      );
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

.chat_element {
  width: 300px;
  height: 100px;
  margin: 10px;
  border-radius: 10px;
  background-color: #66bfbf;
  overflow: hidden;
}

.partner_image {
  margin: 20px 0px 20px 20px;
  float: left;
  width: 30%;
}

.partner_name {
  padding: 40px 0px 40px 0px;
  float: left;
  width: 30%;
}
</style>
