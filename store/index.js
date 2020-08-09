import firebase from "~/plugins/firebase";

const db = firebase.firestore();
const messageRef = db.collection("messages");

export const state = () => ({
  userUid: "",
  userName: "",
  messages: []
});

export const mutations = {
  setUserUid(state, userUid) {
    state.userUid = userUid;
  },
  setUserName(state, userName) {
    state.userName = userName;
  },
  addmessage(state, id_message) {
    console.log("inside a mutations");
    state.messages.push(id_message);
  },
  deletemessage(state, id) {
    for (let i = 0; i < state.messages.length; i++) {
      state.messages.splice(i, 1);
      break;
    }
  },
  clearmessage(state) {
    state.messages = [];
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
  fetchmessages({ commit }) {
    commit("clearmessage");
    messageRef.orderBy("message").onSnapshot(snapshot => {
      let changes = snapshot.docChanges();
      //console.log(changes);
      changes.forEach(change => {
        //console.log(change);
        if (change.type == "added") {
          //console.log("added", change.doc.id, change.doc.data());
          commit("addmessage", change.doc.data());
          //   state.messages.push(change.doc.data());
        } else if (change.type == "removed") {
          //console.log("removed", change.doc.id, change.doc.data());
          commit("deletemessage", change.doc.id);
        }
      });
      //   console.log(changes);
    });
  },
  addmessage({ commit }, id_message) {
    console.log(id_message);
    messageRef
      .add({
        message: id_message.message,
        sender: id_message.sender,
        receiver: id_message.receiver
      })
      .then(function(docRef) {
        // console.log("Document written with ID: ", docRef.id);
        // commit("addmessage", id_message);
      })
      .catch(function(error) {
        // console.error("Error adding document: ", error);
      });
  },
  deletemessage({ commit }, id) {
    console.log("aaaaa");
    messageRef.doc(id).delete();
    then(function(docRef) {
      // console.log("Document written with ID: ", docRef.id);
      commit("deletemessage", id); //これもいらん気がする!?
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
  getmessages(state) {
    return state.messages;
  }
};
