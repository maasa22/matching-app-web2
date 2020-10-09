<template>
  <div>
    <div v-if="isWaiting">
      <p>読み込み中</p>
    </div>
    <div v-else>
      <div v-if="!isLogin">
        <!-- <button @click="googleLogin">Googleでログイン</button> -->
        <GoogleLoginPage />
      </div>
      <div v-else class="container">
        <v-card class="mx-auto" max-width="344">
          <v-img :src="user.profile_images" height="250px"></v-img>
          <div v-if="profile_images_editing">
            <label class="postImage-appendBtn">
              <!-- この辺りだけ変更が必要！ あと画像のトリミング！ -->
              <input @change="upload" type="file" data-label="画像の添付" />
            </label>
            <v-icon
              @click="cancel_editing_profile_images"
              middle
              color="green darken-2"
              class="edit_icon"
            >
              mdi-close
            </v-icon>
            <!-- <v-btn class="cancel_btn" @click="cancel_editing_profile_images"
              >キャンセル</v-btn
            > -->
          </div>
          <div v-else>
            <v-icon
              @click="start_editing_profile_images"
              middle
              color="green darken-2"
              class="edit_icon"
            >
              mdi-image-edit-outline
            </v-icon>
          </div>

          <v-card-title>
            <p>
              <span class="last_login_icon">●</span>
              {{ user.age }}歳
              {{ user.prefecture }}
            </p>
          </v-card-title>
          <v-card-subtitle>
            <div v-if="status_message_editing">
              <v-text-field
                v-model="status_message"
                label="ひとこと"
              ></v-text-field>
              <v-btn @click="update_status_message">
                更新
              </v-btn>
              <!-- <v-icon
                @click="update_status_message"
                middle
                color="green darken-2"
                class="update_icon"
              >
                mdi-check
              </v-icon> -->
              <v-btn class="cancel_btn" @click="cancel_editing_status_message"
                >キャンセル</v-btn
              >
              <!-- <v-icon
                @click="cancel_editing_status_message"
                middle
                color="green darken-2"
                class="cancel_icon"
              >
                mdi-close
              </v-icon> -->
            </div>
            <div v-else>
              {{ user.status_message }}
              <v-icon
                @click="start_editing_status_message"
                middle
                color="green darken-2"
                class="edit_icon"
              >
                mdi-pencil
              </v-icon>
            </div>
          </v-card-subtitle>
          <v-card-actions>
            <v-spacer></v-spacer>
          </v-card-actions>
        </v-card>
        <h3>自己紹介</h3>
        <div v-if="introduction_editing">
          <v-textarea v-model="introduction" label="自己紹介"></v-textarea>
          <v-btn @click="update_introduction">更新</v-btn>
          <v-btn class="cancel_btn" @click="cancel_editing_introduction"
            >キャンセル</v-btn
          >
        </div>
        <div v-else>
          {{ user.introduction }}
          <br />
          <v-icon
            @click="start_editing_introduction"
            middle
            color="green darken-2"
            class="edit_icon"
          >
            mdi-pencil
          </v-icon>
          <!-- <v-btn @click="start_editing_introduction">自己紹介編集</v-btn> -->
        </div>
        <div class="intro_detail">
          <v-simple-table>
            <template v-slot:default>
              <!-- <thead>
                <tr>
                  <th class="text-left">項目</th>
                  <th class="text-left">プロフィール</th>
                </tr>
              </thead> -->
              <tbody>
                <tr>
                  <td>名前</td>
                  <td v-if="display_name_editing">
                    <v-text-field
                      v-model="display_name"
                      label="名前"
                    ></v-text-field>
                    <v-btn @click="update_display_name">更新</v-btn>
                    <v-btn
                      class="cancel_btn"
                      @click="cancel_editing_display_name"
                      >キャンセル</v-btn
                    >
                  </td>
                  <td v-else>
                    {{ user.display_name }}
                    <v-icon
                      @click="start_editing_display_name"
                      middle
                      color="green darken-2"
                      class="edit_icon"
                    >
                      mdi-pencil
                    </v-icon>
                    <!-- <v-btn @click="start_editing_display_name">名前編集</v-btn> -->
                  </td>
                </tr>
                <tr>
                  <td>年齢</td>
                  <td>{{ user.age }}</td>
                </tr>
                <tr>
                  <td>都道府県</td>
                  <td>{{ user.prefecture }}</td>
                </tr>
                <!-- <tr>
                  <td>いいね数</td>
                  <td>{{ user.acquired_favorites }}</td>
                </tr>
                <tr>
                  <td>最終ログイン</td>
                  <td>{{ user.last_login_batch }}</td>
                </tr>-->
              </tbody>
            </template>
          </v-simple-table>
        </div>

        <!-- <p>{{ userAuth.email }}でログイン中</p>
          <button @click="logOut">ログアウト</button>-->
        <h3 class="toDetailSetting">
          詳細設定
          <v-icon
            @click="changeHiddenStatus"
            middle
            color="green darken-2"
            class="edit_icon"
          >
            mdi-chevron-down
          </v-icon>
        </h3>
        <div :class="detail_setting_class">
          <!-- <div>
            <v-btn>課金する（未実装）</v-btn>
          </div> -->
          <div>
            <v-btn @click="logOut">ログアウト</v-btn>
          </div>
          <div>
            <v-dialog v-model="dialog" persistent max-width="290">
              <template v-slot:activator="{ on, attrs }">
                <v-btn v-bind="attrs" v-on="on">
                  退会する
                </v-btn>
              </template>
              <v-card>
                <v-card-title class="headline">
                  退会確認
                </v-card-title>
                <v-card-text>このボタンを押すと退会が完了します。</v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="green darken-1" text @click="dialog = false">
                    キャンセル
                  </v-btn>
                  <v-btn color="green darken-1" text @click="unregister">
                    退会する
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import GoogleLoginPage from "~/components/GoogleLoginPage.vue";
// いいね済かどうかを判定する。
// いいねされていたら、いいね済に表示を変える。from DB data
// いいねボタンがクリックされたら、いいね済に表示を変える。
import firebase from "@/plugins/firebase";
import { v4 as uuidv4 } from "uuid";
export default {
  components: {
    GoogleLoginPage
  },
  asyncData() {
    return {
      status_message: "",
      status_message_editing: false,
      introduction: "",
      introduction_editing: false,
      display_name: "",
      display_name_editing: false,
      profile_images: "",
      profile_images_editing: false,
      isWaiting: true,
      isLogin: false,
      loginUserGoogle: [], //ログインしているユーザーの情報 from google
      loginUser: [], //ログインしているユーザーの情報 from firestore
      user: {}, //ほかのユーザー。
      user_id: "",
      detail_setting_class: "detail_setting_hiddeen",
      detail_setting_hidden: 1,
      dialog: false
    };
  },
  mounted: function() {
    firebase.auth().onAuthStateChanged(userAuth => {
      this.isWaiting = false;
      if (userAuth) {
        this.isLogin = true;
        this.loginUserGoogle = userAuth;
        // if first time, go to register page
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
      console.log("fuga");
      firebase.auth().signOut();
      console.log("hoge");
    },
    checkFirstTime() {
      console.log(this.loginUserGoogle.email);
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
            // 表示する性別
            if (doc.data().gender == "male") {
              this.loginUser.partnergender = "female";
            } else {
              this.loginUser.partnergender = "male";
            }
            // ログインユーザーのID
            this.loginUser.id = doc.id;
            this.user_id = doc.id;
            this.user = doc.data();
          });
        })
        .catch(err => {
          console.log("Error getting documents", err);
        });
    },
    start_editing_status_message() {
      this.status_message = this.user.status_message;
      this.status_message_editing = true;
    },
    async update_status_message() {
      console.log(this.status_message);
      const data = {
        status_message: this.status_message
      };
      // Add a new document in collection "cities" with ID 'LA'
      const res = await firebase
        .firestore()
        .collection("users")
        .doc(this.loginUser.id)
        .set(data, { merge: true });
      this.user.status_message = this.status_message;
      this.status_message = "";
      this.status_message_editing = false;
    },
    cancel_editing_status_message() {
      this.status_message = "";
      this.status_message_editing = false;
    },
    start_editing_introduction() {
      this.introduction = this.user.introduction;
      this.introduction_editing = true;
    },
    async update_introduction() {
      console.log(this.introduction);
      const data = {
        introduction: this.introduction
      };
      // Add a new document in collection "cities" with ID 'LA'
      const res = await firebase
        .firestore()
        .collection("users")
        .doc(this.loginUser.id)
        .set(data, { merge: true });
      this.user.introduction = this.introduction;
      this.introduction = "";
      this.introduction_editing = false;
    },
    cancel_editing_introduction() {
      this.introduction = "";
      this.introduction_editing = false;
    },
    start_editing_display_name() {
      this.display_name = this.user.display_name;
      this.display_name_editing = true;
    },
    async update_display_name() {
      console.log(this.display_name);
      const data = {
        display_name: this.display_name
      };
      // Add a new document in collection "cities" with ID 'LA'
      const res = await firebase
        .firestore()
        .collection("users")
        .doc(this.loginUser.id)
        .set(data, { merge: true });
      this.user.display_name = this.display_name;
      this.display_name = "";
      this.display_name_editing = false;
    },
    cancel_editing_display_name() {
      this.display_name = "";
      this.display_name_editing = false;
    },
    changeHiddenStatus() {
      if (this.detail_setting_hidden == 1) {
        this.detail_setting_hidden = 0;
        this.detail_setting_class = "detail_setting_unhiddeen";
      } else {
        this.detail_setting_hidden = 1;
        this.detail_setting_class = "detail_setting_hiddeen";
      }
    },
    unregister() {
      firebase
        .firestore()
        .collection("users")
        .where("mail", "==", this.loginUserGoogle.email)
        .get()
        .then(snapshot => {
          if (snapshot.empty) {
          }
          snapshot.forEach(doc => {
            console.log(doc.id);
            console.log(doc.data());
            firebase
              .firestore()
              .collection("users")
              .doc(doc.id)
              .delete();
            this.$router.push("/register");
          });
        })
        .catch(err => {
          console.log("Error getting documents", err);
        });
    },
    start_editing_profile_images() {
      this.profile_images = this.user.profile_images;
      this.profile_images_editing = true;
    },
    // 変更が必要。
    async update_profile_images() {
      const data = {
        profile_images: this.user.profile_images
      };
      // Add a new document in collection "cities" with ID 'LA'
      const res = await firebase
        .firestore()
        .collection("users")
        .doc(this.loginUser.id)
        .set(data, { merge: true });
      this.profile_images = "";
      this.profile_images_editing = false;
    },
    cancel_editing_profile_images() {
      this.profile_images = "";
      this.profile_images_editing = false;
    },
    async upload(p) {
      const file = p.target.files[0];
      console.log(file);
      const storageRef = firebase
        .storage()
        .ref("imgs/" + uuidv4() + "___" + file.name);
      console.log(storageRef);
      // 画像をStorageにアップロード
      storageRef.put(file).then(() => {
        // アップロードした画像のURLを取得
        storageRef
          .getDownloadURL()
          .then(url => {
            this.user.profile_images = url;
            this.update_profile_images();
            // 更新する こんな感じ？
            //   await firebase
            // .firestore()
            // .collection("users")
            // .doc(uuidv4())
            // .set(data);
            // this.profile_images = url;
          })
          .catch(error => {
            console.log(error);
          });
      });
    }
  }
  //   async created() {
  //     let cityRef = firebase
  //       .firestore()
  //       .collection("users")
  //       .doc(this.user_id);
  //     let getDoc = cityRef
  //       .get()
  //       .then(doc => {
  //         if (!doc.exists) {
  //           console.log("No such document!");
  //         } else {
  //           console.log("Document data:", doc.data());
  //           this.user = doc.data();
  //         }
  //       })
  //       .catch(err => {
  //         console.log("Error getting document", err);
  //       });
  //   }
};
</script>
<style scoped>
.container {
  margin: 0 auto;
  height: 70vh;
  max-width: 400px;
}
/* 最終ログインによって色を変える。 */
.last_login_icon {
  width: 20px;
  height: 20px;
  color: #005555;
  font-weight: 2000;
  border-radius: 50%;
  /* background-color: blueviolet; */
}
.mx-auto {
  /* height: 350px; */
  margin-bottom: 40px;
}

.edit_icon {
  float: right;
}

.cancel_btn {
  float: right;
}

.intro_detail {
  margin: 60px 0px 0px 0px;
}

h3 {
  margin: 40px 0px 20px 0px;
}

.detail_setting_hiddeen {
  display: none;
}

.detail_setting_unhiddeen {
}

.detail_setting_unhiddeen button {
  margin: 10px 0px 10px 0px;
}
</style>
