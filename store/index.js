import firebase from "~/plugins/firebase";

const db = firebase.firestore();
const todoRef = db.collection("todos");

export const state = () => ({
  userUid: "",
  userName: "",
  todos: []
});

// todoRef.orderBy("todo").onSnapshot(snapshot => {
//   let changes = snapshot.docChanges();
//   changes.forEach(change => {
//     if ((change.type = "added")) {
//       console.log("added", change.doc.id, change.doc.data());
//       //   state.todos.push(change.doc.data());
//     } else if (change.type == "removed") {
//       console.log("removed", change.doc.id, change.doc.data());
//     }
//   });
//   //   console.log(changes);
// });

export const mutations = {
  setUserUid(state, userUid) {
    state.userUid = userUid;
  },
  setUserName(state, userName) {
    state.userName = userName;
  },
  addTodo(state, todo) {
    state.todos.push(todo);
  },
  deleteTodo(state, id) {
    console.log("ccc");
    console.log(state.todos, id);
  },
  clearTodo(state) {
    state.todo = [];
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
    todoRef
      //   .get()
      //   .then(res => {
      //     res.forEach(doc => {
      //       //   console.log("success : " + `${doc.id} => ${doc.data()}`);
      //       commit("addTodo", doc.data());
      //     });
      //   })
      //   .catch(error => {
      //     // console.log("error : " + error);
      //   })
      .orderBy("todo")
      .onSnapshot(snapshot => {
        let changes = snapshot.docChanges();
        console.log(changes);
        changes.forEach(change => {
          console.log(change);
          if (change.type == "added") {
            console.log("added", change.doc.id, change.doc.data());
            commit("addTodo", change.doc.data());
            //   state.todos.push(change.doc.data());
          } else if (change.type == "removed") {
            console.log("bbbb");
            console.log("removed", change.doc.id, change.doc.data());
            commit("deleteTodo", change.doc.id);
          }
        });
        //   console.log(changes);
      });
  },
  addTodo({ commit }, todo) {
    // console.log(todo);
    todoRef
      .add({
        todo: todo.todo,
        limit: todo.limit
      })
      .then(function(docRef) {
        // console.log("Document written with ID: ", docRef.id);
        commit("addTodo", todo);
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
