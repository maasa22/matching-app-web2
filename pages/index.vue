<template>
  <div class="container">
    <header class="header">
      <h1>Chat</h1>
      <!-- ログイン時にはフォームとログアウトボタンを表示 -->
      <div v-if="user.uid" key="login">
        [{{ user.displayName }}]
        <button type="button" @click="doLogout">ログアウト</button>
      </div>
      <!-- 未ログイン時にはログインボタンを表示 -->
      <div v-else key="logout">
        <button type="button" @click="doLogin">ログイン</button>
      </div>
    </header>

    <!--　Firebase から取得したリストを描画（トランジション付き）　-->
    <!-- <transition-group name="chat" tag="div" class="list content"> -->

    <section
      v-for="{ key, name, image, message } in chat"
      :key="key"
      class="item"
    >
      <div class="item-image">
        <img :src="image" width="40" height="40" />
      </div>
      <div class="item-detail">
        <div class="item-name">{{ name }}</div>
        <div class="item-message">
          <p>{{ message }}</p>
        </div>
      </div>
    </section>
    <!-- </transition-group> -->

    <!-- 入力フォーム -->
    <form action @submit.prevent="doSend" class="form">
      <textarea
        v-model="input"
        :disabled="!user.uid"
        @keydown.enter.exact.prevent="doSend"
      ></textarea>
      <button type="submit" :disabled="!user.uid" class="send-button">
        Send
      </button>
    </form>
    <!-- <p>hello</p>
    <p>{{ hoge }}</p>-->
    <!-- <p class="title is-1 is-spaced">user: {{ $store.getters }}</p> -->
    <!-- <button class="button is-primary is-rounded" @click="login">
      ログイン
    </button>-->

    <!-- <table class="table is-narrow">
      <thead>
        <tr>
          <th>todo</th>

          <th>limit</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="todo in $store.getters.getTodos" :key="todo.todo">
          <td>{{ todo.todo }}</td>
          <td>{{ todo.limit }}</td>
        </tr>
      </tbody>
    </table>
    <div class="field is-grouped" style="background-color:#222222;">
      <p class="control is-expanded">
        <input v-model="newTodo" class="input" type="text" placeholder="todo" />
      </p>
      <p class="control is-expanded">
        <input
          v-model="newLimit"
          class="input"
          type="text"
          placeholder="limit"
        />
      </p>
      <p class="control">
        <a class="button is-primary" @click="addTodo">
          add
        </a>
      </p>
    </div>-->
    <!-- <button @click="checkLogin">check login</button> -->
  </div>
  <!-- <v-layout
    column
    justify-center
    align-center
  >
    <v-flex
      xs12
      sm8
      md6
    >
      <div class="text-center">
        <logo />
        <vuetify-logo />
      </div>
      <v-card>
        <v-card-title class="headline">
          Welcome to the Vuetify + Nuxt.js template
        </v-card-title>
        <v-card-text>
          <p>Vuetify is a progressive Material Design component framework for Vue.js. It was designed to empower developers to create amazing applications.</p>
          <p>
            For more information on Vuetify, check out the <a
              href="https://vuetifyjs.com"
              target="_blank"
              rel="noopener noreferrer"
            >
              documentation
            </a>.
          </p>
          <p>
            If you have questions, please join the official <a
              href="https://chat.vuetifyjs.com/"
              target="_blank"
              rel="noopener noreferrer"
              title="chat"
            >
              discord
            </a>.
          </p>
          <p>
            Find a bug? Report it on the github <a
              href="https://github.com/vuetifyjs/vuetify/issues"
              target="_blank"
              rel="noopener noreferrer"
              title="contribute"
            >
              issue board
            </a>.
          </p>
          <p>Thank you for developing with Vuetify and I look forward to bringing more exciting features in the future.</p>
          <div class="text-xs-right">
            <em><small>&mdash; John Leider</small></em>
          </div>
          <hr class="my-3">
          <a
            href="https://nuxtjs.org/"
            target="_blank"
            rel="noopener noreferrer"
          >
            Nuxt Documentation
          </a>
          <br>
          <a
            href="https://github.com/nuxt/nuxt.js"
            target="_blank"
            rel="noopener noreferrer"
          >
            Nuxt GitHub
          </a>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn
            color="primary"
            nuxt
            to="/inspire"
          >
            Continue
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>-->
</template>

<script>
// import Logo from "~/components/Logo.vue";
// import VuetifyLogo from "~/components/VuetifyLogo.vue";
import firebase from "~/plugins/firebase";
import "firebase/firestore";

