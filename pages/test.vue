<template>
  <div>
    <label class="postImage-appendBtn">
      <input @change="upload" type="file" data-label="画像の添付" />
    </label>
    <button @click="download">download</button>
    <p>{{ this.img_url }}</p>
    <img :src="img_url" alt="" />
  </div>
</template>
<script>
import firebase from "@/plugins/firebase";

export default {
  data() {
    return {
      //   img_url:
      //     "https://firebasestorage.googleapis.com/v0/b/matching-app-web2.appspot.com/o/imgs%2Fgithub_logo.jpg?alt=media&token=730ef4e5-6ca9-4c22-8cbe-2f5afc19c99f"
      // img_url: "gs://matching-app-web2.appspot.com/imgs/github_logo.jpg"
      img_url: ""
    };
  },
  methods: {
    async download() {
      let path = "";
      await firebase
        .storage()
        .ref()
        .child("imgs/github_logo.jpg")
        .getDownloadURL()
        .then(url => {
          console.log(url);
          this.img_url = url;
        });
      console.log(path);
    },
    upload(p) {
      const file = p.target.files[0];
      console.log(file);
      const storageRef = firebase.storage().ref("imgs/" + file.name);
      console.log(storageRef);
      // 画像をStorageにアップロード
      storageRef.put(file).then(() => {
        // アップロードした画像のURLを取得
        firebase
          .storage()
          .ref("imgs/" + file.name)
          .getDownloadURL()
          .then(url => {})
          .catch(error => {
            console.log(error);
          });
      });
    }
  },
  created() {
    this.download();
  }
};
</script>
