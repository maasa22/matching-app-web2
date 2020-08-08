import firebase from "~/plugins/firebase";

const db = firebase.firestore();
const todoRef = db.collection("todos");

export const state = () => ({
  userUid: "",
  userName: "",
  todos: []
});

export const mutations = {
  setUserUid(state, userUid) {
    state.userUid = userUid;
  },
  setUserName(state, userName) {
    state.userName = userName;
  },
  addTodo(state, id_todo) {
    state.todos.push(id_todo[1]);
  },
  deleteTodo(state, id) {
    for (let i = 0; i < state.todos.length; i++) {
      state.todos.splice(i, 1);
      break;
    }
  },
  clearTodo(state) {
    state.todos = [];
  }
};

export const actions = {
  login({ commit }) {
    console.log("login action");
    const provider = new firebase.auth.GoogleAuthProvider();
    firebase
      .auth()
      .signInWithPopup(provider)
      .then(function(result) {
        const user = result.user;
        // console.log("success : " + user.uid + " : " + user.displayName);
        commit("setUserUid", user.uid);
        commit("setUserName", user.displayName);
      })
      .catch(function(error) {
        var errorCode = error.code;
        // console.log("error : " + errorCode);
      });
  },
  fetchTodos({ commit }) {
    commit("clearTodo");
    todoRef.orderBy("todo").onSnapshot(snapshot => {
      let changes = snapshot.docChanges();
      //console.log(changes);
      changes.forEach(change => {
        //console.log(change);
        if (change.type == "added") {
          //console.log("added", change.doc.id, change.doc.data());
          commit("addTodo", [change.doc.id, change.doc.data()]);
          //   state.todos.push(change.doc.data());
        } else if (change.type == "removed") {
          //console.log("removed", change.doc.id, change.doc.data());
          commit("deleteTodo", change.doc.id);
        }
      });
      //   console.log(changes);
    });
  },
  addTodo({ commit }, id_todo) {
    // console.log(todo);
    todoRef
      .add({
        id: id_todo[0],
        todo: id_todo[1].todo,
        limit: id_todo[1].limit
      })
      .then(function(docRef) {
        // console.log("Document written with ID: ", docRef.id);
        commit("addTodo", id_todo[1]);
      })
      .catch(function(error) {
        // console.error("Error adding document: ", error);
      });
  },
  deleteTodo({ commit }, id) {
    console.log("aaaaa");
    todoRef.doc(id).delete();
    then(function(docRef) {
      // console.log("Document written with ID: ", docRef.id);
      commit("deleteTodo", id);
    }).catch(function(error) {
      // console.error("Error adding document: ", error);
    });
  }
};

export const getters = {
  getUserUid(state) {
    return state.userUid;
  },
  getUserName(state) {
    return state.userName;
  },
  getTodos(state) {
    return state.todos;
  }
};
