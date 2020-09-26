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
        <h5>マッチングしているユーザー</h5>
        <div v-for="partner in matchedPartnersInfo" :key="partner.index">
          <!-- <p>{{ partner }}</p> -->
          <div class="chat_element">
            <nuxt-link
              :to="{
                path: 'messagedetail/' + loginUser.id + '___' + partner.user_id
              }"
            >
              <div class="partner_image">
                <img :src="partner.profile_images" height="60px" alt="" />
              </div>
              <div class="partner_name">
                <button>{{ partner.display_name }}</button>
                <p>{{ partner.latestMessage.message }}</p>
              </div>
            </nuxt-link>
          </div>
        </div>
        <!--
        <p class="title is-1 is-spaced">user: {{ $store.getters.getUserName }}</p> -->
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
      messages: [],
      loginUserSendLike: [],
      loginUserReceiveLike: [],
      loginUserMatched: [],
      matchedPartnersInfo: []
    };
  },
  mounted: function() {
    // this.$store.state.messages = [];
    firebase.auth().onAuthStateChanged(userAuth => {
      this.isWaiting = false;
      if (userAuth) {
        this.isLogin = true;
        this.loginUserGoogle = userAuth;
        // this.$store.dispatch("fetchmessages");
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
            this.getMatchedPartners();
          });
        })
        .catch(err => {
          console.log("Error getting documents", err);
        });
    },
    getMatchedPartners() {
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
              // asyncとかでなんとかしたいが...
              // console.log(this.loginUserSendLike)
              // console.log(this.loginUserReceiveLike)
              for (let i = 0; i < this.loginUserSendLike.length; i++) {
                if (
                  this.loginUserReceiveLike.includes(this.loginUserSendLike[i])
                ) {
                  this.loginUserMatched.push(this.loginUserSendLike[i]);
                }
              }
              this.fetchMatchedPartnersInfo();
              // this.checkAlreadyMessaged();
            });
        });
    },
    // checkAlreadyMessaged() {},
    fetchMatchedPartnersInfo() {
      for (let i = 0; i < this.loginUserMatched.length; i++) {
        const senderReceiver =
          this.loginUser.id <= this.loginUserMatched[i]
            ? this.loginUser.id + "___" + this.loginUserMatched[i]
            : this.loginUserMatched[i] + "___" + this.loginUser.id;
        // console.log(i);
        // console.log(this.loginUserMatched[i]);
        // console.log(this.matchedPartnersInfo);
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

              // リアルタイム更新にする。
              // 既読/未読判定。 既読フラグをつける。
              // どっちが送ったか書く。
              firebase
                .firestore()
                .collection("messages")
                .where("senderReceiver", "==", senderReceiver)
                .orderBy("createdAt", "desc")
                .limit(1)
                .get()
                .then(snapshot => {
                  snapshot.forEach(doc2 => {
                    // console.log(doc2.id, "=>", doc2.data());
                    matchedPartnerInfo.latestMessage = doc2.data();
                    this.matchedPartnersInfo.push(matchedPartnerInfo);
                  });
                })
                .catch(err2 => {
                  console.log("Error getting documents", err2);
                });
            }
          })
          .catch(err => {
            console.log("Error getting document", err);
          });
      }

      // for (let i = 0; i < this.loginUserMatched.length; i++) {
      //   const senderReceiver =
      //     this.loginUser.id <= this.loginUserMatched[i]
      //       ? this.loginUser.id + "___" + this.loginUserMatched[i]
      //       : this.loginUserMatched[i] + "___" + this.loginUser.id;
      //   firebase
      //     .firestore()
      //     .collection("messages")
      //     .where("senderReceiver", "==", senderReceiver)
      //     .orderBy("createdAt", "desc")
      //     .limit(1)
      //     .get()
      //     .then(snapshot => {
      //       snapshot.forEach(doc => {
      //         console.log(doc.id, "=>", doc.data());
      //       });
      //     })
      //     .catch(err => {
      //       console.log("Error getting documents", err);
      //     });
      // }
      // console.log(this.matchedPartnersInfo);
    }
    // findBy: function(list, value, column1, column2) {
    //   return list.filter(function(item) {
    //     // 入力がない場合は全件表示
    //     // return item[column] == value || value === "";
    //     return item[column1] == value || item[column2] == value;
    //     // return item[column1] == value;
    //   });
    // }
  }
  // filters: {
  //   capitalize: function (value) {
  //     if (!value) return "";
  //     value = value.toString();
  //     return value.charAt(0).toUpperCase() + value.slice(1);
  //   },
  // },
  // computed: {
  //   messages_filtered() {
  //     // return this.$store.state.messages;
  //     return this.findBy(
  //       this.$store.state.messages,
  //       this.loginUserGoogle.email,
  //       // "masaki.hrak@gmail.com",
  //       "sender",
  //       "receiver"
  //     );
  //   }
  // }
};
</script>
<style scoped>
.container {
  margin: 0 auto;
  height: 70vh;
  max-width: 400px;
  /* margin: 0 auto;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  flex-direction: column; */
  /* background-color: #888888; */
  /* color: var(--v-primary-base);
  background-color: var(--v-accent-lighten2); */
}

/* nuxt-linkのunderlineの削除。 */
a {
  text-decoration: none;
}

.chat_element {
  /* width: 300px; */
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
  /* margin: 20px 0px 0px 10px; */
  padding: 30px 0px 0px 10px;
  float: left;
  width: 60%;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}
</style>