export default {
  // components: {
  //   Logo,
  //   VuetifyLogo
  // },
  data() {
    return {
      hoge: "aaa",
      // newTodo: "",
      // newLimit: ""
      user: {}, // ユーザー情報
      chat: [], // 取得したメッセージを入れる配列
      input: "" // 入力したメッセージ
      // messages_firestore: []
    };
  },
  // methods: {
  // login() {
  //   console.log("login");
  //   this.$store.dispatch("login");
  // },
  // addTodo() {
  //   const todo = this.newTodo;
  //   const limit = this.newLimit;
  //   this.$store.dispatch("addTodo", { todo, limit });
  //   this.newTodo = "";
  //   this.newLimit = "";
  // },
  // checkLogin() {
  //   var user = firebase.auth().currentUser;
  //   console.log(user);
  // }
  // },
  created() {
    console.log(this.$store.state.messages);
    firebase.auth().onAuthStateChanged(user => {
      this.user = user ? user : {};
      // const ref_message = firebase.database().ref("message");
      // const db = firebase.firestore();
      // const ref_message = db.collection("message");
      // console.log(ref_message);
      if (user) {
        this.chat = [];
        const db = firebase.firestore();
        let citiesRef = db.collection("message");
        let allCities = citiesRef
          .get()
          .then(snapshot => {
            snapshot.forEach(doc => {
              console.log(doc.id, "=>", doc.data());
              this.chat.push(doc.data());
            });
          })
          .catch(err => {
            console.log("Error getting documents", err);
          });
        // message に変更があったときのハンドラを登録
        // ref_message.limitToLast(10).on("child_added", this.childAdded);
      } else {
        // message に変更があったときのハンドラを解除
        // ref_message.limitToLast(10).off("child_added", this.childAdded);
      }
    });
  },
  // firestore() {
  //   return {
  //     // firestoreのcommentsコレクションを参照
  //     messages_firestore: firebase
  //       .firestore()
  //       .collection("message")
  //       .orderBy("message")
  //   };
  // },
  methods: {
    // ログイン処理
    doLogin() {
      const provider = new firebase.auth.GoogleAuthProvider();
      firebase.auth().signInWithPopup(provider);
    },
    // ログアウト処理
    doLogout() {
      firebase.auth().signOut();
    },
    // スクロール位置を一番下に移動
    scrollBottom() {
      this.$nextTick(() => {
        window.scrollTo(0, document.body.clientHeight);
      });
    },
    // 受け取ったメッセージをchatに追加
    // データベースに新しい要素が追加されると随時呼び出される
    childAdded(snap) {
      const message = snap.val();
      this.chat.push({
        key: snap.key,
        name: message.name,
        image: message.image,
        message: message.message
      });
      this.scrollBottom();
    },
    async doSend() {
      if (this.user.uid && this.input.length) {
        // firebase にメッセージを追加
        const res = await firebase
          .firestore()
          .collection("message")
          .add({
            message: this.input,
            name: this.user.displayName,
            image: this.user.photoURL
          });
        this.chat.push({
          message: this.input,
          name: this.user.displayName,
          image: this.user.photoURL
        });
        this.input = ""; // フォームを空にする
      }
    }
  }
  // computed: {
  //   computedChat: function() {
  //     return firebase.firestore().collection("message");
  //   }
  // }
  // created() {
  //   firebase.auth().onAuthStateChanged(function(user) {
  //     if (user) {
  //       console.log("ok-");
  //       // $nuxt.$router.push("/inspire");
  //       this.hoge = user.displayName;
  //       this.hoge = "dddd ";
  //       console.log(user);
  //       console.log(user.displayName);
  //     } else {
  //       console.log("nook-");
  //     }
  //   });
  // }
  // mounted() {
  //   firebase.auth().onAuthStateChanged(function(user) {
  //     if (user) {
  //       console.log("ok");
  //       // $nuxt.$router.push("/inspire");
  //     } else {
  //       console.log("nook");
  //       $nuxt.$router.push("/login");
  //     }
  //   });
  //   // this.$store.dispatch("fetchTodos");
  //   // console.log(this.$store.getters.getTodos);
  // }
};
</script>
<style>
/* .container {
  background-color: #aaaaaa;
} */

* {
  margin: 0;
  box-sizing: border-box;
}
.header {
  background: #3ab383;
  margin-bottom: 1em;
  padding: 0.4em 0.8em;
  color: #fff;
}
.content {
  margin: 0 auto;
  padding: 0 10px;
  max-width: 600px;
}
.form {
  position: fixed;
  display: flex;
  justify-content: center;
  align-items: center;
  bottom: 0;
  height: 80px;
  width: 80%;
  background: #f5f5f5;
  margin-bottom: 50px;
}
.form textarea {
  border: 1px solid #ccc;
  border-radius: 2px;
  height: 4em;
  width: calc(100% - 6em);
  resize: none;
}
.list {
  margin-bottom: 100px;
}
.item {
  position: relative;
  display: flex;
  align-items: flex-end;
  margin-bottom: 0.8em;
}
.item-image img {
  border-radius: 20px;
  vertical-align: top;
}
.item-detail {
  margin: 0 0 0 1.4em;
}
.item-name {
  font-size: 75%;
}
.item-message {
  position: relative;
  display: inline-block;
  padding: 0.8em;
  background: #113322;
  border-radius: 4px;
  line-height: 1.2em;
}
.item-message::before {
  position: absolute;
  content: " ";
  display: block;
  left: -16px;
  bottom: 12px;
  border: 4px solid transparent;
  border-right: 12px solid #deefe8;
}
.send-button {
  height: 4em;
  background-color: #339933;
}
/* トランジション用スタイル */
.chat-enter-active {
  transition: all 1s;
}
.chat-enter {
  opacity: 0;
  transform: translateX(-1em);
}
</style>
