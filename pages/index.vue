<template>
  <div class="container">
    <p class="title is-1 is-spaced">user: {{ $store.getters.getUserName }}</p>
    <button class="button is-primary is-rounded" @click="login">
      ログイン
    </button>
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
        <a class="button is-primary" @click="addTodo"> add </a>
      </p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      newTodo: "",
      newLimit: ""
    };
  },
  methods: {
    login() {
      console.log("login");
      this.$store.dispatch("login"); //index.jsのactionsで定義した、login関数を実行しているだけ。
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
  },
  // computed: {
  //   todosA() {
  //     return this.$store.dispatch("fetchTodos");
  //   }
  // },
  created() {
    this.$store.dispatch("fetchTodos");
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
  background-color: #888888;
}
</style>
