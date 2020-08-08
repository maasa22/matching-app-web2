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
        <!-- <button class="button is-primary is-rounded" @click="login">
          ログイン
        </button> -->
        <!-- <p>{{ todosA }}</p> -->
        <table class="table is-narrow">
          <tbody>
            <tr>
              <th>todo</th>
              <th>limit</th>
            </tr>
          </tbody>
          <tbody>
            <tr v-for="todo in $store.getters.getTodos" :key="todo.todo">
              <td>{{ todo.todo }}</td>
              <td>{{ todo.limit }}</td>
            </tr>
          </tbody>
        </table>

        <div class="field is-grouped">
          <p class="control is-expanded">
            <input
              v-model="newTodo"
              class="input"
              type="text"
              placeholder="todo"
            />
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
            <a class="button is-primary" @click="addTodo"> add </a>
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
      newTodo: "",
      newLimit: ""
    };
  },
  // mounted: function() {
  created() {
    firebase.auth().onAuthStateChanged(user => {
      this.isWaiting = false;
      if (user) {
        this.isLogin = true;
        this.user = user;
        this.$store.dispatch("fetchTodos");
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
    addTodo() {
      const doc = firebase.firestore().collection("todos").doc;
      const observer = doc.onSnapshot(
        docSnapshot => {
          console.log(`Received doc snapshot: ${docSnapshot}`);
          // ...
        },
        err => {
          console.log(`Encountered error: ${err}`);
        }
      );

      const todo = this.newTodo;
      const limit = this.newLimit;

      this.$store.dispatch("addTodo", { todo, limit });
      this.newTodo = "";
      this.newLimit = "";
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
