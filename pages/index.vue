<template>
  <div class="container">
    <p>hello</p>
    <!-- <p class="title is-1 is-spaced">user: {{ $store.getters }}</p> -->
    <!-- <button class="button is-primary is-rounded" @click="login">
      ログイン
    </button> -->

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
    </div> -->
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
  </v-layout> -->
</template>

<script>
// import Logo from "~/components/Logo.vue";
// import VuetifyLogo from "~/components/VuetifyLogo.vue";
import firebase from "~/plugins/firebase";

export default {
  // components: {
  //   Logo,
  //   VuetifyLogo
  // },
  data() {
    return {
      // newTodo: "",
      // newLimit: ""
    };
  },
  methods: {
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
  },
  mounted() {
    firebase.auth().onAuthStateChanged(function(user) {
      if (user) {
        console.log("ok");
        // $nuxt.$router.push("/inspire");
      } else {
        console.log("nook");
        $nuxt.$router.push("/login");
      }
    });
    // this.$store.dispatch("fetchTodos");
    // console.log(this.$store.getters.getTodos);
  }
};
</script>
